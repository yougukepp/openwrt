#include "typedef.h"
#include <stdio.h>
#include "server.h"

std::list<DEV_INFO> gDevs;
static CRITICAL_SECTION gCs;                  // 关键段 锁

static DWORD WINAPI ThreadListen(LPVOID argv);
static void AddDev(SOCKET client, SOCKADDR_IN clientAddr);

/* 初始化库(开始启动listen accept线程) */
extern "C" _declspec(dllexport) void ServerInit(void)
{
  WORD wVersionRequested;  
  WSADATA wsaData; 

  InitializeCriticalSection(&gCs);//初始化临界区
  gDevs.clear();
  
  wVersionRequested=MAKEWORD(2,2);  
  if(WSAStartup(wVersionRequested,&wsaData)!=0)  
  {  
	  ERROR_BOX("初始化失败!");
	  return;
  }  

  HANDLE threadListen;
  DWORD  threadListenId;
  /* 启动监听线程 */
  threadListen = CreateThread(
      0,                   //默认安全级别
      0,                   //堆栈大小默认(2M)
      ThreadListen,        //线程入口函数
      0,                   //参数没有  
      0,                   //创建时的状态
      &threadListenId      //获得线程ID
      );
  CloseHandle(threadListen);
  //printf("%s,%d.\n", __FILE__, __LINE__);
}

/* 打开与从节点的tcp连接 */
extern "C" _declspec(dllexport) SOCKET ServerOpen(const char *ipAndPort)
{
	SOCKET client = -1;
	int rst = 0;

	for (std::list<DEV_INFO>::iterator it=gDevs.begin(); it != gDevs.end(); ++it)
	{
		string dev = "";
		dev = it->mStrKey;

		rst = dev.compare(ipAndPort);

		if (0 == rst)
		{
			client = it->mClientSocket;
			break;
		}
	}
    
	return client;
}

/* 关闭与从节点的tcp连接 */
extern "C" _declspec(dllexport) void ServerClose(SOCKET socket)
{
    //closesocket(socket);
}

/* 发送 */
extern "C" _declspec(dllexport) void ServerSend(SOCKET socket, const u8 *pBuf, u32 len)
{
	int rst = 0;
	rst = send(socket, (const char *)pBuf, len, 0);
	if(-1 == rst)
	{
		ERROR_BOX("发送失败!"); 
	}
}

/* 接收 */
extern "C" _declspec(dllexport) u32 ServerRecv(SOCKET socket, u8 *pBuf, u32 len)
{
	int rst = 0;
	
	rst = recv(socket, (char *)pBuf, len, 0);
	if(SOCKET_ERROR == rst)
	{ 
          /* 具体错误编号 */
          char sNum[100];
          int b = 0;
          b = WSAGetLastError();
          itoa(b, sNum, 10); 
          
          string s = "接收失败:";
          s += sNum; 
          ERROR_BOX(s.c_str()); 
	}
	if (0 == rst)
	{
		ERROR_BOX("客户端已经关闭!"); 
	}
	if (rst > 0)
	{
		/* 正常接收 */
		return rst;
	}

	return 0;
}

/* 收尾工作 */
extern "C" _declspec(dllexport) void ServerDeInit(void)
{
  DeleteCriticalSection(&gCs);//删除临界区
  WSACleanup(); 
  //printf("%s,%d.\n", __FILE__, __LINE__);
}

/* 获取从设备列表 */
extern "C" _declspec(dllexport) u32 ServerGetDevList(u8 *pBuf, u32 len)
{
	string buf = "";
	u32 bufLen = 0;

	for (std::list<DEV_INFO>::iterator it=gDevs.begin(); it != gDevs.end(); ++it)
	{
		buf += it->mStrKey;
		buf += ",";
	}

	bufLen = buf.length();
	if (len <= bufLen)
	{
	    ERROR_BOX("获取的设备列表过长!"); 
	}

	buf.copy((char *)pBuf, bufLen, 0);

	return bufLen;
}

extern "C" _declspec(dllexport) void bzero(void *ptr, int n)
{
	memset(ptr, 0, n);
}

static DWORD WINAPI ThreadListen(LPVOID argv)
{  
  SOCKET sever = 0;    ///定义套接字
  SOCKET client = 0;

  int cliAddrLen = 0;
  int rst = 0;
  int err = 0;

  SOCKADDR_IN serverAddr;   //服务器地址信息
  SOCKADDR_IN clientAddr;   //客户端地址信息

  bzero(&serverAddr, sizeof(SOCKADDR_IN));
  bzero(&clientAddr, sizeof(SOCKADDR_IN));

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
  serverAddr.sin_port = htons(SER_PORT);  
  memset(serverAddr.sin_zero,0,8);

  /* 创建套接字 */
  sever = socket(AF_INET,SOCK_STREAM,0);  
  if (sever == INVALID_SOCKET)  
  {  
    ERROR_BOX("创建套接字失败!"); 
    return 1;  
  }  

  rst = bind(sever, (SOCKADDR *)&serverAddr, sizeof(SOCKADDR));
  err = WSAGetLastError();
  /* 绑定 */
  if(0 != rst)  
  {  
    ERROR_BOX("绑定失败!");   
    return 1;  
  }

  /* 侦听 */
  if (int i = listen(sever,6) != 0)  
  {  
    /* 具体错误编号 */
    char sNum[100];
    int b = 0;
    b = WSAGetLastError();
    itoa(b, sNum, 10);

    string s = "侦听失败:";
    s += sNum;

    ERROR_BOX(s.c_str()); 
    return 1;  
  }  
  cliAddrLen = sizeof(SOCKADDR); 
  
  //MESSAGE_BOX("服务器端已成功启动......");

  while (1)   //服务器端继续搜索新的连接  
  {  
    /* 返回客户端套接字 */
    if((client = accept(sever, (SOCKADDR *)&clientAddr, &cliAddrLen)) == INVALID_SOCKET)  
    {  
      ERROR_BOX("客户端已经断开连接!");
      break;  
    } 

    /* 将客户端的的套接字和地址存入设备列表 */
    AddDev(client, clientAddr);
    /* FIXME:断线的如何删除? */
  }
  //closesocket(sever);

  return 0;
}

static void AddDev(SOCKET client, SOCKADDR_IN clientAddr)
{
  DEV_INFO dev;
  char buf[10];
  int port = 0;

  dev.mStrKey += inet_ntoa(clientAddr.sin_addr);
  dev.mStrKey += ":";
  port = ntohs(clientAddr.sin_port);
  dev.mStrKey += itoa(port, buf, 10);

  dev.mClientSocket = client;
  memcpy(&dev.mClientAddr, &clientAddr, sizeof(clientAddr));

  EnterCriticalSection(&gCs);//进入临界区
  gDevs.push_back (dev);
  LeaveCriticalSection(&gCs);//离开临界区

  //MESSAGE_BOX(dev.mStrKey.c_str()); 
}
