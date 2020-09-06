# [LeetCode] 88. Merge Sorted Array(未完成)

## 思路

倒著放。

不用擔心 `nums2` 的元素會覆蓋到 `nums1` 的元素，因為 `nums1` 的空間一定大於等於 `m + n`，所以全部的 `nums2` 都塞到 `nums1` 後面是可以的。

如果後面有出現一個 `nums1` 的元素，那一定是從 `nums1` 的最後面拿的，拿走之後的空位剛好可以補一個 `nums2`，依此類推。

## 初次 Submission

``` c
void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n){
    int i;
    for(i = m + n - 1; m > 0 && n > 0; i--) {
        if(nums2[n-1] > nums1[m-1]) {
            nums1[i] = nums2[n-1];
            n--;
        } else {
            nums1[i] = nums1[m-1];
            m--;
        }
    }
    if(n) {
        for(; n > 0; n--)
            nums1[n-1] = nums2[n-1];
    }
}
```

Runtime: 8 ms, faster than 17.94% of C online submissions for Merge Sorted Array.  
Memory Usage: 7.2 MB, less than 64.45% of C online submissions for Merge Sorted Array.

## 合併迴圈

參考 0 ms 的解法，是把最後面的 `if(n)` 部份給放到前面的 `for` 裡。

``` c
void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n){
    int i;
    for(i = m + n - 1; i >= 0; i--) {
        if((m > 0 && n > 0 && nums2[n-1] > nums1[m-1]) || (m == 0)) {
            nums1[i] = nums2[n-1];
            n--;
        } else {
            nums1[i] = nums1[m-1];
            m--;
        }
    }
}
```

Runtime: 12 ms, faster than 17.94% of C online submissions for Merge Sorted Array.  
Memory Usage: 7.2 MB, less than 64.45% of C online submissions for Merge Sorted Array.

沒有比較快。

## 改用指標操作

改用指標操作可以減少 `-1` 和取值的時間。

``` c
void merge(int* nums1, int nums1Size, int m, int* nums2, int nums2Size, int n){
    int *ptrAll = &(nums1[m + n - 1]);
    int *ptr1 = &(nums1[m - 1]);
    int *ptr2 = &(nums2[n - 1]);
    for(; ptrAll >= nums1; ptrAll--) {
        if((ptr1 >= nums1 && ptr2 >= nums2 && *ptr2 > *ptr1) || (ptr1 < nums1)) {
            *ptrAll = *ptr2;
            ptr2--;
        } else {
            *ptrAll = *ptr1;
            ptr1--;
        }
    }
}
```

Runtime: 4 ms, faster than 90.63% of C online submissions for Merge Sorted Array.  
Memory Usage: 7.3 MB, less than 21.74% of C online submissions for Merge Sorted Array.

確實有比較快，但就沒有那麼一目了然。