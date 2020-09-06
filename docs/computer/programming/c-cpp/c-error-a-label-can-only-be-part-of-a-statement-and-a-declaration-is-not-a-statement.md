# C語言編譯時的 a label can only be part of a statement and a declaration is not a statement 錯誤

當我對

``` c
int main() {
    int a = 1;
    switch(a) {
        case 1:
            char c = 'a';
        default:
            a++;
    }
}
```

進行編譯時，很不可思議地得到

```
a.c: In function ‘main’:
a.c:5:13: error: a label can only be part of a statement and a declaration is not a statement
             char c = 'a';
             ^
```

理由是 label 後面**不能接著宣告(declaration)**，而 `switch` 的 `case` 似乎也算 label，所以不允許，如果改成

``` c
case 1: ;
    char c = 'a';
```

就會過了，因為 `;` 就等於是一個空敘述，而空敘述不是宣告。
  
同理，用 `goto` 可以跳過去的那種 label 也會受到這個限制。
  
參考資料：[c - Why do I get "a label can only be part of a statement and a declaration is not a statement" if I have a variable that is initialized after a label? - Stack Overflow](https://stackoverflow.com/questions/18496282/why-do-i-get-a-label-can-only-be-part-of-a-statement-and-a-declaration-is-not-a/18496437#18496437)
 
