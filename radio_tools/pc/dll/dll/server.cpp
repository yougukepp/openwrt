#include "typedef.h"
#include <stdio.h>
#include "server.h"

std::list<DEV_INFO> gDevs;
static CRITICAL_SECTION gCs;                  // �ؼ��� ��

static DWORD WINAPI ThreadListen(LPVOID argv);
static void AddDev(SOCKET client, SOCKADDR_IN clientAddr);

/* ��ʼ����(��ʼ����listen accept�߳�) */
extern "C" _declspec(dllexport) void ServerInit(void)
{
  WORD wVersionRequested;  
  WSADATA wsaData; 

  InitializeCriticalSection(&gCs);//��ʼ���ٽ���
  gDevs.clear();
  
  wVersionRequested=MAKEWORD(2,2);  
  if(WSAStartup(wVersionRequested,&wsaData)!=0)  
  {  
	  ERROR_BOX("��ʼ��ʧ��!");
	  return;
  }  

  HANDLE threadListen;
  DWORD  threadListenId;
  /* ���������߳� */
  threadListen = CreateThread(
      0,                   //Ĭ�ϰ�ȫ����
      0,                   //��ջ��СĬ��(2M)
      ThreadListen,        //�߳���ں���
      0,                   //����û��  
      0,                   //����ʱ��״̬
      &threadListenId      //����߳�ID
      );
  CloseHandle(threadListen);
  //printf("%s,%d.\n", __FILE__, __LINE__);
}

/* ����ӽڵ��tcp���� */
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

/* �ر���ӽڵ��tcp���� */
extern "C" _declspec(dllexport) void ServerClose(SOCKET socket)
{
    //closesocket(socket);
}

/* ���� */
extern "C" _declspec(dllexport) void ServerSend(SOCKET socket, const u8 *pBuf, u32 len)
{
	int rst = 0;
	rst = send(socket, (const char *)pBuf, len, 0);
	if(-1 == rst)
	{
		ERROR_BOX("����ʧ��!"); 
	}
}

/* ���� */
extern "C" _declspec(dllexport) u32 ServerRecv(SOCKET socket, u8 *pBuf, u32 len)
{
	int rst = 0;
	
	rst = recv(socket, (char *)pBuf, len, 0);
	if(SOCKET_ERROR == rst)
	{ 
          /* ��������� */
          char sNum[100];
          int b = 0;
          b = WSAGetLastError();
          itoa(b, sNum, 10); 
          
          string s = "����ʧ��:";
          s += sNum; 
          ERROR_BOX(s.c_str()); 
	}
	if (0 == rst)
	{
		ERROR_BOX("�ͻ����Ѿ��ر�!"); 
	}
	if (rst > 0)
	{
		/* �������� */
		return rst;
	}

	return 0;
}

/* ��β���� */
extern "C" _declspec(dllexport) void ServerDeInit(void)
{
  DeleteCriticalSection(&gCs);//ɾ���ٽ���
  WSACleanup(); 
  //printf("%s,%d.\n", __FILE__, __LINE__);
}

/* ��ȡ���豸�б� */
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
	    ERROR_BOX("��ȡ���豸�б����!"); 
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
  SOCKET sever = 0;    ///�����׽���
  SOCKET client = 0;

  int cliAddrLen = 0;
  int rst = 0;
  int err = 0;

  SOCKADDR_IN serverAddr;   //��������ַ��Ϣ
  SOCKADDR_IN clientAddr;   //�ͻ��˵�ַ��Ϣ

  bzero(&serverAddr, sizeof(SOCKADDR_IN));
  bzero(&clientAddr, sizeof(SOCKADDR_IN));

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
  serverAddr.sin_port = htons(SER_PORT);  
  memset(serverAddr.sin_zero,0,8);

  /* �����׽��� */
  sever = socket(AF_INET,SOCK_STREAM,0);  
  if (sever == INVALID_SOCKET)  
  {  
    ERROR_BOX("�����׽���ʧ��!"); 
    return 1;  
  }  

  rst = bind(sever, (SOCKADDR *)&serverAddr, sizeof(SOCKADDR));
  err = WSAGetLastError();
  /* �� */
  if(0 != rst)  
  {  
    ERROR_BOX("��ʧ��!");   
    return 1;  
  }

  /* ���� */
  if (int i = listen(sever,6) != 0)  
  {  
    /* ��������� */
    char sNum[100];
    int b = 0;
    b = WSAGetLastError();
    itoa(b, sNum, 10);

    string s = "����ʧ��:";
    s += sNum;

    ERROR_BOX(s.c_str()); 
    return 1;  
  }  
  cliAddrLen = sizeof(SOCKADDR); 
  
  //MESSAGE_BOX("���������ѳɹ�����......");

  while (1)   //�������˼��������µ�����  
  {  
    /* ���ؿͻ����׽��� */
    if((client = accept(sever, (SOCKADDR *)&clientAddr, &cliAddrLen)) == INVALID_SOCKET)  
    {  
      ERROR_BOX("�ͻ����Ѿ��Ͽ�����!");
      break;  
    } 

    /* ���ͻ��˵ĵ��׽��ֺ͵�ַ�����豸�б� */
    AddDev(client, clientAddr);
    /* FIXME:���ߵ����ɾ��? */
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

  EnterCriticalSection(&gCs);//�����ٽ���
  gDevs.push_back (dev);
  LeaveCriticalSection(&gCs);//�뿪�ٽ���

  //MESSAGE_BOX(dev.mStrKey.c_str()); 
}
