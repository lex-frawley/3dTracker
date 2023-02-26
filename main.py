import asyncio
import cv2
import numpy as np
import struct
from pseyepy import Camera
from scipy import linalg
from send import SocketSender

class Point:
    def __init__(self, xy, id):
        self.xy = xy
        self.id = id

    def print_all(self):
        print(f"ID = {self.id} \t | X,Y = {self.xy}")

class Camera:
    def __init__(self, index, proj_paf):
        self.index = index
        self.projection_matrix = self.load_projection(proj_paf)
        self.img_queue = asyncio.Queue()
        self.queue = asyncio.Queue()

    def load_projection(self, path):
        cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

        # note we also have to specify the type to retrieve other wise we only get a
        # FileNode object back instead of a matrix
        proj_mat = cv_file.getNode("P").mat()

        cv_file.release()
        return proj_mat

    async def process_footage(self):
        cap = cv2.VideoCapture(self.index)
        cap = Camera(self.index, fps=120)
        while True:
            # Capture frame-by-frame
            frame, timestamp = cap.read()

            # Perform image processing to extract the small circle blob
            frame, bin = self.image_processing(frame)

            asyncio.create_task(self.img_queue.put((frame, bin)))

            # Detect the small blob and return its coordinates
            point = self.get_point(frame, bin)

            # Send the coordinates to the event loop
            await asyncio.sleep(0)
            asyncio.create_task(self.queue.put(point))

    def image_processing(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        thresh_val = cv2.getTrackbarPos('thresh value', 'combined')
        ret, bin = cv2.threshold(frame,thresh_val,255,cv2.THRESH_BINARY)
        return frame, bin

    def get_point(self, frame, bin):
        bin = cv2.bitwise_not(bin)
        # detect circles in the image
        params = cv2.SimpleBlobDetector_Params()

        params.filterByArea = True
        params.minArea = 5

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(bin)
        pts = cv2.KeyPoint_convert(keypoints)
        # blobs = cv2.drawKeypoints(im, keypoints, im, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        point_list = []   
        for i in range(len(pts)):
            p = Point([pts[i][0],pts[i][1]], i)
            point_list.append(p)
        
        if point_list:
            return point_list[0].xy

class DLT:
    def __init__(self, camera1, camera2, host, port):
        self.camera1 = camera1
        self.camera2 = camera2
        self.sender = SocketSender(host, port)

    def nothing(self, x):
        pass
    
    async def run(self):
        cv2.namedWindow('combined')
        cv2.createTrackbar('thresh value', 'combined', 0, 255, self.nothing)
        while True:
            c1frame, c1bin = self.camera1.img_queue.get()
            c2frame, c2bin = self.camera1.img_queue.get()

            combined_overall = self.combine_images(c1frame, c2frame, c1bin, c2bin)
            cv2.imshow('combined', combined_overall)

            # Get the coordinates from both cameras
            point1 = await self.camera1.queue.get()
            point2 = await self.camera2.queue.get()

            # Compute the 3D position using Direct Linear Transformation (DLT)
            p1 = self.camera1.projection_matrix
            p2 = self.camera2.projection_matrix
            if point1 and point2:
                point_3d = self.dlt(p1, p2, point1, point2)
                # Do something with the 3D position
                data = struct.pack('fff', point_3d[0], point_3d[1], point_3d[2])
                self.sender.send(data)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break

    def combine_images(self, fr, fl, br, bl):
        combined_frame = np.concatenate((fr, fl), axis=1)
        combined_bin = np.concatenate((br, bl), axis=1)
        combined_overall = np.concatenate((combined_frame, combined_bin), axis=0)
        return combined_overall

    def DLT(self, P1, P2, point1, point2):
 
        A = [point1[1]*P1[2,:] - P1[1,:],
            P1[0,:] - point1[0]*P1[2,:],
            point2[1]*P2[2,:] - P2[1,:],
            P2[0,:] - point2[0]*P2[2,:]
            ]
        A = np.array(A).reshape((4,4))
    
        B = A.transpose() @ A
        
        U, s, Vh = linalg.svd(B, full_matrices = False)
    
        return Vh[3,0:3]/Vh[3,3]

    def __del__(self):
        self.sender.close()

async def main(host, port):
    # Set up the cameras
    camera1 = Camera(0, 'proj_mat_right.yml')
    camera2 = Camera(1, 'proj_mat_left.yml')

    # Set up the processing tasks for both cameras
    asyncio.create_task(camera1.process_footage())
    asyncio.create_task(camera2.process_footage())

    # Run the DLT algorithm to get the 3D position
    dlt = DLT(camera1, camera2, host, port)
    await dlt.run()

if __name__ == '__main__':
    host = '127.0.0.1'  # localhost
    port = 5000
    asyncio.run(main(host, port))