#include <stdio.h>
#include <stdlib.h>

#include <winsock2.h>
#include <windows.h>

/* 用于测试的两个宏 */
#define TARGET_IP       ("127.0.0.1")
#define TARGET_PORT     (8001)


#define BUF_SIZE        (1024)
#define SERVER_INIT     ("ServerInit")
#define SERVER_OPEN     ("ServerOpen")
#define SERVER_CLOSE    ("ServerClose")
#define SERVER_SEND     ("ServerSend")
#define SERVER_RECV     ("ServerRecv")
#define SERVER_SEARCH   ("ServerSearch")
#define SERVER_DEINIT   ("ServerDeInit")

typedef int(*lpServerInit)(void);
typedef void(*lpServerSearch)(void);
typedef void(*lpServerSend)(const char *, int, const char *, int);
typedef int(*lpServerRecv)(char *, int, char*);
typedef void(*lpServerDeInit)(void);

HINSTANCE hDll;

lpServerInit ServerInit;
lpServerSearch ServerSearch;
lpServerSend ServerSend;
lpServerRecv ServerRecv;
lpServerDeInit ServerDeInit;

static void help(void) 
{
    printf("Usage:\n");
    printf("Serach  709test search.\n");
    printf("Send    709test send ip str.\n");
    printf("Recv    709test recv.\n");
    exit(0);
}

int main(int argc, char *argv[])
{
    hDll = LoadLibrary("dll.dll");

    ServerInit = (lpServerInit)GetProcAddress(hDll, SERVER_INIT);
    ServerSearch = (lpServerSearch)GetProcAddress(hDll, SERVER_SEARCH);
    ServerSend = (lpServerSend)GetProcAddress(hDll, SERVER_SEND);
    ServerRecv = (lpServerRecv)GetProcAddress(hDll, SERVER_RECV);
    ServerDeInit = (lpServerDeInit)GetProcAddress(hDll, SERVER_DEINIT); 
    
    if(argc < 2)
    {
        help();
    } 

    if(0 == strcmp(argv[1], "search"))
    {
        ServerInit();
        ServerSearch();
        ServerDeInit();
        printf("Search Done.\n");
        fflush(stdout);
    }
    else if(0 == strcmp(argv[1], "send"))
    {
        if(4 != argc)
        {
            help();
        }
        const char *pBuf = argv[3];
        int len = strlen(pBuf) + 1;
        ServerInit(); 
        ServerSend(argv[2], TARGET_PORT, pBuf, strlen(pBuf) + 1);
        ServerDeInit();

        printf("send;%s(%d) to %s:%d.\n", pBuf, len, argv[2], TARGET_PORT);
        fflush(stdout);
    }
    else if(0 == strcmp(argv[1], "recv"))
    {
        int readBytes = 0;
        char pBuf[BUF_SIZE] = {0};
        char remoteAddr[BUF_SIZE] = {0};
        memset(pBuf, 0, BUF_SIZE);
        memset(remoteAddr, 0, BUF_SIZE);

        ServerInit(); 
        readBytes = ServerRecv(pBuf, BUF_SIZE, remoteAddr);
        ServerDeInit();

        printf("from:%s recv %s(%d).\n", remoteAddr, pBuf, readBytes);
        fflush(stdout);
    }
    else
    {
        help();
    }

    FreeLibrary(hDll);
    return 0;
}

