# 睡眠排序 Sleep Sort

最早出現在 [Genius sorting algorithm: Sleep sort](https://archive.tinychan.org/read/prog/1295544154) 這個帖子。

``` shell
#!/bin/bash
function f() {
    sleep "$1"
    echo "$1"
}
while [ -n "$1" ]
do
    f "$1" &
    shift
done
wait
```

example usage:

``` shell
./sleepsort.sh 5 3 6 3 6 3 1 4 7
```

1. 構造n個線程，它們和這n個數一一對應。
2. 初始化後，線程們開始睡眠，等到對應的數那麼多個時間單位後各自醒來，然後輸出它對應的數。
3. 這樣最小的數對應的線程最早醒來，這個數最早被輸出。
4. 等所有線程都醒來，排序就結束了。

參考資料：  
[排序算法--睡眠排序、面条排序、猴子排序 (非常严肃) - 曾会玩 - 简书](https://www.jianshu.com/p/4f526ea40df4)  
[天才排序算法：睡眠排序 - 人在江湖 - CSDN博客](https://blog.csdn.net/zmazon/article/details/8514088)