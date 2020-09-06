# 用 dd 製作出可開機 USB

1.  首先我們要先確認要使用的隨身碟「裝置名稱」。請插入 USB 隨身碟，<span style="color: #ff6600;">切記不要掛載隨身碟</span>！開啟終端機，輸入`lsblk`指令確認隨身碟裝置名稱。範例如下：  
    
    ```
    [carolus@magnus ~]$ lsblk 
    NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda      8:0    0 465.8G  0 disk 
    ├─sda1   8:1    0   512M  0 part /boot
    ├─sda2   8:2    0    10G  0 part /
    └─sda3   8:3    0 455.3G  0 part /home
    sdb      8:16   1   3.8G  0 disk 
    └─sdb1   8:17   1   3.8G  0 part 
    sr0     11:0    1  1024M  0 rom 
    ```
    
    由以上可知，範例的 USB 隨身碟的裝置名稱為`sdb`。

2.  在終端機，輸入`dd`指令：
    
    ``` shell
    sudo dd if=/映像檔的路徑/映像檔檔名 of=/dev/隨身碟裝置名稱
    ```
    
    **請注意 dd 寫入時需寫入整個裝置（/dev/sdb）而不是裝置中的分區（/dev/sdb1）。**  
    (可能是因為要把 boot loader 寫入隨身碟的 MBR 吧。)
    
    <span style="color: #008000;">正確</span>：<code>sudo dd if=/home/trajan/chakra-2016.02-ian-x86\_64.iso of=<span style="color: #008000;">/dev/sdb</span></code>  
    <span style="color: #ff0000;">錯誤</span>：<code>sudo dd if=/home/trajan/chakra-2016.02-ian-x86\_64.iso of=<span style="color: #ff0000;">/dev/sdb1</span></code>

3.  寫入映像檔會需要一段不短的時間，這時畫面不會有任何變化，請不要以為程式當掉喔！結束時會出現類似以下訊息：
    
    ```
    4210560+0 records in
    4210560+0 records out
    2155806720 bytes (2.2 GB) copied, 768.018 s, 2.8 MB/s
    ```

資料來源：[dd 指令製作 Live USB 教學](https://chakra-zh.blogspot.tw/2012/04/dd-live-usb.html)
 
