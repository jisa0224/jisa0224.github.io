# [LeetCode] 338. Counting Bits(未完成)

Dynamic Programming 練習

## 思路

每個大於1的數字右移之後，都會跟它除以2的結果相同，利用這點再配合奇偶數處理，就可以利用先前計算過的結果。

## Submission

``` c
/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* countBits(int num, int* returnSize){
    int *result = (int *)malloc(sizeof(int) * (num + 1));
    *returnSize = num + 1;
    result[0] = 0;
    if(num == 0) return result;
    result[1] = 1;
    if(num == 1) return result;
    
    int i;
    for(i = 2; i <= num; i++) {
        result[i] = result[i/2] + (i % 2);
    }
    
    return result;
}
```

Runtime: 48 ms, faster than 21.20% of C online submissions for Counting Bits.  
Memory Usage: 11.9 MB, less than 9.52% of C online submissions for Counting Bits.
