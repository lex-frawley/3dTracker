use std::io::prelude::*;
use std::net::TcpStream;
use byteorder::{ByteOrder, LittleEndian};

const HOST: &str = "127.0.0.1";
const PORT: u16 = 5000;

fn main() {
    // Connect to the server
    let mut stream = TcpStream::connect((HOST, PORT)).unwrap();

    // Receive data from the server
    let mut data = [0u8; 12];  // 3 floats x 4 bytes per float
    loop {
        match stream.read_exact(&mut data) {
            Ok(_) => {
                // Convert the bytes to a tuple of floats
                let tuple_of_floats = (
                    LittleEndian::read_f32(&data[0..4]),
                    LittleEndian::read_f32(&data[4..8]),
                    LittleEndian::read_f32(&data[8..12]),
                );

                // Use the tuple of floats as necessary
                let x = tuple_of_floats.0;
                let y = tuple_of_floats.1;
                let z = tuple_of_floats.2;
            }
            Err(_) => break,
        }
    }
}
