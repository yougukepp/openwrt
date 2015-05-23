""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" VIM7.3 CSCOPE 设置
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"
" 该文件包括vim和cscope的接口
" 有常用映射
"
" USAGE: 
" -- vim 7.3:   将文件考入~/.vim/plugin
"
" NOTE: 
" 本文件的映射使用了多个键。
" 如果觉得延时设置不合理，例如:命令还没有输完，vim的就开始处理，修改延时.
"
"
"
" 彭鹏                  yougukepp@gmail.com             2012/9/13 
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 保护该脚本不被多次加载
if exists("g:loaded_cscope")
    finish
endif
let g:loaded_cscope = 1

" 测试VIM在编译时是否加入--enable-cscope,
" 如果没有,是时候从新编译(或升级)VIM了(^_^)
if has("cscope")

    " 在当前目录加入cscope数据库
    if filereadable("cscope.out")
        cs add cscope.out  
    " 当前目录没有库，则从环境变量中找
    elseif $CSCOPE_DB != ""
        cs add $CSCOPE_DB
    endif

    " 当数据库加入，显示提示消息
    set cscopeverbose  

    """"""""""""" 我的cscope/vim映射
    "
    " 下面的简写对应cscope的搜索类型:
    "
    " s: 查找本 C 符号
    " g: 查找本定义
    " d: 查找本函数调用的函数
    " c: 查找调用本函数的函数
    " t: 查找本字符串
    " e: 查找本egrep模式
    " f: 查找本文件
    " i: 查找包含本文件的文件
    "
    " 下面有三套映射:
    " 1、在当前窗口中显示查询和跳转结果
    " 2、水平分割窗口,跳转目的地在新窗口中显示结果
    " 3、垂直分割窗口,跳转目的地在新窗口中显示结果
    "
    " 所有的映射以CTRL-\开头,在 VIM7.3中没有冲突。
    " 映射中使用<cword>代表光标处单词，
    " <cfile>代表光标处文件全名:t选项表示不包括路径的文件名。


    " 首先输入CTRL-\然后依据上文命令缩写执行命令，查询的内容由光标指示
    " 结果显示在当前窗口
    nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>f :cs find f <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>i :cs find i <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>


    " 首先输入CTRL-\然后输入a，最后依据上文命令缩写执行命令，查询的内容由光标指示
    " 水平分割窗口,跳转目的地在新窗口中显示结果
    nmap <C-\>hs :scs find s <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>hg :scs find g <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>hc :scs find c <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>ht :scs find t <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>he :scs find e <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>hf :scs find f <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>hi :scs find i <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>hd :scs find d <C-R>=expand("<cword>")<CR><CR>


    " 首先输入CTRL-\然后输入v，最后依据上文命令缩写执行命令，查询的内容由光标指示
    " 垂直分割窗口,跳转目的地在新窗口中显示结果
    nmap <C-\>ls :vert scs find s <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>lg :vert scs find g <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>lc :vert scs find c <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>lt :vert scs find t <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>le :vert scs find e <C-R>=expand("<cword>")<CR><CR>
    nmap <C-\>lf :vert scs find f <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>li :vert scs find i <C-R>=expand("<cfile>:t")<CR><CR>
    nmap <C-\>ld :vert scs find d <C-R>=expand("<cword>")<CR><CR>

endif
