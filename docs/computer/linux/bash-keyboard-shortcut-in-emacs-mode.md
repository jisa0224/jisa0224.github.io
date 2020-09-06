# Bash 在 Emacs 模式下的快速鍵和其衝突列表

## 終端機命令

<table style="width: 100%;" border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="55%">功能</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-l</td>
<td>清除螢幕，並將目前輸入中的指令顯示在最上面一行。</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-d</td>
<td>關閉 shell，傳送 EOF (End-of-file) 給 bash，等同於輸入 exit 指令。</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-s</td>
<td>暫停螢幕輸出，與 Ctrl-q 為一組。</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-q</td>
<td>繼續螢幕輸出，與 Ctrl-s 為一組。</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-c</td>
<td>對 process 發出中斷請求 (SIGINT 訊號)，大部份 process 會接受，但有些會忽略。</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-z</td>
<td>將前台任務丟到後台中並暫停。</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

## 編輯類

### 游標移動

<table style="width: 100%;" border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="15%">方向</td>
<td align="center" width="15%">動作</td>
<td align="center" width="25%">範圍/位置</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-b</td>
<td align="center">⇦ 向左</td>
<td align="center">移動</td>
<td>一個字元</td>
<td>tmux send-prefix</td>
</tr>
<tr>
<td align="center">Ctrl-f</td>
<td align="center">⇨ 向右</td>
<td align="center">移動</td>
<td>一個字元</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-b</td>
<td align="center">⇦ 向左</td>
<td align="center">移動</td>
<td>到詞首</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-f</td>
<td align="center">⇨ 向右</td>
<td align="center">移動</td>
<td>到詞尾</td>
<td>MATE Terminal menubar</td>
</tr>
<tr>
<td align="center">Ctrl-a</td>
<td align="center">⇤ 向左</td>
<td align="center">移動</td>
<td>到行首</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-e</td>
<td align="center">⇥ 向右</td>
<td align="center">移動</td>
<td>到行尾</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-x-x</td>
<td colspan="4">⇤⇥ 在行首和當前游標處移動</td>
</tr>
</tbody>
</table>

### 刪除(剪下)與貼上

<table style="width: 100%;" border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="15%">方向</td>
<td align="center" width="15%">動作</td>
<td align="center" width="25%">範圍/位置</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-h</td>
<td align="center">⇦ 向左</td>
<td align="center">刪除</td>
<td>一個字元</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-d</td>
<td align="center">⇨ 向右</td>
<td align="center">刪除</td>
<td>一個字元</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-w</td>
<td align="center">⇦ 向左</td>
<td align="center">刪除</td>
<td>到詞首</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-d</td>
<td align="center">⇨ 向右</td>
<td align="center">刪除</td>
<td>到詞尾 </td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-u</td>
<td align="center">⇦ 向左</td>
<td align="center">刪除</td>
<td>到行首</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-k</td>
<td align="center">⇨ 向右</td>
<td align="center">刪除</td>
<td>到行尾</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-y</td>
<td align="center">⇨ 向右</td>
<td align="center">貼上</td>
<td>上一次刪除的內容</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

### 交換與大小寫轉換

<table style="width: 100%;" border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="15%">方向</td>
<td align="center" width="15%">動作</td>
<td align="center" width="25%">範圍/位置</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-t</td>
<td align="center">⇦ 向左</td>
<td align="center">交換</td>
<td>一個字元</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-t</td>
<td align="center">⇦ 向左</td>
<td align="center">交換</td>
<td>一個詞</td>
<td>MATE Terminal menubar</td>
</tr>
<tr>
<td align="center">Alt-c</td>
<td align="center">⇨ 向右</td>
<td align="center">轉換成大寫</td>
<td>一個字元</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-u</td>
<td align="center">⇨ 向右</td>
<td align="center">轉換成大寫</td>
<td>到詞尾</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-l</td>
<td align="center">⇨ 向右</td>
<td align="center">轉換成小寫</td>
<td>到詞尾</td>
<td>我設定的鎖定螢幕快速鍵</td>
</tr>
</tbody>
</table>

### 命令歷史操作

<table border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="15%">方向</td>
<td align="center" width="15%">動作</td>
<td align="center" width="25%">範圍/位置</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-p</td>
<td align="center">⇧ 向前</td>
<td align="center">讀取歷史</td>
<td>上一條命令</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-n</td>
<td align="center">⇩ 向後</td>
<td align="center">讀取歷史</td>
<td>下一條命令</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-&gt;<br />
(Alt-Shift-.)</td>
<td align="center">⇩ 向後</td>
<td align="center">讀取歷史</td>
<td>當前命令</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-r</td>
<td align="center">⇧ 向前</td>
<td align="center">搜索歷史</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-j</td>
<td align="center">結束</td>
<td align="center">搜索歷史</td>
<td>並顯示搜尋結果</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Ctrl-g</td>
<td align="center">結束</td>
<td align="center">搜索歷史</td>
<td>並回復搜尋前的命令</td>
<td>&nbsp;</td>
</tr>
<tr>
<td align="center">Alt-.</td>
<td colspan="4">使用上一條命令的最後一個參數</td>
</tr>
</tbody>
</table>

### 其它

<table border="1">
<tbody>
<tr>
<td align="center" width="17.5%">快速鍵</td>
<td align="center" width="55%">功能</td>
<td align="center" width="27.5%">衝突</td>
</tr>
<tr>
<td align="center">Ctrl-_<br />
(Ctrl-Shift--)</td>
<td>回復上一個編輯操作</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

## 補充說明

1.  向左刪除**不包含**游標下的字元(即自游標左方的字元開始刪除)，向右刪除**包含**游標下的字元。  
    (範例： 123`4`567 往左刪為 12`4`567，往右刪為 123`5`67。)
2.  `Ctrl-y` 貼上的內容**只限**使用 `Ctrl-w`、`Alt-d`、`Ctrl-u`、`Ctrl-k` 刪除的內容，重複按下 `Ctrl-y` **並不會**貼上更久之前刪除的內容，只會重複上一次的內容。
3.  `Ctrl-y` 貼上的內容會插入到游標下的字元和游標左方的字元中間  
    (範例：在 123`4`567 中插入 abc，其中 4 為游標所在地，結果為 123abc`4`567。)
4.  其實我認為可以把 123`4`567 看成 123|4567，兩者應該是等價的。)

## 參考資料

[让你提升命令行效率的 Bash 快捷键 \[完整版\] ·
LinuxTOY](https://linuxtoy.org/archives/bash-shortcuts.html)  
[The Best Keyboard Shortcuts for Bash (aka the Linux and macOS Terminal)](https://www.howtogeek.com/howto/ubuntu/keyboard-shortcuts-for-bash-command-shell-for-ubuntu-debian-suse-redhat-linux-etc/)  
[Bash Shortcuts For Maximum Productivity](http://www.skorks.com/2009/09/bash-shortcuts-for-maximum-productivity/)  
[Readline keyboard shortcuts for bash, bc, ftp, gnuplot, gpg, ksh, mysql, psql, python, smbclient, xmllint and zsh](http://www.bigsmoke.us/readline/shortcuts)  
[HTML Div Table Generator](http://divtable.com/generator/)