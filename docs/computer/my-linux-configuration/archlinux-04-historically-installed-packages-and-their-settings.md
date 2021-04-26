# Arch Linux (四) 以前安裝過的軟體包及相關設定

## 應用程式

* 網路
    * 瀏覽器: google-chrome@A
        - Chromium 自 88 版開始，停止 Google 帳戶同步功能，所以只好改用 Google Chrome。
        - 使用久了之後會儲存大量的快取，"清除瀏覽資料" 裡的 "Cookie 和其他網站資料" 可以清除 `~/.config/google-chrome` 裡的快取，
          "快取圖片和檔案" 可以清除 `~/.cache/google-chrome` 裡的快取。
        - 安裝 extension: [1995eaton/chromium-vim: Vim bindings for Google Chrome.](https://github.com/1995eaton/chromium-vim)
    * 4kvideodownloader@A

* 教育
    * 數學: (Mathematica 12.0)@O (MATLAB R2020a)@O(依賴於: libselinux@A(依賴於: libsepol@A))
        - Mathematica: 不使用 root 權限安裝在 `~/.local/opt`，安裝與啟用說明跟安裝檔在一起，
          另外還在 `~/.local/share/applications/wolfram-mathematica12.desktop` 加入 `Categories=Education;`。
    * jupyter-calysto_scheme-git@A(依賴於: jupyter-metakernel@A)

* 系統
    * 密碼管理: gnome-keyring
        - gnome-keyring: 第一次使用時，會詢問「預設鑰匙圈」的密碼，**留空後按確認**，不然每次使用時都會跳出視窗要求輸入密碼。
        - gnome-keyring: 新增檔案: `~/.local/share/keyrings`。