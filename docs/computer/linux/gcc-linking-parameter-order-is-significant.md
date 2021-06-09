# GCC 連結時的參數有先後順序

當使用 GCC 連結 (linking) 複數目的擋 (object files) 和函式庫 (透過 `-l` 選項) 時，其參數的先後順序是有意義的，如果隨便放會連結失敗。

## 官方文擋說明

`man gcc` 對於此有說明:

```
DESCRIPTION

       You can mix options and other arguments.  For the most part, the
       order you use doesn't matter.  Order does matter when you use
       several options of the same kind; for example, if you specify -L
       more than once, the directories are searched in the order
       specified.  Also, the placement of the -l option is significant.

OPTIONS

   Options for Linking

       -llibrary
       -l library
           Search the library named library when linking.  (The second
           alternative with the library as a separate argument is only
           for POSIX compliance and is not recommended.)

           The -l option is passed directly to the linker by GCC.  Refer
           to your linker documentation for exact details.  The general
           description below applies to the GNU linker.

           The linker searches a standard list of directories for the
           library.  The directories searched include several standard
           system directories plus any that you specify with -L.

           Static libraries are archives of object files, and have file
           names like liblibrary.a.  Some targets also support shared
           libraries, which typically have names like liblibrary.so.  If
           both static and shared libraries are found, the linker gives
           preference to linking with the shared library unless the
           -static option is used.

           It makes a difference where in the command you write this
           option; the linker searches and processes libraries and
           object files in the order they are specified.  Thus, foo.o
           -lz bar.o searches library z after file foo.o but before
           bar.o.  If bar.o refers to functions in z, those functions
           may not be loaded.
```

連結器從左到右掃描參數中的目的擋和函式庫，概念上可能類似以下 psuedocode:

```
undefined_references = []

for f in 參數中的目的擋和函式庫:
    if f 中具有未定義的符號 s:
        undefined_references += s
    if f 中有 undefined_references 紀錄的符號:
        連結 s
        undefined_references -= s

if undefined_references is not empty:
    連結失敗
```

## 實驗一

``` c
// main.c
#include <math.h>
int main() {
    int e = 3;           // pow(2, 3) will be optimized to a constant
    return pow(2, e);    // so libm.so will not be linked.
}
```

不加 `-lm` 會顯示 `undefined reference` 錯誤:

```
$ gcc -o main main.c
/usr/bin/ld: /tmp/ccsNgJc8.o: in function `main':
main.c:(.text+0x29): undefined reference to `pow'
collect2: error: ld returned 1 exit status
```



## 結論

鍊結時，**被需要**的目的擋和函式庫應盡量放**後面**。

## 參考資料

* `man gcc`
* [静态库和动态库区别 | 守望的个人博客](https://www.yanbinghu.com/2019/06/27/47343.html)
* [一个奇怪的链接问题 | 守望的个人博客](https://www.yanbinghu.com/2018/10/06/46212.html)
* [linux下制作静态库 | 守望的个人博客](https://www.yanbinghu.com/2019/07/10/23906.html)