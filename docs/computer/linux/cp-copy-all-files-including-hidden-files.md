# cp 複製包含隱藏檔在內的所有檔案

## 問題

建立測試環境

```shell
mkdir old{,/oldD} new{,/newD}
touch old/{oldN,.oldH} new/{newN,.newH}
```

測試環境

```
.
├── new
│   ├── newD
│   ├── .newH
│   └── newN
└── old
    ├── oldD
    ├── .oldH
    └── oldN
```

從執行環境執行 `cp -r old/* new` 後

```
.
├── new
│   ├── newD
│   ├── .newH
│   ├── newN
│   ├── oldD
│   └── oldN
└── old
    ├── oldD
    ├── .oldH
    └── oldN
```

Shell 的 filename expansion 沒辦法把以 `.` 開頭的隱藏檔給複製過去。

如果執行 `cp -r old/* old/.* new` 會出錯，所以不行。

## 解決方案

從測試環境執行 `cp -r old/. new` 或 `cp -T -r old new` 後（兩者結果相同）

```
.
├── new
│   ├── newD
│   ├── .newH
│   ├── newN
│   ├── oldD
│   ├── .oldH
│   └── oldN
└── old
    ├── oldD
    ├── .oldH
    └── oldN
```

## 原理

### cp 會合併兩個相同名稱的資料夾

建立測試環境

```shell
mkdir old{,/dir} new{,/dir}
touch old/{file1,dir/file2} new/{file3,dir/file4}
```

測試環境

```
.
├── new
│   ├── dir
│   │   └── file4
│   └── file3
└── old
    ├── dir
    │   └── file2
    └── file1
```

從執行環境執行 `cp -r old/* new` 後

```
.
├── new
│   ├── dir
│   │   ├── file2
│   │   └── file4
│   ├── file1
│   └── file3
└── old
    ├── dir
    │   └── file2
    └── file1
```

可以發現，`cp -r` 對於同名的資料夾，採取的是「合併 (merge)」操作，而不是直接用來源資料夾覆蓋掉目的資料夾。
（當然，如果來源資料夾和目的資料夾內的一般檔案的名稱重複，就會採取覆蓋操作。）

### cp 不會自動約化檔案路經中的 `.`

在 Linux 裡，對於一個資料夾 `dir`，會存在一個 hard link `dir/.` 指向它自己，他們具有相同的 inode，所以本質上是同一個檔案（資料夾）。
因此，我們可能預期 `cp -r old/. new` 和 `cp -r old new` 應該要具有相同的執行結果，因為 `old/.` 和 `old` 視同一個檔案（資料夾）。
然而，執行 `cp -r old new` 卻會把 `old` 複製到 `new/old` 中。

之所以會有這樣的區別，是因為 `cp` 不會自動約化檔案路經 (path) 中的 `.`。

因此，對於 `cp -r old/. new` 來說，`cp` 會將 `old` 裡的 `.` 複製到 `new` 資料夾裡，但因為 `new` 資料夾中已經存在同名的資料夾 `.`，
所以 `old` 裡的 `.` 會合併到 `new` 裡的 `.`，結果就是 `cp` 會把 `old/.`（也就是 `old`）裡的檔案複製到 `new/.`（也就是 `new` 裡）。

備註：讀取資料夾內容時 `cp` 會忽略 `.` 和 `..`，所以不會有遞迴的問題（參考 `copy.c`）。

### cp 的三種模式

根據 `man cp`，`cp` 具有以下三種模式：

```
cp [OPTION]... [-T] SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
cp [OPTION]... -t DIRECTORY SOURCE...
```

在第一種模式中，`SOURCE` 和 `DEST` 的組合可以有很多種情況：

| `SOURCE`   | `DEST`                 | 結果                                                                                    |
|------------|------------------------|-----------------------------------------------------------------------------------------|
| 檔案或資料夾 | 不存在                  | 直接複製一個完全相同的檔案或完全相同內容的資料夾，只是檔名變成 `DEST`                             |
| 檔案        | 存在且為檔案             | 用來源檔案覆蓋目的檔案                                                                     |
| 資料夾      | 存在且為檔案             | 錯誤：`cp` 無法以目錄來覆蓋非目錄                                                           |
| 檔案或資料夾 | 存在且為資料夾，不加 `-T` | `cp` 會在內部轉換為第二種形式，因此 `cp -r old new` 的結果會是 `old` 被複製到 `new/old` 裡      |
| 資料夾      | 存在且為資料夾，加 `-T`   | 用來源資料夾合併 (merge) 目的資料夾，因此 `cp -T -r old new` 的結果會是 `old` 被合併到 `new` 裡 |
| 檔案        | 存在且為資料夾，加 `-T`   | 錯誤：`cp` 無法以非目錄來覆蓋目錄                                                           |

## 參考資料

* `man cp`
* [coreutils/cp.c at master · coreutils/coreutils](https://github.com/coreutils/coreutils/blob/master/src/cp.c)
* [coreutils/copy.h at master · coreutils/coreutils](https://github.com/coreutils/coreutils/blob/master/src/copy.h)
* [coreutils/copy.c at master · coreutils/coreutils](https://github.com/coreutils/coreutils/blob/master/src/copy.c)