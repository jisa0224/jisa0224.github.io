# Bash 如何輸入同資料夾下的檔名但不重複輸入路徑

例如：資料夾 `test` 下有檔案 `a1` 和 `a2`，可以用 `<cmd> test/a1 test/a2`
來執行，但如果路徑太常就會很麻煩。

此時就可以使用 Bash 的 Brace Expansion 功能

以上面的例子來說就會變成

```
<cmd> test/a{1,2}
```

另外，`{1..5}` 會展開成 `1 2 3 4 5`
  
更詳細的功能可參考 man bash 中的 Brace Expansion 一段
  
參考資料：[mv - Quickest way to rename files, without retyping directory path - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/132235/quickest-way-to-rename-files-without-retyping-directory-path/132237#132237)
 
