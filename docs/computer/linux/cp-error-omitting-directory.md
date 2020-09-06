# 解決 cp: omitting directory 錯誤

當你用 `cp` 複製資料夾的時候，無論它是不是空的，都會出現 `cp: omitting directory` 的錯誤，因為
  
`cp` 不加參數時**只能複製檔案**
  
如果要複製資料夾，必須加上 `-r`、`-R` 或 `--recursive`
  
`rm` 也是這樣，但 `mv` 則不會有此問題
  
參考資料：[Linux World: "cp: omitting directory" error in linux](http://tuxthink.blogspot.com/2012/06/cp-omitting-directory.html)
 
