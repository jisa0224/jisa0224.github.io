# Arch Linux (二) 細節與雜項

## 硬體規格

MSI Modern 15 A10M-419TW

## 安裝至 VirtualBox 作為 Guest

* VirtualBox guest: virtualbox-guest-utils
    * `systemctl enable vboxservice`
    * 使用共用資料夾，需要把使用者加入 `vboxsf` 群組才有存取權限，執行 `sudo gpasswd -a $USER vboxsf` 後重新登入即可
* Display drivers(VirtualBox guest): virtualbox-guest-utils xf86-video-vmware open-vm-tools spice-vdagent
* 輸入(VirtualBox guest): xf86-input-vmmouse

## SSD 4K 對齊

SSD 進行 4K 對齊 (即每個分割區的開頭都是 4 KiB 或 8 sectors 的倍數) 可提高效率。

較新的磁碟分割程式 (如: fdisk/cfdisk, gparted) 都自動會做對齊 (不管是機械硬碟還是 SSD 都會對齊)。

fdisk/cfdisk 會自動進行對齊，但因為不明原因它進行的是 1MiB 對齊，而不是 4KiB 對齊，所以如果分割區小於 1MiB，跟下一個分割區之間就會留空。

## SSD TRIM

## NVMe SSD 睡死問題

## BIOS 與 UEFI

建立 EFI System Partition: [EFI system partition - ArchWiki](https://wiki.archlinux.org/index.php/EFI_system_partition)

## Boot Loader

## 環境變數

## ~/.cache

## 使用 Timeshift 進行系統備份