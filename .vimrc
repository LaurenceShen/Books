set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8

set nocompatible
set number
set hlsearch
set ruler
set cursorline
set background=dark
set showmode
set showmatch

set expandtab
set backspace=2
set shiftwidth=4
set tabstop=4
set softtabstop=4

set autoindent
set smartindent

syntax on

"Highlight extra whitespace
highlight ExtraWhitespace ctermbg=darkgreen guibg=lightgreen
match ExtraWhitespace /\s\+$/

"highlight OverLength ctermbg=darkgreen
"match OverLength /\%11v.+/
if exists('+colorcolumn')
    set colorcolumn=120
else
    au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>120v.\+', -1)
endif

"autocmd FileType python set tw=80 cc=+1
autocmd FileType make set noexpandtab

nmap <bslash>p :set paste!<CR>
nmap <bslash>x mzHmx:silent! :%s/[ \t][ \t]*$//g<CR>`xzt`z
nmap <bslash>t :Tlist<CR>

autocmd FileType c nmap <F9> <ESC>\x:w<CR>:!gcc -O2 -Wall -std=c99 % -o %<<CR>
autocmd FileType c nmap <F11> <ESC>\x:w<CR>:!./%<<CR>
autocmd FileType c nmap <F12> <ESC>\x:w<CR>:!gcc -O2 -Wall -std=c99 % -o %< && ./%<<CR>
autocmd FileType c imap <F9> <ESC>\x:w<CR>:!gcc -O2 -Wall -std=c99 % -o %<<CR>
autocmd FileType c imap <F11> <ESC>\x:w<CR>:!./%<<CR>
autocmd FileType c imap <F12> <ESC>\x:w<CR>:!gcc -O2 -Wall -std=c99 % -o %< && ./%<<CR>

autocmd FileType cpp nmap <F9> <ESC>\x:w<CR>:!g++ -O2 -Wall -std=c++11 % -o %<<CR>
autocmd FileType cpp nmap <F11> <ESC>\x:w<CR>:!./%<<CR>
autocmd FileType cpp nmap <F12> <ESC>\x:w<CR>:!g++ -O2 -Wall -std=c++11 % -o %< && ./%<<CR>
autocmd FileType cpp imap <F9> <ESC>\x:w<CR>:!g++ -O2 -Wall -std=c++11 % -o %<<CR>
autocmd FileType cpp imap <F11> <ESC>\x:w<CR>:!./%<<CR>
autocmd FileType cpp imap <F12> <ESC>\x:w<CR>:!g++ -O2 -Wall -std=c++11 % -o %< && ./%<<CR>

autocmd FileType python nmap <F11> <ESC>\x:w<CR>:!./%<CR>
autocmd FileType python nmap <F12> <ESC>\x:w<CR>:!./%<CR>
autocmd FileType python imap <F11> <ESC>\x:w<CR>:!./%<CR>
autocmd FileType python imap <F12> <ESC>\x:w<CR>:!./%<CR>

autocmd FileType tex nmap <F11> <ESC>\x:w<CR>:!gnome-open %<.pdf<CR><CR>
autocmd FileType tex nmap <F12> <ESC>\x:w<CR>:!xelatex %<CR>
autocmd FileType tex imap <F11> <ESC>\x:w<CR>:!gnome-open %<.pdf<CR><CR>
autocmd FileType tex imap <F12> <ESC>\x:w<CR>:!xelatex %<CR>

