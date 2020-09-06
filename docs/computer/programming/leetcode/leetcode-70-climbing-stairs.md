# [LeetCode] 70. Climbing Stairs(未完成)

Dynamic Programming 練習

## 思路

假設 $f(n)$ 為爬樓梯方式的數量，則我們可以發現：

$$ f(n)=\begin{cases}
1 & \text{if}\ \  n=1 \\
2 & \text{if}\ \  n=2 \\
f(n-1)+f(n-2) & \text{if}\ \  n>2
\end{cases} $$

等同於 Fibonacci 數列。

## Submission

``` c
int climbStairs(int n){
    int step[n+1];
    if(n == 1) return 1;
    step[0] = 1;
    step[1] = 1;
    
    int i;
    for(i = 2; i <= n; i++) {
        step[i] = step[i-1] + step[i-2];
    }
    return step[n];
}
```

Runtime: 0 ms, faster than 100.00% of C online submissions for Climbing Stairs.  
Memory Usage: 6.9 MB, less than 17.99% of C online submissions for Climbing Stairs.

註：題目不會出現 `n == 0` 的情況，所以回傳 `0` 或 `1` 都沒差，但 `step[0]` 必須等於 `1`，才符合 Fibonacci 數列。

## 優化

既然知道等同於 Fibonacci 數列，就可以省掉 `step[n+1]` 和 `i` 來進行優化。
