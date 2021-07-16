# Python 執行模式

Python 3 的程式結構主要分成 script 和 module。

## Script

script 可以是

* 單一純文字檔 `script.py`: 以 `python script.py` 方式執行。
* 包含 `__main__.py` 的資料夾 `script`: 以 `python script` 方式執行。
* 包含 `__main__.py` 的 zip 壓縮檔 `script.zip`: 以 `python script.zip` 方式執行。

## Module

module 可以是

* 單一純文字檔
* 包含 `__init__.py` 的資料夾
* 包含 `__init__.py` 的 zip 壓縮檔

不管是哪一種，都可以在 Python 程式碼中以 `import module` 方式 import。

## sys.path

在執行 script 前，Python interpreter 會將一些檔案路徑放入 `sys.path` 變數最前面，以供 import module 時搜尋。

* 以 REPL 方式執行 (`python`): 加入空字串 (代表工作資料夾)。
* 自 stdin 讀取 script 執行 (`python -`): 加入空字串 (代表工作資料夾)。
* 以 `python -c <command>` 方式執行: 加入空字串 (代表工作資料夾)。
* 以 `python -m <module-name>` 方式執行: 從工作資料夾及 `sys.path` 中搜尋 module，並**加入工作資料夾 (非空字串)**。
* 以 `python <script>` 方式執行
  * 若該 script 是單一純文字檔，則加入該檔案所在的資料夾，並執行該檔案。
  * 若該 script 是包含 `__main__.py` 的資料夾，則加入該資料夾，並執行該資料夾中的 `__main__.py`。
  * 若該 script 是包含 `__main__.py` 的 zip 壓縮檔，則加入該 zip 壓縮擋，並執行該 zip 壓縮檔中的 `__main__.py`。

## python -m 的陷阱

特別注意到 `python -m` 是加入**工作資料夾**，而不是加入 module 所在資料夾或 module 本身。

因此，若 module 是一個資料夾/zip 壓縮擋，且 `__main__.py` 需要 import 該資料夾內的其它 module 時，
需要用 relative import (`from . import submodule`) 的方式。

但這樣若以 `python <script>` 的方式執行就會出錯。

## 參考資料

* [Command line and environment — Python 3.9.6 documentation](https://docs.python.org/3/using/cmdline.html#interface-options)
* [sys — System-specific parameters and functions — Python 3.9.6 documentation](https://docs.python.org/3/library/sys.html#sys.path)
* [5. The import system — Python 3.9.6 documentation](https://docs.python.org/3/reference/import.html#package-relative-imports)