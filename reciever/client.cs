using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

const string host = "127.0.0.1";
const int port = 5000;

var client = new TcpClient(host, port);
var stream = client.GetStream();

while (true)
{
    // Receive the data over the socket connection
    var buffer = new byte[12];  // 3 floats x 4 bytes per float
    stream.Read(buffer, 0, buffer.Length);

    // Convert the bytes to a tuple of floats
    var tuple = ByteArrayToTuple<float>(buffer);

    // Use the tuple of floats as necessary
    var x = tuple.Item1;
    var y = tuple.Item2;
    var z = tuple.Item3;
}

// Helper function to convert a byte array to a tuple of a specified type
private static T ByteArrayToTuple<T>(byte[] bytes)
{
    var handle = GCHandle.Alloc(bytes, GCHandleType.Pinned);
    try
    {
        return (T)Marshal.PtrToStructure(handle.AddrOfPinnedObject(), typeof(T));
    }
    finally
    {
        handle.Free();
    }
}
