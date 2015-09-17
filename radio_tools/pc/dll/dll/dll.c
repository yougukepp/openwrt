#include <stdio.h>
#include <WINSOCK2.H>

#include "dll.h"

void DLL_EXPORT ServerInit(void)
{
  printf("%s,%d.\n", __FILE__, __LINE__);
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
  printf("%s,%d.\n", __FILE__, __LINE__);
}

