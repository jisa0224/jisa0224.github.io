# [LeetCode] 343. Integer Break(未完成)

Dynamic Programming 練習

## 思路

此題和 I2A 的 rod cutting 一樣，可以觀察到符合最優子結構：如果把一個數 $n$ 分成兩半 $k$ 和 $n-k$，那麼 $k \times (n-k)$ 要最大的話，$k$ 和 $n-k$ 也必須要有最大的 Integer Break。

不過此題有個要注意的地方，就是 $n$ 的 Integer Break 可能小於 $n$，例如：

$$ \begin{align}
& 2=1+1 \rightarrow 1 \times 1=1<2 \\
& 3=1+2 \rightarrow 1 \times 2=2
\end{align} $$

而不是直接把 2 的 Integer Break 代入，所以遞迴關係式應該是：

$$ f(n)=\begin{cases}
1 & \text{if}\ \  n=1 \\
1 & \text{if}\ \  n=2 \\
\max\limits_{1\leq k<n}(\max(f(k),k),\max(f(n-k),n-k)) & \text{if}\ \  n>2
\end{cases} $$

由於對稱性，$k$ 只需要檢查到一半即可。

## 兩個子問題的版本

``` c
#define max(a, b) ((a) > (b) ? (a) : (b))

int integerBreak(int n){
    int result[n+1];
    result[0] = 1;
    result[1] = 1;
    
    int i, j, max, sum;
    for(i=2; i<=n; i++) {
        max = -1;
        for(j=1; j<=i/2; j++) {
            sum = max(result[j], j) * max(result[i-j], i-j);
            if(sum > max) max = sum;
        }
        result[i] = max;
    }
    
    return result[n];
}
```

Runtime: 4 ms.  
Memory Usage: 6.6 MB.

## 一個子問題的優化版本

在 I2A 裡，rod cutting 從原本的兩個子問題被優化成了一個子問題，這兩個是等價的，而此題也可以這樣做。

*尚未證明*

``` c
#define max(a, b) ((a) > (b) ? (a) : (b))

int integerBreak(int n){
    int result[n+1];
    result[0] = 1;
    result[1] = 1;
    
    int i, j, max, sum;
    for(i=2; i<=n; i++) {
        max = -1;
        for(j=1; j<=i-1; j++) {
            sum = j * max(result[i-j], i-j);
            if(sum > max) max = sum;
        }
        result[i] = max;
    }
    
    return result[n];
}
```

Runtime: 0 ms, faster than 100.00% of C online submissions for Integer Break.  
Memory Usage: 6.9 MB, less than 28.57% of C online submissions for Integer Break.

雖然 `max()` 少了一半，但因為迴圈次數多了一倍，整體時間應該相同，時間卻從 4 ms 減少到 0 ms 這點還蠻奇怪的。
