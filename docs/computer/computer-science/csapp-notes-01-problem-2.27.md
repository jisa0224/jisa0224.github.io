# 【CS:APP 筆記】Problem 2.27 檢查無號整數相加是否溢位

章節：2.3  
問題頁數：P. 89  
解答頁數：P. 152

在解答中提出了

``` c
int uadd_ok(unsigned x, unsigned y) {
    unsigned sum = x + y;
    return sum >= x;
}
```

但我想到另一種解法

``` c
int uadd_ok(unsigned x, unsigned y) {
    return x + y >= x;
}
```

我想知道這樣是否可以

於是我另外寫了以下程式：

``` c
int main() {
    unsigned char x = 255;
    unsigned char y = 1;
    unsigned char sum = x + y;
    printf("%d\n%d\n", sum >= x, x + y >= x);
 
    return 0;
}
```

結果意外的是，輸出為

```
0
1
```

我原本以為是因為 `gcc` 把 `x + y >= x` 優化成 `y >= 0` 的關係，但當我另外用 `-O0` 去編譯時，出來的結果一樣，且 `cmp` 兩個執行檔完全一樣，也就是說 `gcc` 預設是 `-O0`

於是我反組譯它得到了

``` hl_lines="9 10 13 14 15 16"
0000000000400660 <main>:
  400660: 55                    push   rbp
  400661: 48 89 e5              mov    rbp,rsp
  400664: 48 83 ec 10           sub    rsp,0x10
  400668: c6 45 ff ff           mov    BYTE PTR [rbp-0x1],0xff               x = 255;
  40066c: c6 45 fe 01           mov    BYTE PTR [rbp-0x2],0x1                y = 1;
  400670: 0f b6 55 ff           movzx  edx,BYTE PTR [rbp-0x1]                /* edx = x
  400674: 0f b6 45 fe           movzx  eax,BYTE PTR [rbp-0x2]                 * eax = y
  400678: 01 d0                 add    eax,edx                                * edx = edx + eax = x + y = 256 */
  40067a: 88 45 fd              mov    BYTE PTR [rbp-0x3],al                 sum = x + y = 0;
  40067d: 0f b6 55 ff           movzx  edx,BYTE PTR [rbp-0x1]                /* edx = x
  400681: 0f b6 45 fe           movzx  eax,BYTE PTR [rbp-0x2]                 * eax = y
  400685: 01 c2                 add    edx,eax                                * edx = edx + eax = x + y = 256
  400687: 0f b6 45 ff           movzx  eax,BYTE PTR [rbp-0x1]                 * eax = x
  40068b: 39 c2                 cmp    edx,eax                                * compare edx = x + y = 256 and eax = x = 255
  40068d: 0f 9d c0              setge  al                                     * al = (x + y >= x) = 1
  400690: 0f b6 d0              movzx  edx,al                                 * edx = al = 1 */
  400693: 0f b6 45 fd           movzx  eax,BYTE PTR [rbp-0x3]                /* eax = sum = 0
  400697: 3a 45 ff              cmp    al,BYTE PTR [rbp-0x1]                  * compare al = 0 and x = 255
  40069a: 0f 93 c0              setae  al                                     * al = 0
  40069d: 0f b6 c0              movzx  eax,al                                 * eax = al = 0
  4006a0: 89 c6                 mov    esi,eax                                * esi = eax = 0 */
  4006a2: bf 8c 07 40 00        mov    edi,0x40078c
  4006a7: b8 00 00 00 00        mov    eax,0x0
  4006ac: e8 1f fe ff ff        call   4004d0 <printf@plt>                   printf(rdi = 0x0040078c, rsi = 0, rdx = 1);
  4006b1: b8 00 00 00 00        mov    eax,0x0
  4006b6: c9                    leave  
  4006b7: c3                    ret    
  4006b8: 0f 1f 84 00 00 00 00  nop    DWORD PTR [rax+rax*1+0x0]
  4006bf: 00
```

最後一欄是我的註解

可以看到問題出在於標記的這兩個地方

這兩個地方都是先把 x 和 y 複製到四 byte 的暫存器裡再加，所以加完後是 256 而不是馬上 mod 256 變成 0  
前面的部份因為最後要寫入到只有一個 byte 的 `sum` 裡，所以會被 mod 256 變成 0，比較之後 0 \> 255 為 false  
但是後面的部份繼續留在有四個 byte 的 edx 裡，所以比較之後 256 \> 255 為 true

所以如果把第 13 行改成 `add dl,al` 再組譯它可以嗎？

**可以**

改完後的輸出就會是

```
0
0
```

作法就是先 `gcc -masm=intel -S test.c`  
然後修改 `test.s` 中那一行  
之後再 `gcc -o test test.s`
 
