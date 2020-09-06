# [LeetCode] 198. House Robber(未完成)

Dynamic Programming 練習

## 思路

這個問題看起來和 I2A 的 rod cutting 很像，假設 $f(i,j)$ 為 $i$ 號房子到 $j$ 號房子可以搶到的最大值，則一定存在一間中間的房子 $k$ 不能搶（$i\leq k \leq j$），對原問題來說就是要求 $f(1,n)$。

因為左右兩半都必須是最大值，整體才會是最大值，所以符合最優子結構。

因此我們可以列出以下遞迴關係式：

$$ f(i,j)=\begin{cases}
\text{money}[i] & \text{if}\ \ i=j \\
\max_{i\leq k\leq j}(f(i,k-1)+f(k+1,j)) & \text{if}\ \ i<j
\end{cases} $$

其中也可以看出它具有重疊子問題。

## 兩個子問題 + 遞迴 + Memoization 版

``` c
int rob_aux(int* nums, int numsSize, int i, int j, int result[][numsSize]) {
    if(i > j) return 0;
    if(i == j) return nums[i];
    if(result[i][j] != -1) return result[i][j];
    
    int k, max = -1, sum;
    for(k = i; k <= j; k++) {
        sum = rob_aux(nums, numsSize, i, k-1, result) + rob_aux(nums, numsSize, k+1, j, result);
        if(sum > max) max = sum;
    }
    result[i][j] = max;
    return max;
}

int rob(int* nums, int numsSize){
    if(numsSize == 0) return 0;    // 測資裡有空陣列
    
    int result[numsSize][numsSize];
    int i, j;
    for(i = 0; i < numsSize; i++) {
        for(j = 0; j < numsSize; j++) {
            result[i][j] = -1;
        }
    }

    return rob_aux(nums, numsSize, 0, numsSize-1, result);
}
```

Runtime: 24 ms, faster than 5.97% of C online submissions for House Robber.  
Memory Usage: 7 MB, less than 41.25% of C online submissions for House Robber.

雖然看起來時間很多，但如果把第4行的 Memoization 刪掉的話，就會出現 Time Limit Exceeded。
