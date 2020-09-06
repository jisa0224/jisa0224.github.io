# [LeetCode] 747. Largest Number At Least Twice of Others(未完成)

## 初次 Submission

``` c
int dominantIndex(int* nums, int numsSize){
    if(numsSize == 1)
        return 0;
    
    int largestId, secondLargestId;
    
    if(nums[0] > nums[1]) {
        largestId = 0;
        secondLargestId = 1;
    } else {
        largestId = 1;
        secondLargestId = 0;
    }
    
    int i;
    for(i = 2; i < numsSize; i++) {
        if(nums[i] > nums[largestId]) {
            secondLargestId = largestId;
            largestId = i;
        } else if(nums[i] > nums[secondLargestId]) {
            secondLargestId = i;
        }
    }
    
    if(nums[largestId] >= nums[secondLargestId] * 2)
        return largestId;
    else
        return -1;
}
```

Runtime: 4 ms, faster than 83.77% of C online submissions for Largest Number At Least Twice of Others.  
Memory Usage: 6.9 MB, less than 18.87% of C online submissions for Largest Number At Least Twice of Others.

## 優化 if 順序

我認為大部分的情況都不會更換 `largestId` 和 `secondLargestId`，因此改變 `if` 順序看會不會比較快。

``` c
int dominantIndex(int* nums, int numsSize){
    if(numsSize == 1)
        return 0;
    
    int largestId, secondLargestId;
    
    if(nums[0] > nums[1]) {
        largestId = 0;
        secondLargestId = 1;
    } else {
        largestId = 1;
        secondLargestId = 0;
    }
    
    int i;
    for(i = 2; i < numsSize; i++) {
        if(nums[i] <= nums[secondLargestId]) {
            // do nothing
        } else if(nums[i] > nums[largestId]) {
            secondLargestId = largestId;
            largestId = i;
        } else if(nums[i] > nums[secondLargestId]) {
            secondLargestId = i;
        }
    }
    
    if(nums[largestId] >= nums[secondLargestId] * 2)
        return largestId;
    else
        return -1;
}
```

Runtime: 8 ms, faster than 12.99% of C online submissions for Largest Number At Least Twice of Others.  
Memory Usage: 7 MB, less than 15.09% of C online submissions for Largest Number At Least Twice of Others.

結果還更慢。

## 標準解答

``` c
int dominantIndex(int* nums, int numsSize){
    int largestId = 0;
    int i;
    for(i = 1; i < numsSize; i++)
        if(nums[i] > nums[largestId])
            largestId = i;
    for(i = 0; i < numsSize; i++)
        if(i != largestId && nums[i] * 2 > nums[largestId])
            return -1;
    return largestId;
}
```

Runtime: 4 ms, faster than 83.77% of C online submissions for Largest Number At Least Twice of Others.  
Memory Usage: 7 MB, less than 15.09% of C online submissions for Largest Number At Least Twice of Others.

標準解答和討論區的解答用的就是我用的這兩種，但不知道為什麼有的人可以用到 0 ms。

## 成功 0 ms

根據初次 Submission 減少陣列取值。

``` c
int dominantIndex(int* nums, int numsSize){
    if(numsSize == 1)
        return 0;
    
    int largestId, secondLargestId;
    
    if(nums[0] > nums[1]) {
        largestId = 0;
        secondLargestId = 1;
    } else {
        largestId = 1;
        secondLargestId = 0;
    }
    
    int largestValue = nums[largestId];
    int secondLargestValue = nums[secondLargestId];
    
    int i;
    for(i = 2; i < numsSize; i++) {
        if(nums[i] > largestValue) {
            secondLargestId = largestId;
            secondLargestValue = nums[secondLargestId];
            largestId = i;
            largestValue = nums[largestId];
        } else if(nums[i] > secondLargestValue) {
            secondLargestId = i;
            secondLargestValue = nums[secondLargestId];
        }
    }
    
    if(largestValue >= secondLargestValue * 2)
        return largestId;
    else
        return -1;
}
```

Runtime: 0 ms, faster than 100.00% of C online submissions for Largest Number At Least Twice of Others.  
Memory Usage: 7 MB, less than 16.98% of C online submissions for Largest Number At Least Twice of Others.
 
