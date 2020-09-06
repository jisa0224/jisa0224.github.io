# [演算法筆記] 最大子數列問題 Maximum Subarray Problem(未完成)

## 問題

> In computer science, the **maximum subarray problem** is the task of finding a contiguous subarray with the largest sum, within a given one-dimensional array $A[1...n]$ of numbers. Formally, the task is to find indices $i$ and $j$ with $1 \leq i \leq j \leq n$, such that the sum
> 
> $$ \sum _{x=i}^{j}A[x] $$
> 
> is as large as possible. (Some formulations of the problem also allow the empty subarray to be considered; by convention, the sum of all values of the empty subarray is zero.) Each number in the input array $A$ could be positive, negative, or zero.
> 
> *Maximum subarray problem - Wikipedia*

### 符號約定

在以下文章中，非程式碼部份會用 $a_i$ 來代替 $A[i]$，視覺上會比較精簡。

## Θ(n³): 暴力解法

## Θ(n²): 改良版暴力解法

## Θ(n lg n): 分治解法

## Θ(n): 動態規劃解法（Kadane's Algorithm）

### 思路

1. 首先定義一些符號方便討論，令 $S_{i,j}$ 為「一個子數列的和」，即
   
   $$ S_{i,j} = a_i + a_{i+1} + \cdots + a_j $$
   
   其中 $1 \leq i \leq j \leq n$
   
   另外，令 $B_j$ 為「以 $a_j$ 結尾的子數列中最大的和」，即
   
   $$ \begin{align}
   B_j & = \max(\{a_1 + a_2 + \cdots + a_j\}, \{a_2 + \cdots + a_j\}, \cdots, \{a_j\}) \\
   & = \max(S_{1,j}, S_{2,j}, \cdots, S_{j,j})
   \end{align} $$
   
   其中 $1 \leq j \leq n$

2. 接著我們觀察這個問題，可以發現：最大子數列
   
   - 以 $a_1$ 結尾
   - 以 $a_2$ 結尾
   - ...
   - 以 $a_n$ 結尾
   
   以上至少成立一個（若有多個最大子序列則多於一個。允許負數為最大值。），所以
   
   $$ \text{最大子數列和} = \max(B_1, B_2, \cdots, B_n) $$
   
   此部份為 $\Theta(n)$
   
   如果我們可以用 $\Theta(n)$ 求出所有 $B_j$ ，就可以得到 $\Theta(n)$ 的演算法

3. 我們可以從 $B_j$ 求出 $B_{j+1}$，證明如下
   
   $$ \begin{align}
   B_1 & = a_1 \\
   \\
   B_j & = \max(\{a_1 + a_2 + \cdots + a_j\}, \{a_2 + \cdots + a_j\}, \cdots, \{a_j\}) \\
   & = \max(S_{1,j}, S_{2,j}, \cdots, S_{j,j}) \\
   \\
   B_{j+1} & = \max(\{\bbox[silver]{a_1 + a_2 + \cdots + a_j} + a_{j+1}\}, \{\bbox[silver]{a_2 + \cdots + a_j} + a_{j+1}\}, \cdots, \{\bbox[silver]{a_j} + a_{j+1}\}, \{a_{j+1}\}) \\
   & = \max(\{\bbox[silver]{S_{1,j}} + a_{j+1}\}, \{\bbox[silver]{S_{2,j}} + a_{j+1}\}, \cdots, \{\bbox[silver]{S_{j,j}} + a_{j+1}\}, \{a_{j+1}\}) \\
   & = \max(\max(\{\bbox[silver]{S_{1,j}} + a_{j+1}\}, \{\bbox[silver]{S_{2,j}} + a_{j+1}\}, \cdots, \{\bbox[silver]{S_{j,j}} + a_{j+1}\}), \{a_{j+1}\}) \\
   & = \max(\bbox[silver]{\max(S_{1,j}, S_{2,j}, \cdots, S_{j,j})} + a_{j+1}, a_{j+1}) \\
   & = \max(B_j + a_{j+1}, a_{j+1}) \\
   & = \max(B_j, 0) + a_{j+1}
   \end{align} $$
   
   這其中應用到了兩個 $\max$ 函數的性質 $\max(a, b, c) = \max(\max(a, b), c)$ 和 $\max(a+x, b+x, c+x) = \max(a, b, c) + x$
   
   證明完畢，我們確實可以從 $B_j$ 求出 $B_{j+1}$，這也是為什麼它是動態規劃的原因（只是它的最優子結構沒有那麼明顯）

### Kadane's Algorithm

```
Find-Maximum-Subarray(A):
    // 思路第3部份
    Let B[1..n] be a new array
    B[1] = A[1]
    for i = 2 to n
        B[i] = max(B[i-1] + A[i], A[i])
    // 思路第2部份
    max = B[1]
    for i = 2 to n
        if B[i] > max
            max = B[i]
    return max
```

以上是分兩次 `for` 的版本，也可以合併在一起

```
Find-Maximum-Subarray(A):
    max = B = A[1]
    for i = 2 to n
        B = max(B + A[i], A[i])    // 思路第3部份
        if B > max                 // 思路第2部份
            max = B
    return max
```

如果想要知道最大子數列的區間，只須修改如下

```
Find-Maximum-Subarray(A):
    max = B = A[1]
    maxL = maxR = 1
    for i = 2 to n
        B = max(B + A[i], A[i])
        if B > max
            max = B
            maxR = i
            if B == A[i]
                maxL = i
    return (max, maxL, maxR)
```

### 一個實際的例子

假設 $B_5 = a_3 + a_4 + a_5$，則 $B_6 = \max(B_5 + a_6, a_6)$

因為 $B_5$ 是以 $a_5$ 結尾的子數列中和最大的，所以

$$ \begin{align}
\bbox[gray]{a_1+a_2+a_3+a_4+a_5} & < B_5 \\
\bbox[gray]{a_2+a_3+a_4+a_5} & < B_5 \\
\bbox[silver]{a_3+a_4+a_5} & = B_5 \\
\bbox[gray]{a_4+a_5} & < B_5 \\
\bbox[gray]{a_5} & < B_5
\end{align} $$

（為簡化例子，假設沒有 $\leq$ 的情況）

以 $a_6$ 結尾的子數列有以下情況

$$ \begin{align}
\bbox[gray]{a_1+a_2+a_3+a_4+a_5}+a_6 & < B_5 + a_6 \\
\bbox[gray]{a_2+a_3+a_4+a_5}+a_6 & < B_5 + a_6 \\
\bbox[silver]{a_3+a_4+a_5}+a_6 & = B_5 + a_6\\
\bbox[gray]{a_4+a_5}+a_6 & < B_5 + a_6 \\
\bbox[gray]{a_5}+a_6 & < B_5 + a_6 \\
a_6
\end{align} $$

1. 若 $B_5 + a_6 > a_6$，因為 $B_5 + a_6$ 比其它子數列大，得 $B_6 = B_5 + a+6$
   
   但 $a_6$ 和其它子序列哪個比較大則無法得知

2. 若 $a_6 > B_5 + a_6$，因為 $B_5 + a_6$ 比其它子數列大，所以 $a_6$ 是最大的，得 $B_6 = a_6$

### 容易誤解的地方

1. 是否有可能 $a_3 + a_4 + a_5 > a_3 + a_4 + a_5 + a_6$ 且 $a_3 + a_4 + a_5 > a_6$？
   
   有可能，但這只代表 $B_5 > B_6$，$B_6$ 不會因此變為 $a_3 + a_4 + a_5$。
   
   會有這個疑問，是因為誤把 $B_6$（程式碼中的 `B[i]`）當成 $max(B_1, B_2, \cdots, B_6)$（程式碼中的 `max`）。

2. 是否有可能 $a_2 + a_3 + a_4 > a_3 + a_4 + a_5 + a_6$ 且 $a_2 + a_3 + a_4 > a_6$？
   
   與前一點同理，如果成立也只代表 $B_4 \geq a_2 + a_3 + a_4 > B_6$（$\geq$ 是因為無法由題目給的條件得知 $a_1 + a_2 + a_3 + a_4$、$a_3 + a_4$ 和 $a_4$ 是否大於 $a_2 + a_3 + a_4$），不影響 $B_6$

## 參考資料

[最大子數列問題 - 維基百科，自由的百科全書](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E5%88%97%E9%97%AE%E9%A2%98)  
[Maximum subarray problem - Wikipedia](https://en.wikipedia.org/wiki/Maximum_subarray_problem)  
[Dive deep into Kadane’s algorithm​ | thirumal's blog](https://thirumal.blog/2018/03/18/kadane-deep-dive/)