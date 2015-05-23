#!/bin/sh

find . -name "*.[h|c]" > cscope.files
cscope -bkq -i cscope.files
ctags -R --c++-kinds=+p --fields=+iaS --extra=+q

