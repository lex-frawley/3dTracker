package main

import (
	"encoding/binary"
	"net"
)

const (
	host = "127.0.0.1"
	port = "5000"
)

func main() {
	// Connect to the server
	conn, err := net.Dial("tcp", net.JoinHostPort(host, port))
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	// Receive data from the server
	data := make([]byte, 12) // 3 floats x 4 bytes per float
	for {
		_, err := conn.Read(data)
		if err != nil {
			break
		}

		// Convert the bytes to a tuple of floats
		x := binary.LittleEndian.Float32(data[0:4])
		y := binary.LittleEndian.Float32(data[4:8])
		z := binary.LittleEndian.Float32(data[8:12])

		// Use the tuple of floats as necessary
		_ = x
		_ = y
		_ = z
	}
}
