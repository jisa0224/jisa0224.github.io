# 強制 Linux 下 Google Chrome 使用繁中作為 UI 語言(未完成)

Linux 下的 Google Chrome 會自動根據 `LANG` 來調整語言

``` shell
$ echo $LANG
en_US.UTF-8
```

要使按下開始選單用繁中開啟很簡單  
修改 `/usr/share/applications/google-chrome.desktop` (需要 `sudo`)

``` shell
# Exec=/usr/bin/google-chrome-stable %U
Exec=sh -c "LANG=zh_TW.UTF-8 /usr/bin/google-chrome-stable %U"
 
# Exec=/usr/bin/google-chrome-stable
Exec=sh -c "LANG=zh_TW.UTF-8 /usr/bin/google-chrome-stable"
 
# Exec=/usr/bin/google-chrome-stable --incognito
Exec=sh -c "LANG=zh_TW.UTF-8 /usr/bin/google-chrome-stable --incognito"
```

分別把註解的部份(原本的)修改成各自下面的版本即可，我留著原本的把它註解掉作為備份。  
用 `sh` 或 `bash` 都可以，因為它是 `bash` 的符號連結，在要執行的程式前修改環境變數可以讓這個修改只在這次生效。

然後必須到開始功能表右鍵\>「Edit Menus」\>「Revert」(選單會恢復初始狀態)，這樣開始功能表才不會去用本地的 `.desktop` 檔。

此方法也適用 Chromium。

如果不使用 `sh -c` 的方式來開，而直接 `LANG=zh_TW.UTF-8 google-hrome-stable`，其實也可以換語言，但會因為不明原因無法在 Preferred Applications 裡將它設為預設瀏覽器。

參考網站：[Change Google Chrome language? - Ask Ubuntu](https://askubuntu.com/questions/202670/change-google-chrome-language/484302#484302)

TBD: 圖形界面(Gnome, KDE)的開始功能表，啟動程式的方式是用 shell 執行命令，還是 fork-and-exec?