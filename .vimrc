set nocompatible              " 不要受限于Vi

" Vundle插件开始
filetype off                  " required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/Vundle.vim'
" 自动补全
Plugin 'Valloric/YouCompleteMe'
    let g:ycm_autoclose_preview_window_after_completion=1
    let g:ycm_key_list_select_completion = ['<c-n>', '<Down>']
    let g:ycm_key_list_previous_completion = ['<c-p>', '<Up>']
" 高级状态栏
Bundle 'Lokaltog/vim-powerline'
    set laststatus=2
" molokai主题
Bundle 'tomasr/molokai'
" Lisp
Bundle 'kovisoft/slimv'
    let g:slimv_swank_cmd='! xterm -e mit-scheme --load /home/maxiee/.vim/bundle/slimv/slime/contrib/swank-mit-scheme.scm &'
    let g:lisp_rainbow=1
    let g:swank_log=1
" Javacomplete
Bundle 'PeterCxy/javacomplete'
    autocmd Filetype java set omnifunc=javacomplete#Complete
    autocmd Filetype java set completefunc=javacomplete#CompleteParamsInf

" UltiSnips
Plugin 'SirVer/ultisnips'   " Track the engine.
Plugin 'honza/vim-snippets' " Snippets are separated from the engine. 
    " Trigger configuration. Do not use <tab> YouCompleteMe.
    let g:UltiSnipsExpandTrigger="<tab>"
    let g:UltiSnipsJumpForwardTrigger="<c-k>"
    let g:UltiSnipsJumpBackwardTrigger="<c-j>"
    " If you want :UltiSnipsEdit to split your window.
    let g:UltiSnipsEditSplit="vertical"
    let g:UltiSnipsSnippetDirectories=["UltiSnips","/home/maxiee/.vim/bundle/my-snippet"]


call vundle#end()            
filetype plugin indent on    
" Vundle结束

set cindent "使用C语言缩进
set clipboard+=unnamed "共享剪贴板
set modeline "通过代码中的注释设置Vim选项
set tabstop=4 expandtab shiftwidth=4 softtabstop=4 " Python
set ruler "显示行号列号
set showcmd "显示输入的命令

filetype plugin indent on "根据文件类型智能载入插件、缩进
syntax on "高亮

set nu              " line number
"set linespace=6     " line space

colorscheme molokai
set guifont=Monospace\ 16 "设置字体

" for Android
if filereadable('AndroidManifest.xml')
    echo "Android Project Found!"
    let $ANDROID_JAR = '/opt/android-sdk/platforms/android-19/android.jar'
    let $JAVACOMPLETE_CACHE = '~/.jcc'
endif

