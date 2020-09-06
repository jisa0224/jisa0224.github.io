# 【CS:APP 筆記】Stack 與未初始化的區域變數

章節：3.7.4

函數的區域變數會在被呼叫後於 stack 分配位置，而返回之後只是調整 `rsp` 的值，也就是說原本的資料還留著。

那如果在呼叫一次相同的函數，但不初始化區域變數，還能讀到上次的資料嗎？

``` c
#include <stdio.h>
 
void test() {
    char a;    // uninitialized
    printf("%p: %d\n", &a, a);
    a++;
}
 
int main() {
    for(int i = 0; i < 10; i++)
        test();
}
```

結果

```
// 第一次
0x7fffde89623f: 0
0x7fffde89623f: 1
0x7fffde89623f: 2
0x7fffde89623f: 3
0x7fffde89623f: 4
0x7fffde89623f: 5
0x7fffde89623f: 6
0x7fffde89623f: 7
0x7fffde89623f: 8
0x7fffde89623f: 9
 
// 第二次
0x7ffd6944269f: 0
0x7ffd6944269f: 1
0x7ffd6944269f: 2
0x7ffd6944269f: 3
0x7ffd6944269f: 4
0x7ffd6944269f: 5
0x7ffd6944269f: 6
0x7ffd6944269f: 7
0x7ffd6944269f: 8
0x7ffd6944269f: 9
```

去看 `/proc/*/maps` 就會知道，區域變數 `a` 是在 stack 裡。

但這只是剛好而已，如果真的要這樣做，最好還是宣告為 static 或全域變數。順帶一提，static 和全域變數都是被放在 heap 的前一段。
 
