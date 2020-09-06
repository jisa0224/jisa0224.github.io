# C 語言技巧(未完成)

## 使用 C11 的 thread.h 達成跨平台的 sleep()

[thrd_sleep - cppreference.com](https://en.cppreference.com/w/c/thread/thrd_sleep)

## ?

上面的 `(struct timespec){.tv_sec=1}` 是可以直接宣告？

## 直接對 String literal 做 Array subscripting

``` c
#include <stdio.h>

int main() {
    putchar("abcdefg"[3]);    // d

    return 0;
}
```