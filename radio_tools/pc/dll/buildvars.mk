MINGW_GCC=x86_64-w64-mingw32-gcc
#MINGW_GCC=i686-pc-mingw32-gcc

CC=$(MINGW_GCC)
LD=$(MINGW_GCC)
CFLAGS=-std=c11 -Wall -DBUILD_DLL -O2 -c 

