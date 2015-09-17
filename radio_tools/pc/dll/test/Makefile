include ../buildvars.mk

LIB=
LDFLAGS=

all:clean main.o
	$(LD) $(LDFLAGS) main.o -o test -s $(LIB) -s
	cp -rf test ../709test

main.o:main.c
	$(CC) $(CFLAGS) main.c -o main.o

clean:
	rm -rf test *.o
