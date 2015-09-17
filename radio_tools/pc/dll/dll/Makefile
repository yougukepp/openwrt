include ../buildvars.mk

LIB=-luser32
LDFLAGS=-shared -Wl,--output-def=libdll.def -Wl,--out-implib=libdll.a -Wl,--dll

all:clean dll.o
	$(LD) $(LDFLAGS) dll.o -o dll.dll -s $(LIB)
	cp -rf dll.dll ../

dll.o:dll.c
	$(CC) $(CFLAGS) dll.c -o dll.o

clean:
	rm -rf *.dll *.o
