# 【CS:APP 筆記】P.259 多維陣列取值的組合語言另解

章節：3.8.3  
頁數P. 259

在課本裡提供了這樣的方法

``` asm
leaq (%rsi,%rsi,2), %rax
leaq (%rdi,%rax,4), %rax
movl (%rax,%rdx,4), %eax
```

在我的電腦上使用 `-O1` 以上才會得到這樣的程式碼

而我想到了

``` asm
leaq (%rsi,%rsi,2), %rax
leaq (%rax,%rdx), %rax
movl (%rdi,%rax,4), %eax
```

根據之前的方法修改後組譯，結果是可以的

另外，我的電腦在 `-Og` 下產生出了這樣的程式碼(`-O0` 有十幾行)

``` asm
leaq (%rsi,%rsi,2), %rcx
leaq 0(,%rcx,4), %rax
addq %rdi, %rax
movl (%rax,%rdx,4), %eax
```

基本上和課本的方法是一樣的
 
