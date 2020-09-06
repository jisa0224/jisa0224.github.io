# Vim 以 root 權限開啟、開啟後以 root 權限儲存以及強制寫入(:w!)的疑問

## 以 root 權限開啟

一般來說要編輯系統/系統程式的設定檔，會用 `sudo vim <FILE>` 的方式來編輯，但因為 `sudo` 的關係 Vim 不會去讀取我自己的 `~/.vimrc`，而是 root 的 `~/.vimrc`，這樣一來我就必須用沒有調整過的編輯環境去修改我的檔案，非常糟糕，如果是用 `sudo vim -u .vimrc <FILE>` 的話會因為 `$HOME` 變成 `/root` 的關係導致 plugin 無法使用，於是就想要有能夠以 root 權限開啟 Vim 的同時並能讀取我自己的 `~/.vimrc` 的方法。

解決方法就是執行

``` shell
sudo -e <FILE>
```

或是

``` shell
sudoedit <FILE>
```

註：此兩者為等價命令，`man sudo` 中寫了「當 `sudo` 是以 `sudoedit` 調用時，隱含了 `-e` 選項」，並且 `/usr/bin/sudoedit` 會以符號連結或硬連結的方式連結到 `/usr/bin/sudo`，程式依照命令列的第一個參數來判斷 (關於這個主題可參考\<TBD\>)

但如果直接這麼執行的話不一定會是用 Vim 來開啟，因為 `man sudo` 中寫到 `sudo -e` 調用的編輯器是依照環境變數 `SUDO_EDITOR`、`VISUAL` 及 `EDITOR` 來判斷，前項為空或找不到可執行檔就換下一項，如果都為空或找不到可執行檔，就會用 `/etc/sudoers` 中的 `editor` 欄位(`man sudoer` 建議使用)來判斷，如果還是為空或找不到可執行檔，就會調用 Vi。

如果想加在 `/etc/sudoers` 裡，在最後加入

```
Defaults editor = "/usr/bin/vim"
```

順帶一題，在我電腦上會調用 Elvis 這個長的很像 vi 的編輯器，原本我還一直以為它是 Vi，一直到我 `:version` 才發現，但我那三個環境變數和 `/etc/sudoers` 都為空，為什麼會是 Elvis？

因為

```
$ ls -l `which vi`
lrwxrwxrwx 1 root root 5 Dec 23  2017 /usr/bin/vi -> elvis
```

`sudo -e` 的運作原理看起來是這樣的：先複製目標檔案一份到暫存資料夾，編輯它，此時不需要 root 權限，可以使用我自己的 Vim 環境來編輯，如果內容有修改再複製回去取代原檔案，最後移除暫存的複製檔。(之所以說「看起來」是因為編輯前後的檔案 inode 不會變，而「取代(`mv`)」這動作卻會，真正的原理可能跟底下強制寫入那部份一樣。)

特別注意的是不能編輯符號連結指向的檔，不能編輯我有寫權限的資料夾中的檔案(root 除外)，如果最後無法取代回去，編輯過得檔案會留在暫存資料夾中。

最後，因為如果只是拿 Vim 來取代 less 或 more 當閱讀器的話，這個功能也很方便，因為如果沒有編輯的話不會動到原本的檔案，不會有不小心把原檔案弄壞的情況。

參考資料：  
[permissions - Start Vim as my user with root privileges - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/46699/start-vim-as-my-user-with-root-privileges/46724#46724)  
[sudo - How to set visudo to use a different editor than the default on Fedora? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/4408/how-to-set-visudo-to-use-a-different-editor-than-the-default-on-fedora/4409#4409)

## 開啟後以 root 權限儲存

有時候忘了用 `sudo` 開啟，或原本只想看看但後來想修改的時候，雖然說可以先以自己的權限另存新檔在別的地方，然後再用 root 權限複製回去取代掉(用 `sudo cp` 的話會擁有者會變成 root，`sudo mv` 不會)，但就是懶，想要直接存，此時可以在 Vim 內執行

```
:w !sudo tee %
```

此時會出現

```
W12: Warning: File "/test" has changed and the buffer was changed in Vim as well
See ":help W12" for more info.
[O]K, (L)oad File:
```

按 L (大小寫皆可)才會顯示出以儲存的內容，O 的話會顯示未儲存(但其實已經存了)

原理是這樣的：`:[range]w[rite] [++opt] !{cmd}` 會以本文件指定範圍內的內容為標準輸入傳給 `cmd` (就像 pipe 一樣)，此時的 `:w` 並不代表儲存，而 `tee` 會把從標準輸入得到的資料傳到標準輸出，同時存成檔案，檔名就是 `%`，在 Vim 中代表本文件的檔名，而前面加的 `sudo` 會使 `tee` 用 root 權限來存檔案，所以其實也是用取代的方式達成(不過 inode 還是不會變啊！為什麼？)

其實因為 `tee` 還會向標準輸出丟資料的關係，螢幕上會被文件內的內容給刷過，如果不要輸出在螢幕上可以在後面加 `> /dev/null`

可以在 `.vimrc` 中加入

```
" Allow saving of files as sudo when I forgot to start vim using sudo.
cmap w!! w !sudo tee % > /dev/null
```

以方便使用，只需要 `:w!!`

最後，其實

```
:w !sudo dd of=%
```

也是可以的，原理也差不多，而且不會輸出文件內容，只不過因為我先發現 tee 的版本，所以寫在前面而已。

參考資料：  
[unix - What are the dark corners of Vim your mom never told you about? - Stack Overflow](https://stackoverflow.com/questions/726894/what-are-the-dark-corners-of-vim-your-mom-never-told-you-about/726920#726920)  
[How does the vim "write with sudo" trick work? - Stack Overflow](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)

## 強制寫入(:w\!)的疑問

TBD

<https://unix.stackexchange.com/questions/58880/how-does-vim-steal-root-owned-files>
 
