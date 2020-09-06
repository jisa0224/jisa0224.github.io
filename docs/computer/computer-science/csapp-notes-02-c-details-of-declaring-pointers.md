# 【CS:APP 筆記】C 語言中宣告指標的小細節

## 星號的位置

``` c
int *p1, *p2;
int* p3, p4;
int* p5, *p6;
int * p7;
int * p8, p9;
 
/* p1: int *
 * p2: int *
 * p3: int *
 * p4: int
 * p5: int *
 * p6: int *
 * p7: int *
 * p8: int *
 * p9: int
 */
```

也就是說是不是指標就只看名稱前面有沒有 `*` 號。

## 指標陣列與指向陣列的指標

來源：CS:APP Machine Prog: Data 影片和講義
  
code  
因為在 C 的運算子順序中 `( )` 與 `[ ]` 同級，且它們優先於 `*`。
  
參考資料：[C Operator Precedence - cppreference.com](https://en.cppreference.com/w/c/language/operator_precedence)

### 指向 void 的指標

問題來源：CS:APP 2.3 Aside P. 100

如果宣告一個 `void *p = 0;`  
那麼執行完 `p++` 之後 `p` 會是多少？

答案是 1  
因為 `sizeof(void) = 1`
 
