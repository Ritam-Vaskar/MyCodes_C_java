#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib") // Link with ws2_32.lib

int main() {
    WSADATA wsa;
    SOCKET s, new_socket;
    struct sockaddr_in server, client;
    int c;
    char *message;

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

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY; // Fill in the blank
    server.sin_port = htons(8888);

    // Bind
    if (bind(s, (struct sockaddr *)&server, sizeof(server)) == SOCKET_ERROR) { // Fill in the blank
        printf("Bind failed with error code : %d\n", WSAGetLastError());
        return 1;
    }
    printf("Bind done\n");

    // Listen to incoming connections
    listen(s, 3); // Fill in the blank

    printf("Waiting for incoming connections...\n");

    c = sizeof(struct sockaddr_in);

    new_socket = accept(s, (struct sockaddr *)&client, &c); // Fill in the blank
    if (new_socket == INVALID_SOCKET) {
        printf("Accept failed with error code : %d\n", WSAGetLastError());
        return 1;
    }

    printf("Connection accepted\n");

    // Reply to the client
    message = "Hello Client, I have received your connection.\n";
    send(new_socket, message, strlen(message), 0); // Fill in the blank

    closesocket(s);
    WSACleanup();

    return 0;
}