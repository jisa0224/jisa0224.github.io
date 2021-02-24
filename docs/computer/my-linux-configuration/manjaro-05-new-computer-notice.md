# Manjaro (五) 新電腦注意事項

## NVMe SSD 問題

新的電腦使用 NVMe SSD 取代傳統的機械硬碟，原廠電腦有一個硬碟，後來又加購一個。

但在使用時發現，如果將 /home 放在第二個硬碟上，並執行 I/O 頻繁的程式（如：在 VirtualBox guest 裡執行 Pacman 系統升級，或在 host 安裝 Mathematica），
host 和 guest 就會直接卡住（但執行中的程式只要不讀取硬碟就可以繼續執行），只能強制重開機。

從 `journalctl` 有發現 `kernel: nvme nvme1: I/O 320 QID 4 timeout, aborting`(數字可能不同)，確定問題出在 NVMe SSD 上。

根據網路資料，確認過不是溫度太高、RAM 用完造成，也更換過一顆新的硬碟，所以問題出在 Linux 上（因為沒發現 Windows 有這個問題）。

因為可能是 I/O 太頻繁的關係，但之前往硬碟寫了 200 多 GB 的資料也沒事，所以也有可能和 VirtualBox 有關。
根據網路資料，(1) System: 打勾 "Enable I/O APIC" (2) SATA controller: 打勾 "Use host I/O cache" (3) VDI: 打勾 "Solid-state drive"，無效。

根據網路資料，可能是 Linux 的 NVMe 驅動程式中的省電模式有問題，關掉省電模式就可以解決。
編輯 `/etc/default/grub`，在 `GRUB_CMDLINE_LINUX_DEFAULT` 加上 `nvme_core.default_ps_max_latency_us=0`，儲存後執行 `update-grub`。
`cat /sys/module/nvme_core/parameters/default_ps_max_latency_us` 原本 100000，修改後為 0。
經過長期測試發現有效。

參考資料：  
[Fixing NVME SSD Problems On Linux – TEKBYTE](https://tekbyte.net/2020/fixing-nvme-ssd-problems-on-linux/)  
[完整學習機器學習實錄1——安裝 Ubuntu 18.04 - HackMD](https://hackmd.io/@William-Mou/ryNms2F-E?type=view)

## Linux + SSD

要開啟 TRIM 避免消耗，在磁碟機 mount 選項中加入 `discard`。

參考資料：  
[Solid state drive (正體中文) - ArchWiki](https://wiki.archlinux.org/index.php/Solid_state_drive_(%E6%AD%A3%E9%AB%94%E4%B8%AD%E6%96%87)#TRIM)

## UEFI + GPT

新的電腦使用 UEFI 取代傳統的 BIOS，UEFI+GPT 分割表需要多分割一個「EFI 系統分割區」（UEFI+MBR 分割表就不需要），網路建議 EFI 系統分割區至少 512 MB。
使用 parted 的操作方式見下方。

參考資料：  
[Partitioning - ArchWiki](https://wiki.archlinux.org/index.php/partitioning#UEFI/GPT_layout_example)  
[EFI system partition - ArchWiki](https://wiki.archlinux.org/index.php/EFI_system_partition#GPT_partitioned_disks)