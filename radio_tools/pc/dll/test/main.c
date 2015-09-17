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
    printf("ʹ�÷���:\n");
    printf("���Ҵ��豸          709test search\n");
    printf("�򿪴��豸          709test open ���豸ip.\n");
    printf("�رմ��豸          709test close ���豸ip.\n");
    printf("�������ݵ����豸    709test send �ַ���.\n");
    printf("�Ӵ��豸��������    709test recv.\n");
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
    printf("����:\n");
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
        printf("���Ҵ��豸���.\n");
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

    FreeLibrary(hDll);//�ͷ�Dll���
    return 0;
}


