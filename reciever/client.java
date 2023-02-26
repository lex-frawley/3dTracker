import java.io.*;
import java.net.*;

public class Receiver {
    public static void main(String[] args) throws IOException {
        String host = "127.0.0.1";
        int port = 5000;

        // Connect to the server
        Socket socket = new Socket(host, port);

        // Receive data from the server
        DataInputStream in = new DataInputStream(socket.getInputStream());
        byte[] data = new byte[12]; // 3 floats x 4 bytes per float
        while (true) {
            in.readFully(data);

            // Convert the bytes to a tuple of floats
            float x = Float.intBitsToFloat(
                ((data[3] & 0xff) << 24) |
                ((data[2] & 0xff) << 16) |
                ((data[1] & 0xff) << 8) |
                ((data[0] & 0xff))
            );
            float y = Float.intBitsToFloat(
                ((data[7] & 0xff) << 24) |
                ((data[6] & 0xff) << 16) |
                ((data[5] & 0xff) << 8) |
                ((data[4] & 0xff))
            );
            float z = Float.intBitsToFloat(
                ((data[11] & 0xff) << 24) |
                ((data[10] & 0xff) << 16) |
                ((data[9] & 0xff) << 8) |
                ((data[8] & 0xff))
            );

            // Use the tuple of floats as necessary
            // ...
        }
    }
}
