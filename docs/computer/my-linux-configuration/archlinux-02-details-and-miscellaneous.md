# Arch Linux (二) 細節與雜項

## 硬體規格

MSI Modern 15 A10M-419TW

* 進入 UEFI 開機選單的方法: 在按下開機鍵後立刻按下 Delete 鍵。
* 硬碟為 2 顆 NVMe SSD (`/dev/nvme0n1` 和 `/dev/nvme1n1`)。
* 顯示卡為內建的 Intel UHD Graphics。

## 安裝至 VirtualBox 作為 Guest

VirtualBox 機器設定如下: 

* 勾選 "啟用 EFI" 及 "硬體時鐘以 UTC 時間"。
* 圖形控制器使用 VMSVGA (如果使用 VBoxSVGA 有時候 host 和 guest 會一起當掉，只能在 host 切換到 VT `kill` VirtualBox，原因不明)。
* 硬碟控制器改成 "NVMe (PCIe)"，硬碟勾選 "固態磁碟機"。

VirtualBox 的 "設定 > 系統 > 開機順序" 是 BIOS 才有效，UEFI 有它自己的開機選單 (進入 UEFI 開機選單的方法: 在啟動虛擬機器後立刻按下 Esc 鍵)。

軟體包: 

* Display drivers 改成裝 xf86-video-vmware open-vm-tools spice-vdagent。
* 輸入加裝 xf86-input-vmmouse
* 加裝 virtualbox-guest-utils
    * `systemctl enable vboxservice`。
    * 使用共用資料夾，需要把使用者加入 `vboxsf` 群組才有存取權限，執行 `usermod -a -G vboxsf $USER` 後重新登入即可。

## SSD 4K 對齊

SSD 進行 4K 對齊 (即每個分割區的開頭都是 4 KiB 或 8 sectors 的倍數) 可提高效率。

較新的磁碟分割程式 (如: fdisk/cfdisk, gparted) 都自動會做對齊 (不管是機械硬碟還是 SSD 都會對齊)。

fdisk/cfdisk 會自動進行對齊，但因為不明原因它進行的是 1MiB 對齊，而不是 4KiB 對齊，所以如果分割區小於 1MiB，跟下一個分割區之間就會留空。

## SSD TRIM

要開啟 TRIM 避免消耗，在磁碟機 mount 選項中加入 `discard`。

參考資料: [Solid state drive (正體中文) - ArchWiki](https://wiki.archlinux.org/index.php/Solid_state_drive_(%E6%AD%A3%E9%AB%94%E4%B8%AD%E6%96%87)#TRIM)

## NVMe SSD 睡死問題

新的電腦使用 NVMe SSD 取代傳統的機械硬碟，原廠電腦有一個硬碟，後來又加購一個。

但在使用時發現，如果將 /home 放在第二個硬碟上，並執行 I/O 頻繁的程式 (如：在 VirtualBox guest 裡執行 Pacman 系統升級，或在 host 安裝 Mathematica)，
host 和 guest 就會直接卡住（但執行中的程式只要不讀取硬碟就可以繼續執行），只能強制重開機。

從 `journalctl` 有發現 `kernel: nvme nvme1: I/O 320 QID 4 timeout, aborting`(數字可能不同)，確定問題出在 NVMe SSD 上。

根據網路資料，確認過不是溫度太高、RAM 用完造成，也更換過一顆新的硬碟，所以問題出在 Linux 上 (因為沒發現 Windows 有這個問題)。

因為可能是 I/O 太頻繁的關係，但之前往硬碟寫了 200 多 GB 的資料也沒事，所以也有可能和 VirtualBox 有關。
根據網路資料，(1) System: 打勾 "Enable I/O APIC" (2) SATA controller: 打勾 "Use host I/O cache" (3) VDI: 打勾 "Solid-state drive"，無效。

根據網路資料，可能是 Linux 的 NVMe 驅動程式中的省電模式有問題，導致硬碟進入省電模式後就無法恢復(睡死)，關掉省電模式就可以解決。

在 Linux kernel options 加上 `nvme_core.default_ps_max_latency_us=0`: 

* GRUB: 編輯 `/etc/default/grub`，在 `GRUB_CMDLINE_LINUX_DEFAULT` 加上 `nvme_core.default_ps_max_latency_us=0`，儲存後執行 `update-grub`。
* systemd-boot: 編輯 `/efi/loader/entries/*.conf`，在 `options` 加上 `nvme_core.default_ps_max_latency_us=0`，儲存後即可。

`cat /sys/module/nvme_core/parameters/default_ps_max_latency_us` 原本 100000，修改後為 0。

經過長期測試發現有效。

參考資料: 

* [Fixing NVME SSD Problems On Linux – TEKBYTE](https://tekbyte.net/2020/fixing-nvme-ssd-problems-on-linux/)
* [完整學習機器學習實錄1——安裝 Ubuntu 18.04 - HackMD](https://hackmd.io/@William-Mou/ryNms2F-E?type=view)

## BIOS 與 UEFI

新的電腦使用 UEFI 取代傳統的 BIOS，UEFI+GPT 分割表需要多分割一個「EFI 系統分割區」(UEFI+MBR 分割表就不需要)，網路建議 EFI 系統分割區至少 512 MB。

參考資料：  
[Partitioning - ArchWiki](https://wiki.archlinux.org/index.php/partitioning#UEFI/GPT_layout_example)  
[EFI system partition - ArchWiki](https://wiki.archlinux.org/index.php/EFI_system_partition#GPT_partitioned_disks)

## Boot Loader

### GRUB

* GRUB (BIOS/MBR)
    * `/boot` 可以位於另外一個分割區，或是和 `/` 同一個分割區。
    * 安裝 grub os-prober。
    * 安裝 Boot Loader 到 MBR: 執行 `grub-install --target=i386-pc /dev/nvme0n1`。
    * 編輯 `/etc/default/grub` 後，執行 `grub-mkconfig -o /boot/grub/grub.cfg`。
      (MBR 裡的 GRUB 會讀取 `/boot/grub` 裡的設定和模組，顯示開機選單。)
    * GRUB 會自動載入 CPU microcode 更新，不須手動設定。

* GRUB (UEFI/GPT)
    * 建立一個 EFI 系統分割區，掛載到 `/efi`。
    * `/boot` 可以位於另外一個分割區，或是和 `/` 同一個分割區。
    * 安裝 efibootmgr grub os-prober。
    * 安裝 EFI bootloader: 執行 `grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=arch_grub`。  
      (GRUB 會往 UEFI NVRAM 裡寫入 boot entry，指向 `/efi/EFI/GRUB/grubx64.efi`。)
    * 編輯 `/etc/default/grub` 後，執行 `grub-mkconfig -o /boot/grub/grub.cfg`。
      (`grubx64.efi` 會讀取 `/boot/grub` 裡的設定和模組，顯示開機選單。)
    * GRUB 會自動載入 CPU microcode 更新，不須手動設定。

### systemd-boot

systemd-boot 只支援 UEFI/GPT，且只支援讀取 FAT32 分割區，因此 Linux 的 kernel (`/boot/vmlinuz-linux`)、
Initramfs 和 CPU microcode 必須全部放在該分割區裡。

* systemd-boot (單 Linux 方案)
    * 建立一個 EFI 系統分割區，掛載到 `/boot`，不需要 `/efi`。
    * systemd-boot 已經包含在 Arch Linux 的 systemd 軟體包裡，不用另外安裝。
    * 安裝 EFI boot manager: 執行 `bootctl install`。  
      (systemd-boot 會往 UEFI NVRAM 裡寫入 boot entry，指向 `/boot/EFI/systemd/systemd-bootx64.efi`。)
    * 編輯 systemd-boot 設定檔 `/boot/loader/loader.conf`。
    * 新增一個 boot entry `/boot/loader/entries/arch.conf`。
    * 如果安裝成功，執行 `bootctl list` 應該會看到上面加入的 boot entry；
      執行 `efibootmgr -v` 應該會看到 "Linux Boot Manager ... File(\EFI\systemd\systemd-bootx64.efi)"
    * 未來如果更新 systemd-boot，需要手動更新 boot manager (執行 `bootctl update`)，
      或者安裝 systemd-boot-pacman-hook@A 自動在更新 systemd-boot 後更新 boot manager。

但因為 Linux 的 kernel 通常都會放在 `/boot` 裡，如果同一顆硬碟上有多個 Linux，可能會把彼此的 kernel 覆蓋掉。
解決方法是給每個 Linux 一個單獨的 `/boot` 分區 (必須是 FAT32)，把 EFI 系統分割區掛載到 `/efi`。或者採用下面的方法。

* systemd-boot (多 Linux 方案)
    * 建立一個 EFI 系統分割區，掛載到 `/efi`。
    * 建立 `/efi/installs/<id>` 資料夾，然後 `mount --bind /efi/installs/<id> /boot`，這樣每個 Linux 都可以把它自己的 kernel 放在自己的資料夾裡。
    * systemd-boot 已經包含在 Arch Linux 的 systemd 軟體包裡，不用另外安裝。
    * 安裝 EFI boot manager: 執行 `bootctl install`。  
      (systemd-boot 會往 UEFI NVRAM 裡寫入 boot entry，指向 `/efi/EFI/systemd/systemd-bootx64.efi`。)
    * 編輯 systemd-boot 設定檔 `/efi/loader/loader.conf`。
    * 新增一個 boot entry `/efi/loader/entries/arch.conf`。
    * 如果安裝成功，執行 `bootctl list` 應該會看到上面加入的 boot entry；
      執行 `efibootmgr -v` 應該會看到 "Linux Boot Manager ... File(\EFI\systemd\systemd-bootx64.efi)"
    * 未來如果更新 systemd-boot，需要手動更新 boot manager (執行 `bootctl update`)，
      或者安裝 systemd-boot-pacman-hook@A 自動在更新 systemd-boot 後更新 boot manager。

備註：之後開機時如果要進 Live CD，必須 (1) 直接從機器提供的 UEFI 選單進入 (VirtualBox 是在啟動後馬上按 Esc 鍵)，
或者 (2) 從 systemd-boot 的 "Reboot Into Firmware Interface" (不一定有此項目) 進入機器提供的 UEFI 選單，然後選擇 Live CD。

備註：在 boot entry 上按 `e` 可以編輯 kernel options (只有本次開機會生效，不會儲存)，
像是加上 `rw init=/bin/bash` 可以在忘記密碼時進行救援 (關機必須用 `poweroff -f`，重新開機必須用 `reboot -f`)。

備註：VirtualBox guest 中 kernel options 如果加上 `quiet` 有時候會在開機時卡住，原因不明 (可能是因為用了 proprietery display driver?)。

參考資料: 

* [systemd-boot - ArchWiki](https://wiki.archlinux.org/index.php/Systemd-boot)
* [Multi Boot Linux With One Boot Partition | John Ramsden](https://ramsdenj.com/2016/04/15/multi-boot-linux-with-one-boot-partition.html)
* [\[SOLVED\]How to Uninstall GRUB and Install reFInd? / Newbie Corner / Arch Linux Forums](https://bbs.archlinux.org/viewtopic.php?id=243870)
* [Efibootmgr - Gentoo Wiki](https://wiki.gentoo.org/wiki/Efibootmgr)
* [Reset lost root password - ArchWiki](https://wiki.archlinux.org/index.php/Reset_lost_root_password)
* [How to Boot Arch Linux in Single User Mode / Rescue Mode](https://www.linuxtechi.com/boot-arch-linux-single-user-mode-rescue-mode/)

## 環境變數

環境變數到底放哪裡？

<../linux/etc-environment-environment-variables-for-all-program.md>

`/etc/environment`: The environment variables config file，參考 `man pam_env.conf`

雖然最好不要修改系統檔案，但因為 (1) root 不會讀取 `/root/.pam_environment` (2) `~/.pam_environment` 未來會被廢棄 (3) pam_env 是設定環境變數唯一 shell/GUI-agnostic 的方式，所以只能這麼做。

## ~/.cache

* `~/.cache` 底下的快取檔刪除不影響系統和程式運作，它們會自己重新快取。
* Qt 會在 `~/.cache` 裡放一大堆 QML 的快取，但即使是不再使用的 QML 程式，它也不會自己刪除快取！  
  可以在 `/etc/environment` 加入 `QML_DISK_CACHE_PATH=/tmp/QtQmlDiskCache_jisa`，把快取放到 tmpfs 上，每次關機自動清理，
  雖然重開機後第一次啟動 QML 程式會比較慢(其實感覺不太出來)，但是之後因為快取位於 tmpfs 上，反而會比較快；
  或是改成加入 `QML_DISABLE_DISK_CACHE=1`，完全關閉快取。  
  參考資料：[The QML Disk Cache | Qt QML 5.15.3](https://doc-snapshots.qt.io/qt5-5.15/qmldiskcache.html)

## 使用 Timeshift 進行系統備份

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