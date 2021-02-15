# 使用 Python 快速建立一個簡單的 HTTP 伺服器

先切換到網站的根目錄，然後執行 `python -m http.server` 即可。

**重要**：記得開啟防火牆。

預設 port 是 8000，可以用 `python -m http.server <port>` 改成其它 port。

參考資料：[http.server — HTTP servers — Python 3.9.1 documentation](https://docs.python.org/3/library/http.server.html)

備註：`python -m SimpleHTTPServer <port>` 是 Python 2 的用法，此 module 在 Python 3 中被整合到 `http.server` 中。 