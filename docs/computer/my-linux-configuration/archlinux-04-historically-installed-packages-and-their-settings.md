# Arch Linux (四) 以前安裝過的軟體包及相關設定

## 應用程式

* 教育
    * 數學: (Mathematica 12.0)@O (MATLAB R2020a)@O(依賴於: libselinux@A(依賴於: libsepol@A))
        - Mathematica: 不使用 root 權限安裝在 `~/.local/opt`，安裝與啟用說明跟安裝檔在一起，
          另外還在 `~/.local/share/applications/wolfram-mathematica12.desktop` 加入 `Categories=Education;`。
    * jupyter-calysto_scheme-git@A(依賴於: jupyter-metakernel@A)