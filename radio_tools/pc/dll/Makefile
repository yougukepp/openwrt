all:
	make clean
	make -C dll
	make -C test 
	./709test

clean:
	make -C dll clean
	make -C test clean
	rm -rf *.exe *.dll
