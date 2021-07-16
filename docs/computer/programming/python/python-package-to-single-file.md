# Python 打包資料夾成單一檔案

Python 3 的 script 和 module 可以以資料夾的形式使用，但資料夾在傳輸和儲存上不方便。
因此 Python 支援將資料夾打包成 zip 壓縮擋的形式，並且使用上和資料夾完全相同。

## 手工打包

假設我們有以下的資料夾型 script

```
script/
    __main__.py
    module1/
        __init__.py
        module1a.py
        module1b.py
    module2/
        __init__.py
        module2a.py
    module3.py
```

將 `script` 資料夾中的所有檔案 (**但不包含 `script` 資料夾**) 壓縮成 zip 檔 `script.zip` 即可。

注意 `script.zip` 中的最頂層是 `__init__.py`，而不是 `script` 資料夾。

這樣就可以以 `python script.zip` 方式執行了。

對於資料夾型 module 也是這樣打包，但要注意 relative import 的問題。

## 使用 zipapp 打包

若是電腦中沒有安裝 zip 壓縮工具，就無法使用手工打包，因此 Python 提供了 zipapp module。

切換到 `script` 的上層資料夾，執行 `python -m zipapp script` 即可，會產生 `script.pyz`，同樣以 `python script.pyz` 方式執行。

雖然副檔名為 `.pyz`，但實際上它就是一個 zip 壓縮擋。

## 自解壓縮 zip 檔

若是每次都要以 `python script.pyz` 方式執行，看起來有點不直觀。

我們可以利用 Unix-like 作業系統的 shebang 支援，把 `script.pyz` 變成**看起來像是**普通可執行檔。

執行 `echo '#!/usr/bin/env python3' | cat - script.zip > script`，然後執行 `chmod +x script`，就可以像普通可執行檔一樣用 `./script` 執行。

原理只是把 `#!/usr/bin/env python3` 給加到 zip 檔的最前端而已。

當然這個檔案就無法用普通的 zip 檔案管理器打開了。

## 參考資料

* [How to build a single python file from multiple scripts? - Stack Overflow](https://stackoverflow.com/questions/9002275/how-to-build-a-single-python-file-from-multiple-scripts)
* [zipapp — Manage executable Python zip archives — Python 3.9.6 documentation](https://docs.python.org/3/library/zipapp.html)