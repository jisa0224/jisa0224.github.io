# Linux 執行程式時出現 No such file or directory 錯誤

有時候執行程式時明明有 `x` 權限，也確定是可執行檔，但卻出現 `No such file or directory` 錯誤。

可能是因為你在 x86\_64 的電腦上執行 x86\_32 格式的執行檔，但電腦裡沒有 multilib 的環境。

multilib 環境讓 x86\_64 的電腦可以執行和編譯 x86\_32 格式的執行檔，Slackware 64-bit 剛裝完是沒有 multilib 的，可以自己去裝，但是就比較麻煩。

要看一個執行檔是 x86\_64 還是 x86\_32 格式，可以用 `file`。

```
$ file /bin/ls
/bin/ls: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, stripped
```

```
$ file btest
btest: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=8f430a6d2d519dc1af8ba74867fc435c33abb688, not stripped
```

註：btest 是 CS:APP Data Lab 的一部分。

解決方案就是去裝 multilib 環境，或者用 VirtualBox 裝個純 x86\_32 或有 multilib 的作業系統。我有想過可不可以用 Docker，不過還沒試。

參考資料：[linux - "No such file or directory" error when executing a binary - Stack Overflow](https://stackoverflow.com/questions/2716702/no-such-file-or-directory-error-when-executing-a-binary)
 
