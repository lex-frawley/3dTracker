#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

const char* HOST = "127.0.0.1";
const int PORT = 5000;

int main() {
    // Create a socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Failed to create socket\n";
        return 1;
    }

    // Connect to the server
    sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, HOST, &serv_addr.sin_addr) <= 0) {
        std::cerr << "Failed to convert address\n";
        return 1;
    }
    if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Failed to connect to server\n";
        return 1;
    }

    // Receive data from the server
    float data[3];
    while (true) {
        ssize_t n = recv(sock, data, sizeof(data), 0);
        if (n <= 0) {
            break;
        }

        // Use the received data as necessary
        float x = data[0];
        float y = data[1];
        float z = data[2];
    }

    // Close the socket
    close(sock);

    return 0;
}
