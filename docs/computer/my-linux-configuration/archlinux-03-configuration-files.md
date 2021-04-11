# Arch Linux (三) 設定檔

這裡放置一些太長沒辦法放在主要文章裡的設定檔。

## ~/.envars

``` shell
# 
# ~/.envars: Environment Variables
#
# Use $HOME instead of ~ in this file
#
# for Bash: add `[[ -f ~/.envars ]] && . ~/.envars` in ~/.bashrc
# for KDE Plasma: execute `ln -s ../../../.envars ~/.config/plasma-workspace/env/envars.sh`
#                 ref: <https://userbase.kde.org/Session_Environment_Variables>
# <https://wiki.archlinux.org/index.php/XDG_Base_Directory>
#

# Default programs
export EDITOR="nvim"
export PAGER="less"

# Location of configuration and history files
export LESSHISTFILE="/dev/null"                                           # disable less history (default: ~/.lesshst)
export IPYTHONDIR="${XDG_CONFIG_HOME:-$HOME/.config}/ipython"             # change IPython configuration files location (default: ~/.ipython)
export JUPYTER_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/jupyter"     # change Jupyter configuration files location (default: ~/.jupyter)

# Fcitx 5 (Input Method Engine)
export GTK_IM_MODULE="fcitx"
export QT_IM_MODULE="fcitx"
export XMODIFIERS="@im=fcitx"
export SDL_IM_MODULE="fcitx"

# OpenJDK (Java)
export _JAVA_OPTIONS="-Dawt.useSystemAAFontSettings=on"

# The following doesn't work
#export GTK2_RC_FILES="${XDG_CONFIG_HOME:-$HOME/.config}/gtk-2.0/gtkrc"    # change GTK 2 configuration files location (default: ~/.gtkrc-2.0)
#export _JAVA_OPTIONS="-Djava.util.prefs.userRoot='${XDG_CONFIG_HOME:-$HOME/.config}/java'"    # change Java configuration files location (default: ~/.java)
```

## ~/.bash_profile

``` shell
#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc
```

## ~/.bashrc

``` shell
#
# ~/.bashrc
#

# Clear Bash history every boot (`$HOME/.cache` is mouted as tmpfs)
HISTFILE="$HOME/.cache/bash_history"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Load environment variables
[[ -f ~/.envars ]] && . ~/.envars

# Command line prompt (PS1)
if [[ ${EUID} == 0 ]]; then
    # root
    PS1='\[\033[01;31m\]\h\[\033[01;34m\] \W \$\[\033[00m\] '
else
    # non-root
    PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
fi

# Command alias
alias more='less'
alias nv='nvim'
alias ls='ls --color=auto'
alias ll='ls --color=auto -lh'
alias lld='ls --color=auto -ldh'
alias la='ls --color=auto -a'
alias lla='ls --color=auto -alh'
alias rm='rm -i'                    # confirm before delete something
alias cp='cp -i'                    # confirm before overwriting something
alias du='du -h'                    # human-readable sizes
alias free='free -h'                # human-readable sizes
alias grep='grep --color=auto'      # colored output
alias egrep='egrep --color=auto'    # colored output
alias fgrep='fgrep --color=auto'    # colored output
alias tree='tree -C'                # colored output
alias diff='diff --color=auto'      # colored output
alias ip='ip -color=auto'           # colored output
alias bc='bc -l'                    # show decimals (equal to `scale=20`)

df() {
	# sort without header: https://unix.stackexchange.com/questions/11856/sort-but-keep-header-line-at-the-top/71949#71949
	# sort by ASCII: https://stackoverflow.com/questions/5296428/how-to-sort-a-text-file-according-to-character-code-or-ascii-code-value/5296453#5296453
	# `command` suppress shell function lookup (so it will not cause infinite loop)
	command df -hT "$@" | awk 'NR == 1; NR > 1 {print $0 | "LC_COLLATE=C sort"}'
}

man() {
	# Enable colored man using less
	# https://wiki.archlinux.org/index.php/Color_output_in_console#man
    LESS_TERMCAP_md=$'\e[01;31m' \
    LESS_TERMCAP_me=$'\e[0m' \
    LESS_TERMCAP_se=$'\e[0m' \
    LESS_TERMCAP_so=$'\e[01;44;33m' \
    LESS_TERMCAP_ue=$'\e[0m' \
    LESS_TERMCAP_us=$'\e[01;32m' \
    command man "$@"
}
```

## ~/Desktop/root.desktop

``` 
[Desktop Entry]
Name=Root
Name[zh_TW]=根目錄
Type=Link
URL[$e]=file:/
Icon=drive-harddisk-root
```

## ~/Desktop/home.desktop

``` 
[Desktop Entry]
Name=Home
Name[zh_TW]=家目錄
Type=Link
URL[$e]=file:$HOME
Icon=user-home
```

## ~/Desktop/trash.desktop

``` 
[Desktop Entry]
Name=Trash
Name[zh_TW]=垃圾桶
Type=Link
URL[$e]=trash:/
Icon=user-trash-full
EmptyIcon=user-trash
```

## ~/.local/share/templates/empty-file.desktop

``` 
[Desktop Entry]
Name=Empty File...
Name[zh_TW]=空白檔案...
Comment=Enter filename:
Comment[zh_TW]=輸入檔名：
Type=Link
URL=.source/empty-file.txt
Icon=none
```

## ~/.config/fontconfig/fonts.conf

``` XML
<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
<!-- 
    設定目標：
        sans-serif -> Noto Sans CJK
        serif      -> Noto Serif CJK
        monospace  -> Noto Mono      -> Noto Sans CJK     (注意是 Noto Mono 而不是 Noto Sans Mono，後者是無襯線字型而不是等寬字型)
        Noto Sans  -> Noto Sans CJK
        Noto Serif -> Noto Serif CJK
        Noto Mono  -> Noto Sans CJK
    ('Noto *' 不包含 CJK，所以需要 'Noto * CJK' 作為 fallback)

    fontconfig 的處理順序：
    1.  需要字型的程式送出 pattern 給 fontconfig 程式庫
    2.  將 /etc/fonts/fonts.conf 設定的規則應用到 pattern 上 (font matching, match/test/edit)
        /etc/fonts/fonts.conf 會 include /etc/fonts/fonts.d/*，並按照以下順序執行
        00-09: Font directories
        10-19: system rendering defaults (AA, etc)
        20-29: font rendering options
        30-39: family substitution
        40-49: generic identification, map family->generic    (40-48 會為一些已知的字型加上 sans-serif/serif/monospace 的 fallback，如果是未知的字型，49 會加上 sans-serif 的 fallback)
        50-59: alternate config file loading                  (這個檔案就是 50 include 的)
        60-69: generic aliases, map generic->family           (52-69 會在最初 pattern 和 generic 之間加入字型，越先加入的會在越前面，微軟正黑體等字型就是在這裡加入的)
        70-79: select font (adjust which fonts are available) (這個檔案的原版 70-noto-cjk.conf 就在這，但因為它加入的字型會在 50-69 的後面，所以如果 50-69 裡加入的字型存在的話，70-noto-cjk.conf 加入的字型永遠不會被用到！)
        80-89: match target="scan" (modify scanned patterns)
        90-99: font synthesis
        具體過程參考 `FC_DEBUG=4 fc-match '<font family name>'
    3.  為 pattern 添加一些預設的 element
    4.  對「所有字型」比對 pattern，每個字型會得到一個分數
    5.  將不支援 Unicode 的字型的分數加上一個很大的值
    6.  依照分數從低到高排列，分數最低的最優先，如果該字型沒有某個字，則往後 fallback (`fc-match -s` 看到的就是這個順序)

    參考資料：
        [fonts-conf](https://www.freedesktop.org/software/fontconfig/fontconfig-user.html)
        [Linux fontconfig 的字体匹配机制 - 双猫CC](https://catcat.cc/post/2020-10-31/)
        [fc-match 執行檔的程式碼](https://github.com/freedesktop/fontconfig/blob/master/fc-match/fc-match.c)
        [fontconfig 程式庫中負責 font matching 的程式碼](https://github.com/freedesktop/fontconfig/blob/master/src/fcmatch.c)
-->
<fontconfig>
 <!-- 如果想用其它字型當作 sans-serif/serif/monospace 的預設字型就修改這裡 -->
 <!--
    <alias binding="strong">
        <family>sans-serif</family>
        <prefer>
            <family>Noto Sans</family>
        </prefer>
    </alias>
    <alias binding="strong">
        <family>serif</family>
        <prefer>
            <family>Noto Serif</family>
        </prefer>
    </alias>
    <alias binding="strong">
        <family>monospace</family>
        <prefer>
            <family>DejaVu Sans Mono</family>
            <family>Source Han Mono TC</family>
        </prefer>
    </alias>
    -->
 <!-- 以下修改自 /etc/fonts/conf.avail/70-noto-cjk.conf -->
 <match target="pattern">
  <test name="lang">
   <string>ja</string>
  </test>
  <test name="family">
   <string>serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Serif CJK JP</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>ko</string>
  </test>
  <test name="family">
   <string>serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Serif CJK KR</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-cn</string>
  </test>
  <test name="family">
   <string>serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Serif CJK SC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-tw</string>
  </test>
  <test name="family">
   <string>serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Serif CJK TC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-hk</string>
  </test>
  <test name="family">
   <string>serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Serif CJK HK</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>ja</string>
  </test>
  <test name="family">
   <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Sans CJK JP</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>ko</string>
  </test>
  <test name="family">
   <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Sans CJK KR</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-cn</string>
  </test>
  <test name="family">
   <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Sans CJK SC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-tw</string>
  </test>
  <test name="family">
   <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Sans CJK TC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-hk</string>
  </test>
  <test name="family">
   <string>sans-serif</string>
  </test>
  <edit name="family" mode="prepend">
   <string>Noto Sans CJK HK</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>ja</string>
  </test>
  <test name="family">
   <string>monospace</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
   <string>Noto Mono</string>
   <string>Noto Sans CJK JP</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>ko</string>
  </test>
  <test name="family">
   <string>monospace</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
   <string>Noto Mono</string>
   <string>Noto Sans CJK KR</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-cn</string>
  </test>
  <test name="family">
   <string>monospace</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
   <string>Noto Mono</string>
   <string>Noto Sans CJK SC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-tw</string>
  </test>
  <test name="family">
   <string>monospace</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
   <!-- 必須加上 binding="strong"，不然 Noto Mono 的順序會低於 Noto Sans CJK (因為支援 Unicode 的字型比不支援的更 match) -->
   <string>Noto Mono</string>
   <!-- 原本是 Noto Sans Mono，改成 Noto Mono 後加上 Noto Sans CJK 處理 CJK 部份 -->
   <string>Noto Sans CJK TC</string>
  </edit>
 </match>
 <match target="pattern">
  <test name="lang">
   <string>zh-hk</string>
  </test>
  <test name="family">
   <string>monospace</string>
  </test>
  <edit name="family" mode="prepend" binding="strong">
   <string>Noto Mono</string>
   <string>Noto Sans CJK HK</string>
  </edit>
 </match>
 <dir>~/.fonts</dir>
</fontconfig>
```

## ~/.config/nvim/init.vim

``` 
" NeoVim init
" 安裝 Neovim 後，依照 https://github.com/junegunn/vim-plug 的說明安裝 vim-plug，之後將此文件複製到 ~/.config/nvim/init.vim，最後在 Neovim 中 :PlugUpdate 即可

" ========================================================================
" 編輯環境設定
" ========================================================================
set hidden
set confirm
set number
set nowrap
set listchars=eol:$,tab:>-,trail:-
set noshowmode

set ignorecase
set smartcase

let mapleader=";"

set cursorline
highlight CursorLine cterm=none ctermbg=236 ctermfg=none

set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
autocmd FileType make,sh :set noexpandtab

autocmd FileType c,cpp :set cindent


" ========================================================================
" 按鍵設定
" ========================================================================
" wrap 的設定
nnoremap j gj
nnoremap k gk
nnoremap 0 g0
nnoremap $ g$

" map insert newline without enter insert mode
nnoremap <CR> o<Esc>0D
autocmd FileType qf unmap <CR>

" map <Esc> to exit terminal-mode
tnoremap <Esc> <C-\><C-n>

" 注意 <C-J> 和 <C-K> 會使 NerdTree 裡的快速鍵無法使用
nnoremap <C-J> <Esc>:bnext<CR>
nnoremap <C-K> <Esc>:bprevious<CR>
nnoremap <C-H> <Esc>:tabprevious<CR>
nnoremap <C-L> <Esc>:tabnext<CR>

" Allow saving of files as sudo when I forgot to start vim using sudo.
cnoremap w!! w !sudo tee % > /dev/null

" 單檔編譯與執行
autocmd FileType c,cpp noremap <F7> <Esc>:w<CR>:vsp +terminal\ gcc\ -std=c11\ -o\ ./%<\ ./%\ &&\ ./%<<CR>a
" 單檔執行
autocmd FileType c,cpp noremap <F8> <Esc>:w<CR>:vsp +terminal\ ./%<<CR>a


" ========================================================================
" Plug-in 載入(https://github.com/junegunn/vim-plug)
" ========================================================================
call plug#begin('~/.local/share/nvim/plugged')
Plug 'vim-airline/vim-airline'           " 狀態列
Plug 'vim-airline/vim-airline-themes'    " 狀態列主題
"Plug 'skywind3000/vim-quickui'
Plug 'easymotion/vim-easymotion'         " 快速移動
"Plug 'justinmk/vim-sneak'                " 雙字搜尋移動
"Plug 'ctrlpvim/ctrlp.vim'                " 模糊檔名搜尋
"Plug 'tpope/vim-surround'

"Plug 'neoclide/coc.nvim', {'do': './install.sh nightly'}    " 代碼補全
"Plug 'w0rp/ale'                          " 錯誤檢查
"Plug 'ludovicchabant/vim-gutentags'      " tag 管理
"Plug 'rhysd/vim-clang-format'            " 代碼格式化
"Plug 'majutsushi/tagbar'                 " 顯示函數、變數等列表
"Plug 'scrooloose/nerdtree'
"Plug 'scrooloose/nerdcommenter'

"echodoc
call plug#end()


" ========================================================================
" Plug-in 設定
" ========================================================================
" vim-airline and vim-airline-themes
let g:airline_theme='deus'
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail'

" coc.nvim
" Map <tab> to trigger completion and navigate to the next item: >
function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~ '\s'
endfunction

inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()

" Map <c-space> to trigger completion: >
inoremap <silent><expr> <c-space> coc#refresh()

" <CR> to confirm completion, use: >
inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<CR>"

" ale
let g:ale_sign_column_always = 1
let g:ale_echo_msg_format = '[%linter%] %code: %%s'
let g:ale_lint_on_text_changed = 'normal'
let g:ale_lint_on_insert_leave = 1
noremap <F5> <Esc>:ALEToggle<CR>

" vim-gutentags
" gutentags 搜索工程目录的标志，碰到这些文件/目录名就停止向上一级目录递归
let g:gutentags_project_root = ['.root', '.svn', '.git', '.hg', '.project']

" 所生成的数据文件的名称
let g:gutentags_ctags_tagfile = '.tags'

" 将自动生成的 tags 文件全部放入 ~/.cache/tags 目录中，避免污染工程目录
let s:vim_tags = expand('~/.cache/tags')
let g:gutentags_cache_dir = s:vim_tags

" 配置 ctags 的参数
let g:gutentags_ctags_extra_args = ['--kinds-all=*']

" 检测 ~/.cache/tags 不存在就新建
if !isdirectory(s:vim_tags)
   silent! call mkdir(s:vim_tags, 'p')
endif

" vim-clang-format
let g:clang_format#code_style = "google"
let g:clang_format#style_options = {
            \ "AccessModifierOffset": 0,
            \ "AlignAfterOpenBracket": "DontAlign",
            \ "AlignConsecutiveAssignments": "false",
            \ "AlignConsecutiveDeclarations": "false",
            \ "AlignEscapedNewlinesLeft": "true",
            \ "AlignOperands": "true",
            \ "AlignTrailingComments": "true",
            \ "AllowAllParametersOfDeclarationOnNextLine": "true",
            \ "AllowShortBlocksOnASingleLine": "true",
            \ "AllowShortFunctionsOnASingleLine": "All",
            \ "AllowShortIfStatementsOnASingleLine": "true",
            \ "AllowShortLoopsOnASingleLine": "true",
            \ "AlwaysBreakAfterDefinitionReturnType": "None",
            \ "AlwaysBreakAfterReturnType": "None",
            \ "AlwaysBreakBeforeMultilineStrings": "false",
            \ "BinPackArguments": "true",
            \ "BinPackParameters": "true",
            \ "BreakBeforeBinaryOperators": "None",
            \ "BreakBeforeBraces": "Attach",
            \ "BreakBeforeTernaryOperators": "true",
            \ "BreakConstructorInitializersBeforeComma": "false",
            \ "ColumnLimit": 0,
            \ "IndentWidth": 4,
            \ "IndentWrappedFunctionNames": "true",
            \ "NamespaceIndentation": "All",
            \ "ObjCBlockIndentWidth": 4,
            \ "ReflowComments": "false",
            \ "SortIncludes": "false",
            \ "SpaceBeforeParens": "Never",
            \ "SpacesBeforeTrailingComments": 4,
            \ "SpacesInContainerLiterals": "false",
            \ "DerivePointerAlignment": "false",
            \ "PointerAlignment": "Right",
            \ "TabWidth": 4}
autocmd FileType c,cpp,objc nnoremap <buffer><F3> :<C-u>ClangFormat<CR>
autocmd FileType c,cpp,objc vnoremap <buffer><F3> :ClangFormat<CR>

" TagBar
noremap <F4> :TagbarToggle<CR>
" 設定 ctags 對哪些代碼標示符生成標籤
let g:tagbar_type_c = {
    \ 'kinds' : [
         \ 'c:classes:0:1',
         \ 'd:macros:0:1',
         \ 'e:enumerators:0:0',
         \ 'f:functions:0:1',
         \ 'g:enumeration:0:1',
         \ 'l:local:0:1',
         \ 'm:members:0:1',
         \ 'n:namespaces:0:1',
         \ 'p:functions_prototypes:0:1',
         \ 's:structs:0:1',
         \ 't:typedefs:0:1',
         \ 'u:unions:0:1',
         \ 'v:global:0:1',
         \ 'x:external:0:1'
     \ ],
     \ 'sro'        : '::',
     \ 'kind2scope' : {
         \ 'g' : 'enum',
         \ 'n' : 'namespace',
         \ 'c' : 'class',
         \ 's' : 'struct',
         \ 'u' : 'union'
     \ },
     \ 'scope2kind' : {
         \ 'enum'      : 'g',
         \ 'namespace' : 'n',
         \ 'class'     : 'c',
         \ 'struct'    : 's',
         \ 'union'     : 'u'
     \ }
\ }
let g:tagbar_type_cpp = {
    \ 'kinds' : [
         \ 'c:classes:0:1',
         \ 'd:macros:0:1',
         \ 'e:enumerators:0:0',
         \ 'f:functions:0:1',
         \ 'g:enumeration:0:1',
         \ 'l:local:0:1',
         \ 'm:members:0:1',
         \ 'n:namespaces:0:1',
         \ 'p:functions_prototypes:0:1',
         \ 's:structs:0:1',
         \ 't:typedefs:0:1',
         \ 'u:unions:0:1',
         \ 'v:global:0:1',
         \ 'x:external:0:1'
     \ ],
     \ 'sro'        : '::',
     \ 'kind2scope' : {
         \ 'g' : 'enum',
         \ 'n' : 'namespace',
         \ 'c' : 'class',
         \ 's' : 'struct',
         \ 'u' : 'union'
     \ },
     \ 'scope2kind' : {
         \ 'enum'      : 'g',
         \ 'namespace' : 'n',
         \ 'class'     : 'c',
         \ 'struct'    : 's',
         \ 'union'     : 'u'
     \ }
\ }

" NERD
noremap <C-n> :NERDTreeToggle<CR>
" autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
let g:NERDSpaceDelims = 1               " Add spaces after comment delimiters by default
let g:NERDCompactSexyComs = 1           " Use compact syntax for prettified multi-line comments
let g:NERDCommentEmptyLines = 1         " Allow commenting and inverting empty lines (useful when commenting a region)
let g:NERDTrimTrailingWhitespace = 1    " Enable trimming of trailing whitespace when uncommenting
```

