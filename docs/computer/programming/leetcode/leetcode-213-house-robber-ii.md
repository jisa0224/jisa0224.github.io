# [LeetCode] 213. House Robber II(未完成)

Dynamic Programming 練習

## 思路

跟 <a href='{% post_path "LeetCode-198-House-Robber" %}' target='_blank' rel='noopener'>[LeetCode] 198. House Robber</a> 的演算法相同，幾乎不需要修改，只須針對環形部份修正即可。

環形的關鍵在於：如果第一個有搶，最後一個就不能搶，相當於 $f(1,n-1)$；如果最後一個有搶，第一個就不能搶，相當於 $f(2,n)$，所以我們只需要找出

$$ \max(f(1,n-1),f(2,n)) $$

不過這個方法雖然可以通過，卻沒有嚴謹的證明，只能算是直覺而已（我感覺好像有例外，但又想不到）。

## Submission

``` c hl_lines="17 27 28 29"
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
    if(numsSize == 0) return 0;
    if(numsSize == 1) return nums[0];    // 只有一筆資料時，rob_aux 返回 0
    
    int result[numsSize][numsSize];
    int i, j;
    for(i = 0; i < numsSize; i++) {
        for(j = 0; j < numsSize; j++) {
            result[i][j] = -1;
        }
    }

    int without_last = rob_aux(nums, numsSize, 0, numsSize-1-1, result);
    int without_first = rob_aux(nums, numsSize, 1, numsSize-1, result);
    return without_last > without_first ? without_last : without_first;
}
```

Runtime: 16 ms, faster than 11.11% of C online submissions for House Robber II.  
Memory Usage: 7.2 MB, less than 25.00% of C online submissions for House Robber II.