# Arch Linux (一) 安裝、設定與軟體包

命令和程式碼中帶有 `<>` 的選項，請自行替換。

## 安裝

以下安裝至 [MSI Modern 15 A10M-419TW][HWSpec] ([安裝至 VirtualBox 作為 Guest 參考此篇][VBoxGuest])。

Boot Loader 採用 systemd-boot 多 Linux 方案。

1.  下載 Arch Linux 安裝光碟，並寫入 USB 隨身碟 (使用...) 或燒錄至光碟。
2.  到電腦的 UEFI Boot Manager 設定以該 USB 隨身碟或光碟開機，開機後會自動以 root 登入。
3.  預設 keyboard layout 為 US，需要的話進行調整。
4.  確認是否以 UEFI 開機: 執行 `[ -d /sys/firmware/efi/efivars ] && echo "booted in UEFI mode" || echo "booted in BIOS (or CSM) mode"`。
5.  連線到網際網路。
6.  更新系統時間: 執行 `timedatectl set-ntp true`。
7.  分割磁碟: 執行 `cfdisk /dev/nvme0n1`，建立 GPT 分割表，第一個分區[建立 EFI 系統分割區][BIOS/UEFI]，大小至少 512MiB，Type 選 "EFI System"，
    之後建立其它分割區 (ext4 分割區的 Type 選預設的 "Linux filesystem"。)  
    (cfdisk 跟 fdisk 功能一樣，但是有比較好用的類圖形界面。)  
    (用 parted 分割 GPT 會偷偷加上 partition name (是存在 GPT 裡的名字，不是各分割區自己的 label，後者可用 e2label 查看)，因此改用 fdisk/cfdisk)  
    ([SSD 4K 對齊][SSD4KAlign])
8.  格式化磁碟分區
    ```
    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 /dev/nvme0n1p2
    mkfs.ext4 /dev/nvme0n1p3
    ```
    ([建立 EFI 系統分割區][BIOS/UEFI])
9.  掛載新安裝的系統的磁碟分區
    ```
    mount /dev/nvme0n1p2 /mnt -o discard
    mkdir -p /mnt/efi /mnt/efi/installs/arch /mnt/home
    mount /dev/nvme0n1p1 /mnt/efi -o discard
    mount --bind /mnt/efi/installs/arch /mnt/boot
    mount /dev/nvme0n1p3 /mnt/home -o discard
    ```
    (`-o discard` 是為了開啟 [SSD TRIM][SSDTRIM])
10. 安裝最小可用系統: 執行 `pacstrap /mnt base linux linux-firmware`。
11. 安裝其它軟體包 (見下面章節)，可以
    * 繼續用 `pacstrap` 安裝。
    * 等一下 chroot 進新安裝的系統裡用 `pacman` 安裝。
    * 重開機進入新安裝的系統裡用 `pacman` 安裝。
    (不管選擇什麼時候裝，至少分類在 "基本"、"開機" 和 "網路" 的軟體包必須裝上)
12. 產生 fstab: 執行 `genfstab -U /mnt | sed 's|/mnt/efi/installs/arch|/efi/installs/arch|g' >> /mnt/etc/fstab`
13. chroot 進新安裝的系統，執行 `arch-chroot /mnt`，**以下位於 chroot 裡的命令會以 "(in chroot)" 開頭**。
14. (in chroot) 設定系統時間
    * 執行 `ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime`。
    * 執行 `timedatectl set-ntp true`。
15. (in chroot) 設定語言及地區
    * uncomment `/etc/locale.gen` 裡的 `en_US.UTF-8 UTF-8` 和 `zh_TW.UTF-8 UTF-8` 後，執行 `locale-gen`。
    * 執行 `echo LANG=en_US.UTF-8 > /etc/locale.conf`。
    * 如果前面有修改 keyboard layout，編輯 `/etc/vconsole.conf`。
16. (in chroot) 設定網路
    * 執行 `echo <hostname> > /etc/hostname`。
    * 執行 `echo '127.0.0.1    localhost' >> /etc/hosts`。
    * 執行 `echo '::1          localhost' >> /etc/hosts`。
    * 執行 `systemctl enable NetworkManager`。
17. (in chroot) 建立 Initramfs: 執行 `mkinitcpio -P`  
    <https://wiki.archlinux.org/index.php/Mkinitcpio#Possibly_missing_firmware_for_module_XXXX>  
    `wd719x` 和 `aic94xx` 是 SCSI 的 firmware，一般電腦沒有。`xhci_pci` 是 USB 3.0 的 firmware。（？？？）
18. (in chroot) 設定 root 密碼: 執行 `passwd`。
19. (in chroot) 安裝 Boot Loader (採用 systemd-boot 多 Linux 方案)
    * systemd-boot 已經包含在 Arch Linux 的 systemd 軟體包裡，不用另外安裝。
    * 安裝 EFI boot manager: 執行 `bootctl install`。
    * 編輯 systemd-boot 設定檔 `/efi/loader/loader.conf`。
      ```
      default arch.conf
      timeout 5
      ```
    * 新增一個 boot entry `/efi/loader/entries/arch.conf`。
      ```
      title Arch Linux
      linux /installs/arch/vmlinuz-linux
      initrd /installs/arch/intel-ucode.img
      initrd /installs/arch/initramfs-linux.img
      options root=UUID=<執行 `lsblk -f` 找出 UUID> rw nvme_core.default_ps_max_latency_us=0
      ```
    * 如果安裝成功，執行 `bootctl list` 應該會看到上面加入的 boot entry；
      執行 `efibootmgr -v` 應該會看到 "Linux Boot Manager ... File(\EFI\systemd\systemd-bootx64.efi)"
    * 未來如果更新 systemd-boot，需要手動更新 boot manager (執行 `bootctl update`)，
      或者安裝 systemd-boot-pacman-hook@A 自動在更新 systemd-boot 後更新 boot manager。
    * [systemd-boot - ArchWiki](https://wiki.archlinux.org/index.php/Systemd-boot)
    * `nvme_core.default_ps_max_latency_us=0` 是為了[修正 NVMe SSD 睡死問題][NVMeProblem]。
20. (in chroot) 離開 chroot，執行 `exit` 或按下 `Ctrl+D`。
21. 卸載新安裝的系統的磁碟分區: 執行 `umount -R /mnt`。
22. 執行 `poweroff` 關機，最後退出安裝媒體，下次開機就會進入新安裝的系統。

參考資料: 
* [Installation guide - ArchWiki](https://wiki.archlinux.org/index.php/installation_guide)
* [General recommendations - ArchWiki](https://wiki.archlinux.org/index.php/General_recommendations)
* Display drivers 參考 Manjaro Architect 自動安裝的軟體包

## 設定

以下在新安裝的系統執行。

* 系統設定
    * (以 root 登入) 建立一般使用者並開啟 sudo
        * 執行 `useradd -m -G <additional_groups> -s <login_shell> <username>` (`<login_shell>` 必須存在於 `/etc/shells`)，
          然後執行 `passwd <username>` 設定密碼。
        * 執行 `EDITOR=nvim visudo` 並 uncomment `%wheel ALL=(ALL) ALL`，然後把使用者加入該群組 `usermod -a -G wheel <username>`。
        * 調整 sudo timeout，讓 sudo 不用隔一段時間重新輸入密碼: 執行 `EDITOR=nvim visudo -f /etc/sudoers.d/<username>`，
          加入 `Defaults timestamp_timeout=-1` 後儲存離開。
    * 開機時進入圖形界面: 執行 `systemctl enable sddm`。
    * 解決關機時出現 `A stop job is running for ... (... / 1min 30s)`，需要等待很長時間的問題: 
      於 `/etc/systemd/system.conf` 中修改或加入 `DefaultTimeoutStopSec=10s`，儲存後重開機。  
      參考資料：[systemd - A stop job is running for Session c2 of user - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/273876/a-stop-job-is-running-for-session-c2-of-user)
    * 系統安裝完後，systemd 的藍牙服務未開啟: 執行 `sudo systemctl enable bluetooth` 設定開機後自動啟動藍牙服務。
* 使用者設定
    * 環境變數設定
    * 由於許多程式都會在 `~/.cache` 快取，卻不會自動清理不再使用的快取，因此把它掛載為 tmpfs，每次關機自動清理:   
      在不登入的情況下清空 `~/.cache`，然後在 `/etc/fstab` 中加入 `tmpfs /home/jisa/.cache tmpfs rw,nosuid,nodev,relatime,size=50%,mode=755,uid=1000,gid=1000 0 0`，儲存後重開機。  
      (雖然重開機後第一次執行程式會比較慢(其實感覺不太出來)，但是之後因為快取位於 tmpfs 上，反而會比較快。)
* 桌面環境 (KDE) 設定
    * 設定語言及地區
        * 到 System Settings > Regional Settings > Language 加入"繁體中文"，並移到最上面  
        * 到 System Settings > Regional Settings > Formats 改為"台灣 - 繁體中文"  
        * 這兩個會修改 `~/.config/plasma-localerc`，不會修改其它檔案 (像是 `/etc/locale.conf` 或 `~/.config/locale.conf`)，
          所以用 VT 的時候 locale 還是 `/etc/locale.conf` 指定的 `en_US.UTF-8`
    * 設定 KDE Plasma 外觀
        * 設定 Plasma Style 為 Breeze Dark  
        * 設定 Colors 為 Breeze
    * disable kwallet, baloo
    * 字型設定
* Shell 設定

## 軟體包

* 更新 mirror: 執行 ...
* 軟體包名稱沒有後綴的來自 Arch Linux 官方軟體庫，有 `@A` 後綴的來自 Arch User Repository (AUR)，
  有 `@M` 後綴的來自 Manjaro 官方軟體庫 (用手動下載而非加入 pacman 的 mirror)，有 `@O` 後綴的代表其它安裝方式。

---

* 基本
    * 最小可用: base linux linux-firmware  
      (base package group 包含 bash bzip2 coreutils file filesystem findutils gawk gcc-libs gettext glibc grep gzip iproute2 iputils licenses pacman pciutils procps-ng psmisc sed shadow systemd systemd-sysvcompat tar util-linux xz)
    * 基本工具: bash-completion diffutils less lsb-release man-db neovim rsync tree wget which xdg-user-dirs xdg-utils
    * 檔案系統: dosfstools e2fsprogs exfat-utils ntfs-3g
    * 管理工具: htop lsof polkit procps-ng psmisc sudo usbutils

* 開機
    * CPU microcode: intel-ucode
    * Bootloader: efibootmgr systemd-boot-pacman-hook@A

* 網路
    * 網路管理: networkmanager ppp ufw
      (NetworkManager 內建 DHCP client，不須另外安裝 dhclient 或 dhcpcd。)
      (需要 `systemctl enable ufw`，plasma-firewall 可以作為 ufw 的前端。)
    * 無線網路: ipw2100-fw ipw2200-fw iw wpa_supplicant

* 圖形界面與多媒體
    * Display server: xorg-server
    * Display drivers: mesa(可選依賴於: libva-mesa-driver mesa-vdpau) xf86-video-intel vulkan-intel libva(可選依賴於: intel-media-driver)  
      (Intel UHD Graphics 為 Skylake 微架構 > Broadwell > Haswell。)
    * Display manager: sddm  
      (之後還需要在新安裝的系統裡執行 `systemctl enable sddm` 才會開機進入圖形界面。)
    * 輸入: xf86-input-libinput
    * 音訊: (ALSA is a set of built-in Linux kernel modules. Therefore, manual installation is not necessary.)
    * 桌面環境: plasma konsole dolphin
        * plasma 是一個 package group，安裝除了 discover kwallet-pam oxygen plasma-systemmonitor plasma-thunderbolt 以外的軟體包，photon-qt5-backend 選擇 photon-qt5-vlc
        * 安裝 package group 時如何只安裝或排除特定幾個，參考 <https://wiki.archlinux.org/index.php/Pacman#Installing_package_groups>
    * GUI 函式庫: gtk3
    * 字型: ttf-dejavu noto-fonts noto-fonts-cjk (沒有 noto-fonts-compat(Noto Mono))

* 應用程式
    * 工具: spectacle ark p7zip unrar kcalc grpn@A the_silver_searcher
    * 文書: kate neovim(可選依賴於: python-pynvim xsel) okular libreoffice-fresh libreoffice-fresh-zh-tw
    * 多媒體: viewnior kcolorchooser kolourpaint vlc kid3
    * 網路: google-chrome@A (JDownloader 2)@O transmission-qt 4kvideodownloader@A
    * 教育
        * 翻譯: stardict
        * 數學: (Mathematica 12.0)@O (MATLAB R2020a)@O(依賴於: libselinux@A(依賴於: libsepol@A))
        * Python 函式庫: python-numpy python-matplotlib(依賴於: pyside2) python-scipy
        * jupyter-calysto_scheme-git@A(依賴於: jupyter-metakernel@A)
    * 開發
        * base-develcmake ltrace strace git
        * Qt5: qt5-tools(依賴於: qt5-webkit) qt5-doc qt5-examples qtcreator pyside2
        * Python: python python-pip ipython jupyterlab
        * 虛擬機器: virtualbox virtualbox-guest-iso virtualbox-ext-oracle@A
        * IDE: visual-studio-code-bin@A
    * 系統
        * 語言包: poppler-data qt5-translations
        * 輸入法: fcitx5 fcitx5-qt fcitx5-gtk fcitx5-configtool fcitx5-chewing
        * 軟體包: (arch 沒有 pacman-mirrors，但有 reflector) (arch 沒有 pamac-cli pamac-gtk)
        * 備份: timeshift
        * 磁碟: baobab partitionmanager
        * Java: jre-openjdk

# 其它



[HWSpec]:      archlinux-02-details-and-miscellaneous.md#_1
[VBoxGuest]:   archlinux-02-details-and-miscellaneous.md#virtualbox-guest
[SSD4KAlign]:  archlinux-02-details-and-miscellaneous.md#ssd-4k
[SSDTRIM]:     archlinux-02-details-and-miscellaneous.md#ssd-trim
[NVMeProblem]: archlinux-02-details-and-miscellaneous.md#nvme-ssd
[BIOS/UEFI]:   archlinux-02-details-and-miscellaneous.md#bios-uefi
[BootLoader]:  archlinux-02-details-and-miscellaneous.md#boot-loader
[EnvVars]:     archlinux-02-details-and-miscellaneous.md
[Cache]:       archlinux-02-details-and-miscellaneous.md