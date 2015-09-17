#include <stdio.h>
#include <stdlib.h>

#include <winsock2.h>
#include <windows.h>

#define BUF_SIZE (1024)
#define SERVER_INIT     ("ServerInit")
#define SERVER_OPEN     ("ServerOpen")
#define SERVER_CLOSE    ("ServerClose")
#define SERVER_SEND     ("ServerSend")
#define SERVER_RECV     ("ServerRecv")
#define SERVER_SEARCH   ("ServerSearch")
#define SERVER_DEINIT   ("ServerDeInit")

typedef int(*lpServerInit)(void);
typedef void(*lpServerSearch)(void);
typedef SOCKET(*lpServerOpen)(const char *);
typedef void(*lpServerClose)(SOCKET);
typedef void(*lpServerSend)(SOCKET, const unsigned char*, unsigned int);
typedef unsigned int(*lpServerRecv)(SOCKET, unsigned char*, unsigned int);
typedef void(*lpServerDeInit)(void);

HINSTANCE hDll;

lpServerInit ServerInit;
lpServerSearch ServerSearch;
lpServerOpen ServerOpen;
lpServerClose ServerClose;
lpServerSend ServerSend;
lpServerRecv ServerRecv;
lpServerDeInit ServerDeInit;

static void help(void) 
{
    printf("使用方法:\n");
    printf("查找从设备          709test search\n");
    printf("打开从设备          709test open 从设备ip.\n");
    printf("关闭从设备          709test close 从设备ip.\n");
    printf("发送数据到从设备    709test send 字符串.\n");
    printf("从从设备接收数据    709test recv.\n");
    exit(0);
}

int main(int argc, char *argv[])
{
    unsigned char pBuf[BUF_SIZE]={0};
    hDll = LoadLibrary("dll.dll");

    ServerInit = (lpServerInit)GetProcAddress(hDll, SERVER_INIT);
    ServerSearch = (lpServerSearch)GetProcAddress(hDll, SERVER_SEARCH);
    ServerOpen = (lpServerOpen)GetProcAddress(hDll, SERVER_OPEN);
    ServerClose = (lpServerClose)GetProcAddress(hDll, SERVER_CLOSE);
    ServerSend = (lpServerSend)GetProcAddress(hDll, SERVER_SEND);
    ServerRecv = (lpServerRecv)GetProcAddress(hDll, SERVER_RECV);
    ServerDeInit = (lpServerDeInit)GetProcAddress(hDll, SERVER_DEINIT); 
    
    /*
    printf("命令:\n");
    for(int i=0;i<argc;i++)
    { 
        printf("%d:%s\n", i, argv[i]);
    }
    */

    if(argc < 2)
    {
        help();
    } 

    if(0 == strcmp(argv[1], "search"))
    {
        ServerInit();
        ServerSearch();
        printf("查找从设备完成.\n");
        fflush(stdout);
        ServerDeInit();
    }
    else if(0 == strcmp(argv[1], "open"))
    {
        ;
    }
    else if(0 == strcmp(argv[1], "close"))
    {
        ;
    }
    else if(0 == strcmp(argv[1], "send"))
    {
        ;
    }
    else if(0 == strcmp(argv[1], "recv"))
    {
        ;
    }
    else
    {
        help();
    }
#if 0
    printf("4.\n");
    fflush(stdout);
    SOCKET s = ServerOpen("123");

    printf("5.\n");
    fflush(stdout);
    ServerSend(s, pBuf, BUF_SIZE);

    printf("6.\n");
    fflush(stdout);
    ServerRecv(s, pBuf, BUF_SIZE);

    printf("7.\n");
    fflush(stdout);
    ServerClose(s);

    printf("9.\n");
    fflush(stdout);
#endif

    FreeLibrary(hDll);//释放Dll句柄
    return 0;
}


