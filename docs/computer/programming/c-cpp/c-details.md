# C 語言細節(未完成)

## extern 與 static

[21]  [轉載] C 陷阱： extern ＆ static ＆ 多檔案、宣告、定義、變數、函式  
[21]  [轉載] C 语言中 extern 关键字详解  
[21]  [轉載] C 語言:關於變數的二三事

<https://medium.com/@alan81920/c-c-%E4%B8%AD%E7%9A%84-static-extern-%E7%9A%84%E8%AE%8A%E6%95%B8-9b42d000688f>

## Expression 與 Statement

## Compound Statement

當我們使用迴圈時，會需要在迴圈外宣告一個變數來當 iterator（因為 C 不允許 `for(int i...)`）。

如果一段程式中有多個迴圈，又不希望每個都宣告一個 iterator 時，我們必須使用前一個迴圈宣告的 iterator，但在實做上會造成變數管理不易，若是刪除了最前面的迴圈，則其 iterator 通常也會被刪除，造成後面找不到變數。

此息我希望能夠利用 `{ }` 來造成變數的區域性，原本我以為 `{ }` 一定要屬於 `if`、`while` 或 函數等區塊，但後來仔細閱讀 C11 標準後發現：

```
statement:
      labeled-statement
      compound-statement
      expression-statement
      selection-statement
      iteration-statement
      jump-statement

compound-statement:
      { block-item-list(opt) }

block-item-list:
      block-item
      block-item-list block-item

block-item:
      declaration
      statement

selection-statement:
      if ( expression ) statement
      if ( expression ) statement else statement
      switch ( expression ) statement
```

換言之，`{ }` 可以單獨存在！而且它並不是 `if` 的一部分，而是後面的 `statement`。

從這裡也可看出 `else if` 並非最底層的語法，而是在 `else` 後面放上一個 `selection-statement`。

所以我們可以這樣寫：

``` c
#include <stdio.h>

int main() {
    int x = 1;

    printf("%d\n", x);        // 1

    /* block 1 */ {
        int x = 2;
        printf("%d\n", x);    // 2
    }

    printf("%d\n", x);        // 1

    /* block 2 */ {
        int x = 3;
        printf("%d\n", x);    // 3
    }

    printf("%d\n", x);        // 1

    return 0;
}

```

這種寫法還可以讓我們在一段程式內進行分區，但又不想把它拉出去另外一個函式時用。