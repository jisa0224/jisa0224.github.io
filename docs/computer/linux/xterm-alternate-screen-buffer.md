# XTerm 的 Alternate Screen Buffer

在虛擬終端機(pty)使用 Vim 的時候會注意到一個特別的現象：

1. 原本的終端機可以藉由捲軸來看以前的內容
2. 進入 Vim 後，捲軸不見了
3. 退出 Vim 後，捲軸出現，並且可以看到以前的內容

代表說 Vim 並沒有消除/覆蓋掉以前的內容。

這是透過 `xterm` 的 **Alternative Screen Buffer** 功能提供的

根據[這份文件](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-The-Alternate-Screen-Buffer)

> XTerm maintains two screen buffers. The **Normal Screen Buffer** allows you to scroll back to view saved lines of output up to the maximum set by the saveLines resource. The **Alternate Screen Buffer** is exactly as large as the display, contains no additional saved lines. When the Alternate Screen Buffer is active, you cannot scroll back to view saved lines. XTerm provides control sequences and menu entries for switching between the two.
>
> Most full-screen applications use `terminfo` or `termcap` to obtain strings used to start/stop full-screen mode, i.e., `smcup` and `rmcup` for terminfo, or the corresponding `ti` and `te` for termcap. The titeInhibit resource removes the ti and te strings from the TERMCAP string which is set in the environment for some platforms. That is not done when xterm is built with terminfo libraries because terminfo does not provide the whole text of the termcap data in one piece.  It would not work for terminfo anyway, since terminfo data is not passed in environment variables; setting an environment variable in this manner would have no effect on the application's ability to switch between Normal and Alternate Screen buffers. Instead, the newer private mode controls (such as 1 0 4 9 ) for switching between Normal and Alternate Screen buffers simply disable the switching. They add other features such as clearing the display for the same reason: to make the details of switching independent of the application that requests the switch.

這是只有在 `xterm` 上才有的，用 `Ctrl-Alt` 加數字的 VT 是沒有的（因為它是 VT100 的樣子）。

只要在 shell 裡執行 `tput smcup` 就可以進到 Alternative Screen Buffer，然後再執行 `tput rmcup` 就會回到剛剛的環境，如果把輸出弄亂了，可以執行 `reset` 回覆到最原始的狀態。

如果要查看 `smcup` 和 `rmcup` 的控制碼，可以用 `infocmp xterm` 來看（不加參數就是看現在的設定）。

參考資料：[terminal - How curses preserves screen contents? - Stack Overflow](https://stackoverflow.com/questions/39188508/how-curses-preserves-screen-contents)
 
