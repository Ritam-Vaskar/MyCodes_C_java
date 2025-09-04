#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib") // Link with ws2_32.lib

int main() {
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;
    char message[1024], server_reply[2000];

    printf("Initialising Winsock...\n");
    if (WSAStartup(MAKEWORD(2,2),&wsa) != 0) {
        printf("Failed. Error Code : %d\n",WSAGetLastError());
        return 1;
    }
    printf("Initialised.\n");

    // Create a socket
    s = socket(AF_INET, SOCK_STREAM, 0); // Fill in the blank
    if (s == INVALID_SOCKET) {
        printf("Could not create socket : %d\n", WSAGetLastError());
        return 1;
    }
    printf("Socket created.\n");

    server.sin_addr.s_addr = inet_addr("127.0.0.1"); // Fill in the blank
    server.sin_family = AF_INET;
    server.sin_port = htons(8888);

    // Connect to remote server
    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0) { // Fill in the blank
        printf("Connect error\n");
        return 1;
    }
    printf("Connected\n");

    // Communicate with server
    while(1) {
        printf("Enter message: ");
        gets(message);

        if (send(s, message, strlen(message), 0) < 0) { // Fill in the blank
            printf("Send failed\n");
            return 1;
        }

        if (recv(s, server_reply, 2000, 0) < 0) { // Fill in the blank
            printf("Recv failed\n");
            break;
        }

        printf("Server reply: %s\n", server_reply);
    }

    closesocket(s);
    WSACleanup();

    return 0;
}