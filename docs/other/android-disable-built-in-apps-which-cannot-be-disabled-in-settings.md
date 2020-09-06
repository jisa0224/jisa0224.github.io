# 停用無法停用的 Android 內建 App

目標

1. Sony 的 What's New (com.sonymobile.entrance) 停用後想把它刪除或停用，但無法停用
2. 停用「軟體更新」(com.sonyericsson.updatecenter)以避免其跳出更新通知

使用 adb

1. pm disable
    
    ```
    $ pm disable com.sonymobile.entrance
    Error: java.lang.SecurityException: Shell cannot change component state for com.sonymobile.entrance/null to 2
    
    $ pm disable --user 0 com.sonymobile.entrance
    Error: java.lang.SecurityException: Shell cannot change component state for com.sonymobile.entrance/null to 2
    ```
    
    無效

2. pm uninstall
    
    ```
    $ pm uninstall -k --user 0 com.sonymobile.entrance
    Success
    ```
    
    手機顯示「這位使用者並未安裝」，且無法從手機啟用
    
    未測試過有沒有 `-k` 差在哪裡
    
    ```
    $ cmd package install-existing com.sonymobile.entrance
    Package com.sonymobile.entrance installed for user: 0
    ```
    
    還原可用 install-existing

3. pm disable-user
    
    ```
    $ pm disable-user com.sonymobile.entrance
    Package com.sonymobile.entrance new state: disabled-user
    ```
    
    手機顯示「已停用」，且無法從手機啟用
    
    ```
    $ pm disable-user --user 0 com.sonymobile.entrance
    Package com.sonymobile.entrance new state: disabled-user
    ```
    
    手機顯示「已停用」，且無法從手機啟用，結果跟沒加 `--user 0` 一樣
    
    ```
    $ pm enable com.sonymobile.entrance
    Package com.sonymobile.entrance new state: enabled
    ```
    
    可用 pm enable 啟用

參考資料：[Android adb shell 删除内置应用（魅蓝metal）_Android_闫珂的博客](https://yanke.info/?id=102)