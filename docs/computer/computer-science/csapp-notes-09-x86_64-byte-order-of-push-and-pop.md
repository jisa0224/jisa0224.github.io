# 【CS:APP 筆記】x86_64 PUSH 與 POP 的 byte order

章節：3.10.3  
頁數：P. 283 Practice 3.46

1.  初始 stack
    
    ```
    --  <= rsp
    ```

2.  執行 `push 0x01234567` 後的 stack
    
    ```
    --
    00
    00
    00
    00
    01
    23
    45
    67  <= rsp
    ```
    
    註：沒有 push *imm64* 的電路實現
    
    GDB 的結果
    
    ```
    (gdb) x/xg $rsp
    0x7fffffffdd68: 0x0000000001234567
    (gdb) x/8xb $rsp
    0x7fffffffdd68: 0x67 0x45 0x23 0x01 0x00 0x00 0x00 0x00
    ```
    
    記住：stack 是由高位址往低位址長的，再加上 x86\_64 是小端，所以 rsp 所指的地方就是 short、int 和 long
    的開頭！
    
    而 push 一個立即數的結果會符合這個規則。
    
    那麼暫存器呢？

3.  執行 `pop rax` 後  
    GDB 的結果
    
    ```
    (gdb) print /x $rax
    $7 = 0x1234567
    ```

4.  執行 `push rax` 後的 stack
    
    ```
    --
    00
    00
    00
    00
    01
    23
    45
    67  <= rsp
    ```
    
    GDB 的結果
    
    ```
    (gdb) x/xg $rsp
    0x7fffffffdd68: 0x0000000001234567
    (gdb) x/8xb $rsp
    0x7fffffffdd68: 0x67 0x45 0x23 0x01 0x00 0x00 0x00 0x00
    ```
    
    也同樣沒有問題
 
