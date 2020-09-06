# 為什麼使用 sudo 仍得到 Permission denied？

發生這種情況多半是發生在使用了 Shell 的重定向(redirection)，也就是 `>`，理由很簡單，因為重定向不是由 `sudo` 負責的，而是**由 Shell 負責**的，所以

``` shell
sudo ls > /root/test
```

其實應該看成 <code><span style="color: #ff0000;">sudo ls</span>&nbsp;<span style="color: #00ff00;">&gt;</span>&nbsp;<span style="color: #0000ff;">/root/test</span></code> 而不是 <code><span style="color: #ff0000;">sudo</span>&nbsp;<span style="color: #0000ff;">ls &gt; /root/test</span></code>  
那麼有被 `sudo` 到的只有 `ls`，而重定向(也就是 `bash`)當然沒有權限寫入 `/root/test`  
  
解決方法有以下幾種

1.  使用 `sh -c`  
    
    ``` shell
    sudo sh -c 'ls > /root/test'
    ```

2.  使用管道(pipe) 和 `tee`  
    tee - read from standard input and write to standard output and files
    
    ``` shell
    ls | sudo tee /root/test > /dev/null
    ```
    
    `/dev/null` 是避免 `tee` 再輸出到螢幕上

3.  使用 `sudo -s` 或 `sudo -i`
    
    ``` shell
    sudo -s
    ls > /root/test
    ```
    
    另外還有一個 `sudo -i`，可以用 login shell (所以會讀取 `.profile`)，並跳至 root 的家目錄，但在此例中因為 `ls` 的目標是我的家目錄，所以只能用 `sudo -s`。

參考資料：  
[command line - When using sudo with redirection, I get 'permission denied' - Ask Ubuntu](https://askubuntu.com/questions/230476/when-using-sudo-with-redirection-i-get-permission-denied/230482#230482)  
[避免’sudo echo x \>’ 时’Permission denied’ - CSDN博客](https://blog.csdn.net/hejinjing_tom_com/article/details/7767127)
 
