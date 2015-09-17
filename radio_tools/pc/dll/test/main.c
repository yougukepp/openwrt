#include <stdio.h>
#include <stdlib.h>

#include <winsock2.h>
#include <windows.h>

#define BUF_SIZE (1024)

typedef int(*lpServerInit)(void);
typedef SOCKET(*lpServerOpen)(const char *);
typedef void(*lpServerClose)(SOCKET);
typedef void(*lpServerSend)(SOCKET, const unsigned char*, unsigned int);
typedef unsigned int(*lpServerRecv)(SOCKET, unsigned char*, unsigned int);
typedef void(*lpServerDeInit)(void);

HINSTANCE hDll;

lpServerInit ServerInit;
lpServerOpen ServerOpen;
lpServerClose ServerClose;
lpServerSend ServerSend;
lpServerRecv ServerRecv;
lpServerDeInit ServerDeInit;

int main()
{
    unsigned char pBuf[BUF_SIZE]={0};

    hDll = LoadLibrary("dll.dll");

    ServerInit = (lpServerInit)GetProcAddress(hDll, "ServerInit");
    ServerOpen = (lpServerOpen)GetProcAddress(hDll, "ServerOpen");
    ServerClose = (lpServerClose)GetProcAddress(hDll, "ServerClose");
    ServerSend = (lpServerSend)GetProcAddress(hDll, "ServerSend");
    ServerRecv = (lpServerRecv)GetProcAddress(hDll, "ServerRecv");
    ServerDeInit = (lpServerDeInit)GetProcAddress(hDll, "ServerDeInit");

    printf("1.\n");
    fflush(stdout);

    ServerInit();

    printf("2.\n");
    fflush(stdout);
    SOCKET s = ServerOpen("123");

    printf("3.\n");
    fflush(stdout);
    ServerSend(s, pBuf, BUF_SIZE);

    printf("4.\n");
    fflush(stdout);
    ServerRecv(s, pBuf, BUF_SIZE);

    printf("5.\n");
    fflush(stdout);
    ServerClose(s);

    printf("6.\n");
    fflush(stdout);
    ServerDeInit();

    printf("7.\n");
    fflush(stdout);
    FreeLibrary(hDll);//ÊÍ·ÅDll¾ä±ú
    return 0;
}


