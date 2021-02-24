# Adobe Flash Player 結束服務後繼續使用的方法

Adobe Flash Player 在 2020 年 12 月 31 日停止服務，但有些網頁仍然使用 Flash 開發。

## 使用內含 Flash 的網頁瀏覽器

不須再額外安裝 Flash，打開即用。

* [百分浏览器](https://www.centbrowser.cn/)  
  [免安裝版](https://www.gdaily.org/25308/centbrowser-flash-player)  
  中國軟體，有資訊安全顧慮者自行衡量是否使用。
* [Puffin Web Browser](https://www.puffin.com/android/puffin-web-browser/)
  只有 Android 有免費版，Windows 和 iOS 版都需要付費。

## Windows 10 IE 修復法（已無法使用）

Windows 10 的 Internet Explorer (IE) 內建 Adobe Flash Player AcitveX 附加元件。

原本是可以使用的，但在 2021 年 1 月的某天後，所有網站都無法使用，但該附加元件還在。

修復方法如下：

在 `C:\Windows\System32\Macromed\Flash` 和 `C:\Windows\SysWOW64\Macromed\Flash` 建立一個檔案 `mms.cfg`，內容為：

```
EnableAllowList=1
AllowListRootMovieOnly=1
AllowListUrlPattern=<網址一>
AllowListUrlPattern=<網址二>
AllowListUrlPattern=<網址三>
SilentAutoUpdateEnable=0
AutoUpdateDisable=1
EOLUninstallDisable=1
```

網址的部份數量無限制，舉例來說，常被拿來測試 Flash 的網站就這樣加入 `AllowListUrlPattern=http://ultrasounds.com/`。

這個方法對 Edge 無效。

未來 Microsoft 可能會移除 Windows 10 裡的 IE。

2021/2/24 確認 Adobe Flash Player AcitveX 附加元件 已被移除（`C:\Windows\{System32,SysWOW64}\Macromed` 全空），此方法失效。

## 參考資料

[Flash救援包，修復2021後Flash Player無法使用 - GDaily](https://www.gdaily.org/25283/flash-player-fix)