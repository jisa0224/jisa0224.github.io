# Manjaro (三) 系統備份：使用 Timeshift

以下進行測試以證實 Timeshift 的還原不會影響到 /home 中的檔案

1.  設定 Timeshift：
    ```
    類型 RSYNC
    位置 sda2(/home)  
    過濾器 新增 /home (注意是「排除」（- 號）！！）
    ```
2.  進行備份，備份後重開機
3.  對系統進行變更
    1. 在 /home/jisa 的不同位置新增有內容的文字檔
    2. `sudo pacman -R firefox`
4.  重開機
5.  進行還原（「選擇目標裝置」和「Bootloader 選項」都使用預設選項，以下為預設選項）  
    選擇目標裝置：
    ```
    /     sda1
    /boot 儲存於根裝置
    /home 儲存於根裝置
    ```
    Bootloader 選項：
    ```
    V （重新）安裝 GRUB2 於 sda (不是 sda1!!)
    X 更新 initramfs
    V 更新 GRUB 選單
    ```
    按下一步後會先有 Dry Run 比較檔案，然後列出會變更的檔案列表，按下一步之後才會開始還原，還原後會自動重開機
6.  重開機後確認 /home/jisa 中的檔案都還在，且 firefox 有在

如果無法進入 X 時的測試：

以下步驟替換第 5 步

`sudo timeshift --list` 可列出 snapshot  
`sudo timeshift --restore` 會跳出所有 snapshot 的列表，選擇 snapshot 後列出還原選項（只有「Bootloader 選項」，沒有「選擇目標裝置」！！），之後就直接還原（沒有 Dry Run！！），還原後自動重開機

與使用 Timeshift GUI 結果相同，重開機後確認 /home/jisa 中的檔案都還在，且 firefox 有在