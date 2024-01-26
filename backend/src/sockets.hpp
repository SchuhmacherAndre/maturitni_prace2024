// class for socket communication c++ server -> $client
// designed by me 
// based on https://learn.microsoft.com/en-us/windows/win32/winsock/using-winsock

#pragma once
#include <iostream>
#include <WinSock2.h>

class cSockets {
public:
	int init();

private:
    WSADATA wsaData;
    int iResult;

    SOCKET ListenSocket = INVALID_SOCKET;
    SOCKET ClientSocket = INVALID_SOCKET;

    struct addrinfo* result = NULL;
    struct addrinfo hints;

    int iSendResult;
    char recvbuf[512];
    int recvbuflen = 512;
};

extern cSockets* sockets;