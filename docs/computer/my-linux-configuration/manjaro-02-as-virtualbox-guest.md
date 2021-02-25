# Manjaro (二) 作為 VirtualBox guest

## VirtualBox 注意事項

1. 安裝時，如果進入 GRUB 後沒畫面，圖形控制器改用 VMSVGA。
2. 安裝後，如果進入 GRUB 後沒畫面，圖形控制器改用 VBoxSVGA。
3. 安裝後，圖形控制器改用 VBoxSVGA 才可以在改變 VirtualBox 視窗大小後自動調整解析度。
4. 安裝後不需要再裝 VirtualBox Guest Additions，Manjaro 已經自動裝好了。
5. 使用共用資料夾，需要把使用者加入 `vboxsf` 群組才有存取權限，執行 `usermod -a -G vboxsf $USER` 後重新登入即可。