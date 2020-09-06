# [LeetCode] 1. Two Sum(未完成)

## 思路



## Submission

``` c
void sort(int arr[], int n, int index[]) {
    int i, j;
    for(i=0; i<n; i++) index[i] = i;
    
    /* insertion sort */
    for(i=1; i<n; i++) {
        int now = arr[i];
        for(j=i; (j>0) && (arr[j-1] > now); j--) {
            arr[j] = arr[j-1];
            index[j] = index[j-1];
        }
        arr[j] = now;
        index[j] = i;
    }
}

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize){
    int indexBeforeSort[numsSize];
    sort(nums, numsSize, indexBeforeSort);
    
    int i = 0, j = numsSize - 1;
    while(i < j) {
        int sum = nums[i] + nums[j];
        if(sum == target) break;
        if(sum > target) j--;
        if(sum < target) i++;
    }
    
    *returnSize = 2;
    int *result = (int *)malloc(sizeof(int) * 2);
    /* 題目說一定存在唯一一個解，所以一定是 i < j，其它狀況省略 */
    result[0] = indexBeforeSort[i];
    result[1] = indexBeforeSort[j];
    return result;
}
```

Runtime: 8 ms, faster than 94.41% of C online submissions for Two Sum.  
Memory Usage: 7.7 MB, less than 26.11% of C online submissions for Two Sum.

## I2A 解答版


