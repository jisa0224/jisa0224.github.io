# Cling: Interactive C++ Interpreter 使用指南

由於 Cling 的官方文件沒多少東西，因此寫這份文件紀錄。

以下假設有一個 C++ 程式碼檔 `foo.cpp`

``` cpp
#include <cstdio>

int add(int a, int b) {
    return a + b;
}

int main() {
    printf("Hello World!\n");
	printf("1 + 2 = %d\n", add(1, 2));
	
	return 0;
}
```

## 顯示回傳值與不顯示回傳值

```
[cling]$ int a = 10;
[cling]$ a
(int) 10
[cling]$ a;
[cling]$ int b = 99
(int) 99
```

不管是宣告還是函式呼叫，只要後面有接分號，就不會顯示回傳值；沒有分號就會顯示回傳值。

## 從命令列直接執行 .cpp 檔

```
$ cling foo.cpp 
warning: cannot find function 'foo()'; falling back to .L
```

Cling 會在讀取完整個檔案後執行 `foo.cpp` 中的 `foo()`，所以只要把 `int main()` 改成 `int foo()` 即可。

但如果想要同時能讓 Cling 執行且通過 GCC 編譯的話，可以改成下面這樣：

``` cpp
#ifdef __CLING__
int foo() {
#else
int main() {
#endif
```

註一：經過測試，如果以上述方式執行含有 `main()` 的 `main.cpp`，會導致 Cling 崩潰退出！
註二：因為 Cling 會執行 `foo()`，所以 `int foo(int argc, *argv[])` 是不可行的，目前還沒有找到傳遞命令列參數的方式。

### 為什麼知道有 `__CLING__` ？

利用 Cling 的 `.g`

```
   .g 				- Prints out information about global variable
				  'name' - if no name is given, print them all
```

複製出來後 `grep` 可以得到

```
<command line>    7 (address: NA) #define __CLING__CXX11 = 1
<command line>    3 (address: NA) #define __CLING__GNUC_MINOR__ = 3
<command line>    2 (address: NA) #define __CLING__GNUC__ = 9
<command line>    6 (address: NA) #define __CLING__ = 1
<command line>    4 (address: NA) #define _GLIBCXX_USE_CXX11_ABI = 1
<command line>    5 (address: NA) #define CLING_EXPORT
<command line>    1 (address: NA) #define NDEBUG = 1
```

所以可以利用 `__CLING__` 這個 marco 再加上 `#ifdef` 來做到同時能讓 Cling 執行且通過 GCC 編譯。

## 從命令列載入 .cpp 檔後留在 REPL 界面

使用 `cling -l foo.cpp`，之後就可以

```
[cling]$ add(3, 4)
(int) 7
```

## 從 Cling 的 REPL 界面載入 .cpp 檔

利用 Cling 的 `.L`

```
[cling]$ .L foo.cpp
[cling]$ add(3, 4)
(int) 7
```

## .cpp 檔案的最外層只能有「宣告」

我本來想說是否能夠從 Cling 的 REPL 界面執行 .cpp 檔，所以我就在 `foo.cpp` 的最後加上

```
#ifdef __CLING__
foo();
#endif
```

結果不論是從命令列執行，或從 REPL 執行都顯示錯誤

```
$ cling foo.cpp 
In file included from input_line_3:1:
/tmp/foo.cpp:21:1: error: C++ requires a type specifier for all declarations
foo();
^
```

```
$ cling -l foo.cpp 
In file included from input_line_3:1:
./foo.cpp:21:1: error: C++ requires a type specifier for all declarations
foo();
^
[cling]$ 
```

```
$ cling 
[cling]$ .L foo.cpp
In file included from input_line_3:1:
/tmp/foo.cpp:21:1: error: C++ requires a type specifier for all declarations
foo();
^
[cling]$ 
```

有此可知，.cpp 檔案的最外層只能有「宣告」，只有在 REPL 界面才可以有「命令」。

## 讓 Cling 可以直接顯示 `struct/class` 等複合型別的內容

對於 primitive 型別，Cling 可以直接顯示出其內容：

```
[cling]$ int a = 3;
[cling]$ a
(int) 3
[cling]$ int b[] = {1, 2, 3, 4};
[cling]$ b
(int [4]) { 1, 2, 3, 4 }
```

但如果是自己建立的 `struct/class` 複合型別的話就不行了

```
[cling]$ struct foo {int x; int y;}
[cling]$ foo a = {1, 2};
[cling]$ a
(foo &) @0x7fc07ace4010
```

根據 [Custom type value printers for Cling – Michiel's 0s & 1s](https://me.m01.eu/blog/2018/07/custom-type-value-printers-for-cling) 的說明，該文作者從 [Cling 的原始碼](https://github.com/root-project/cling/blob/2a60e2a/lib/Interpreter/ValuePrinter.cpp#L676)中發現：只要為自訂型別定義 `cling::printValue` 函數，就可以讓它顯示內容：

``` cpp
#include <sstream>
 
namespace cling {
    std::string printValue(const foo* f) {
        std::ostringstream oss;
        oss << "{.x=" << f->x << ", " << ".y=" << f->y << "}";
        return oss.str();
    }
}
```

可以得到

```
[cling]$ a
(foo &) {.x=1, .y=2}
```

而且用 gcc 編譯也不會顯示錯誤
 
