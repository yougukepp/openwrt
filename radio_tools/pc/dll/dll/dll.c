#include <stdio.h>
#include <string.h>

#include <WINSOCK2.H>
#include <process.h>

#include "dll.h"

#define BUF_SIZE    (1024)

void DLL_EXPORT ServerInit(void)
{
    WORD wVersionRequested;  
    WSADATA wsaData; 

    wVersionRequested=MAKEWORD(2,2);  
    if(WSAStartup(wVersionRequested,&wsaData)!=0)  
    {  
        printf("%s,%d WSAStartup失败.\n", __FILE__, __LINE__);
        return;
    } 
}

void DLL_EXPORT ServerSearch(void)
{
    int ret = 0;
    char hostName[BUF_SIZE]; 
    char cmd[BUF_SIZE];
    char host_ip[BUF_SIZE];
    char ping_buf[BUF_SIZE]; 
    unsigned char ip[4] = {0};
    float step = 100.0f / 254;
    float rate = 0.0f;
    int line_cnt = 0;
    FILE *device_ip_list_file = NULL;

    memset(hostName, 0, sizeof(hostName));
    memset(cmd, 0, sizeof(cmd));
    device_ip_list_file = fopen("ips.log", "w");

    ret = gethostname(hostName,sizeof(hostName));
    if(0 != ret)
    {
        printf("%s,%d gethostbyname 错误.\n", __FILE__, __LINE__);
        return;
    }

    /* 求取主机分段ip */
    struct hostent *pHostent = gethostbyname(hostName); 
    if(NULL != pHostent)
    {
        for(int i=0;i<4;i++)
        {
            ip[i] = pHostent->h_addr_list[0][i] & 0x00ff;
        }
    }

    /* 逐个主机Ping */
    for(int i=0;i<256;i++)
    {
        /* 构造同网段主机 */
        if( (i == ip[3]) || (i == 255) )
        {
            continue;
        }
        memset(host_ip, 0, sizeof(host_ip));
        sprintf(host_ip, "%d.%d.%d.%d", ip[0], ip[1], ip[2], i);

        /* 构造ping命令 */ 
        memset(cmd, 0, sizeof(cmd));
        strcat(cmd, "ping -f -n 1 -w 1 ");
        strcat(cmd, host_ip);
        //strcat(cmd, " > ping.log");

        //system(cmd);
        FILE *pingOut = _popen(cmd, "rt");
        if(NULL == pingOut)
        {
            printf("%s,%d _popen错误.\n", __FILE__, __LINE__);
            return;
        } 
        line_cnt = 0;
        while(!feof( pingOut))
        {
            fgets(ping_buf, BUF_SIZE, pingOut);
            /*printf("%d:", line_cnt);
            printf(ping_buf);*/
            line_cnt++;
        } 
        if(9 == line_cnt) /* ping有回显输出9行 否则7行 */
        {
            fprintf(device_ip_list_file, "%s\n", host_ip);
            fflush(device_ip_list_file);
        }

        _pclose(pingOut);

        printf("%s:", cmd);
        printf("\t\t\t\t%.2f%%\n", rate);
        fflush(stdout);
        rate += step;
    } 
    fclose(device_ip_list_file);
}

SOCKET DLL_EXPORT ServerOpen(const char *ipAndPort)
{
  printf("%s,%d.\n", __FILE__, __LINE__);
  return 0;
}

void DLL_EXPORT ServerClose(SOCKET socket)
{
  printf("%s,%d.\n", __FILE__, __LINE__);
}

void DLL_EXPORT ServerSend(SOCKET socket, const u8 *pBuf, u32 len)
{
  printf("%s,%d.\n", __FILE__, __LINE__);
}

u32 DLL_EXPORT ServerRecv(SOCKET socket, u8 *pBuf, u32 len)
{
  printf("%s,%d.\n", __FILE__, __LINE__);

  return 0;
}

void DLL_EXPORT ServerDeInit(void)
{ 
  WSACleanup(); 
}

