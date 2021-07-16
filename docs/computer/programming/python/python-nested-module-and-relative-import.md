# Python 巢狀 module 和 relative import

假設現在有以下資料夾型 script

```
app/
    __main__.py
    module1/
        __init__.py
    module2/
        __init__.py
        module2a.py
    module3/
        __init__.py
        module3a/
            __init__.py
```

在 `app/__main__.py` 中可以用

``` python
import module1
import module2
import module3
```

但在 `app/module2/__init__.py` 中必須用

``` python
from . import module2a
```

同理，在 `app/module3/__init__.py` 中必須用

``` python
from . import module3a
```

原因是執行 `python app` 後，`sys.path` 中只有 `app` 資料夾和其它系統路徑，所以 app 中的模組 (module1, module2, module3) 必須用 relative import 的方式 import 其子模組 (module2a, module3a)。

參考資料: [5. The import system — Python 3.9.6 documentation](https://docs.python.org/3/reference/import.html#package-relative-imports)