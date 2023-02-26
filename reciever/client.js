const net = require('net');
const { Buffer } = require('buffer');

const HOST = '127.0.0.1';
const PORT = 5000;

const client = new net.Socket();
client.connect(PORT, HOST, () => {
  console.log(`Connected to ${HOST}:${PORT}`);
});

client.on('data', (data) => {
  // Convert the data buffer to a tuple of floats
  const tuple_of_floats = [
    data.readFloatLE(0),
    data.readFloatLE(4),
    data.readFloatLE(8)
  ];

  // Use the tuple of floats as necessary
  const [x, y, z] = tuple_of_floats;
});

client.on('close', () => {
  console.log('Connection closed');
});
