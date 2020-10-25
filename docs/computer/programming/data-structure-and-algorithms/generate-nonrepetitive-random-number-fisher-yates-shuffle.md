# 生成不重複隨機數：Fisher-Yates shuffle

## 問題

> 給定一個正整數 N，產生一個序列，其中每個數都是從 1 ~ N 的隨機正整數，但序列中沒有重複的數。

## 問題分析

因為每一個數都不能重複，所以這個序列最長就是 N，所以這個問題可以推廣如下：

> 給定一個長度為 N 的序列，求該序列的一個隨機排列(permutation)。

* **隨機排列**指該序列的 N! 種排列（假定序列中每個東西都不相同），每一種被選到的機率相等。
* 在原版的問題中，給定的序列其實就是從 1 ~ N 的正整數序列，但其實也可以是其它東西的序列。
* 如果只需要 k 個隨機數，隨機排列後取前 k 個即可。

## Fisher-Yates shuffle: Pencil-and-paper method

### Python 實做

``` python
from random import randint
def random_permute(x):
    result = []
    while len(x) > 0:
        idx = randint(0, len(x)-1)     # 產生 [0, len(x)-1] 而不是 [0, len(x)-1) 的隨機數
        result.append(x[idx])
        x.remove(x[idx])               # 把用過的號碼刪掉
    return result
```

從陣列的中間移除元素相當沒有效率，所以可以用 swap 直接把它換到最後

``` python
from random import randint
def random_permute(x):
    N = len(x)
    result = []
    for i in range(N-1):
        idx = randint(i, N-1)          # 產生 [i, N-1] 而不是 [i, N-1) 的隨機數
        result.append(x[idx])
        x[i], x[idx] = x[idx], x[i]    # 把用過的號碼往前換
    return result
```

## Fisher-Yates shuffle: Modern method

這是 in-place 版

### Python 實做

``` python
from random import randint
def random_permute(x):
    N = len(x)
    for i in range(N-1):
        idx = randint(i, N-1)          # 產生 [i, N-1] 而不是 [i, N-1) 的隨機數
        x[i], x[idx] = x[idx], x[i]
    return x
```

## 參考資料

* [Random permutation - Wikipedia](https://en.wikipedia.org/wiki/Random_permutation)
* [Fisher–Yates shuffle - Wikipedia](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)