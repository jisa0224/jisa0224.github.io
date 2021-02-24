# Google Chrome (電腦版) 使用技巧

以下適用於電腦版 Google Chrome 和 Chromium。

## 禁用 Tab Hover Cards

設定 Chrome Flags 的 Tab Hover Cards 為 Disabled 後重新啟動 Chrome。

> Tab Hover Cards
>
> chrome://flags/#tab-hover-cards
>
> Enables a popup containing tab information to be visible when hovering over a tab. 
> This will replace tooltips for tabs. – Mac, Windows, Linux, Chrome OS

參考資料：[[Tip] Disable New Tab Hover Pop-ups and Restore Classic Tab Tooltips in Google Chrome - AskVG](https://www.askvg.com/tip-disable-new-tab-hover-pop-ups-and-restore-classic-tab-tooltips-in-google-chrome/)

## 顯示完整網址

Chrome 某一版更新後，預設隱藏了網址列中的 `http://`、`https://` 和 `www.`。

設定 Chrome Flags 的 Context menu show full URLs 為 Enabled 後重新啟動 Chrome，然後在網址列勾選「Always show full URLs」。

> Context menu show full URLs
>
> chrome://flags/#omnibox-context-menu-show-full-urls
>
> Provides an omnibox context menu option that prevents URL elisions. – Mac, Windows, Linux, Chrome OS

參考資料：[How to Always Show Full URLs in Google Chrome](https://www.howtogeek.com/677848/how-to-always-show-full-urls-in-google-chrome/)

備註：Google Chrome 88 刪除了這個選項，直接在網址列勾選「Always show full URLs」就可以了。

## 開啟內建 QR Code 產生器

設定 Chrome Flags 的 Enable sharing page via QR Code 為 Enabled 後重新啟動 Chrome。

> Enable sharing page via QR Code
>
> chrome://flags/#sharing-qr-code-generator
>
> Enables right-click UI to share the page's URL via a generated QR Code. – Mac, Windows, Linux, Chrome OS

參考資料：[Chrome 內建QR Code 產生器 功能，教你免外掛也能製作條碼 - 瘋先生](https://mrmad.com.tw/chrome-qr-code)

備註：Google Chrome 88 預設開啟此功能。

# 避免在網址列輸入 "google <SPACE>" 後變成在 Google 搜尋

到 設定 > 搜尋引擎 > 管理搜尋引擎，會出現一條或數條 "搜尋引擎、關鍵字、查詢網址" 的項目，找到關鍵字為 "google" 的項目，把關鍵字改為 "google.com" 或其它比較少用到的字串即可。

在網址列輸入「關鍵字」後按下空格或 Tab 鍵，就會變成在那個關鍵字的搜尋引擎搜尋。

參考資料：[How to disable ["google" + <SPACE> = search autocomplete] in address bar : chrome](https://www.reddit.com/r/chrome/comments/3lt0vw/how_to_disable_google_space_search_autocomplete/)