# Arch Linux (一) 安裝、設定與軟體包

命令和程式碼中帶有 `<>` 的選項，請自行替換。

## 安裝

以下安裝至 [MSI Modern 15 A10M-419TW][HWSpec] ([安裝至 VirtualBox 作為 Guest 參考此篇][VBoxGuest])。

Boot Loader 採用 systemd-boot 單 Linux 方案。

1.  下載 Arch Linux 安裝光碟，並寫入 USB 隨身碟 ([USB flash installation medium - ArchWiki](https://wiki.archlinux.org/index.php/USB_flash_installation_medium)) 或燒錄至光碟。
2.  到電腦的 UEFI Boot Manager 設定以該 USB 隨身碟或光碟開機，開機後會自動以 root 登入。
3.  預設 keyboard layout 為 US，需要的話進行調整。
4.  確認是否以 UEFI 開機: 執行 `[ -d /sys/firmware/efi/efivars ] && echo "booted in UEFI mode" || echo "booted in BIOS (or CSM) mode"`。
5.  連線到網際網路。
6.  更新系統時間: 執行 `timedatectl set-ntp true`。
7.  分割磁碟: 執行 `cfdisk /dev/nvme0n1`，建立 GPT 分割表，第一個分區[建立 EFI 系統分割區][BIOS/UEFI]，大小至少 512MiB，Type 選 "EFI System"，
    之後建立其它分割區 (ext4 分割區的 Type 選預設的 "Linux filesystem"。)  
    (cfdisk 跟 fdisk 功能一樣，但是有比較好用的類圖形界面。)  
    (用 parted 分割 GPT 會偷偷加上 partition name (是存在 GPT 裡的名字，不是各分割區自己的 label，後者可用 e2label 查看)，因此改用 fdisk/cfdisk)  
    (如果要刪除分割表，要用 fdisk，執行後按 `g`)  
    ([SSD 4K 對齊][SSD4KAlign])
8.  格式化磁碟分區
    ```
    mkfs.fat -F32 /dev/nvme0n1p1    # /boot (EFI 系統分割區必須為 FAT32)
    mkfs.ext4 /dev/nvme0n1p2        # /
    mkfs.ext4 /dev/nvme0n1p3        # /home
    ```
    ([建立 EFI 系統分割區][BIOS/UEFI])
9.  掛載新安裝的系統的磁碟分區
    ```
    mount /dev/nvme0n1p2 /mnt -o discard
    mkdir /mnt/boot /mnt/home
    mount /dev/nvme0n1p1 /mnt/boot -o discard
    mount /dev/nvme0n1p3 /mnt/home -o discard
    ```
    (`-o discard` 是為了開啟 [SSD TRIM][SSDTRIM])
10. 安裝最小可用系統: 執行 `pacstrap /mnt base linux linux-lts linux-firmware`。
11. 產生 fstab: 執行 `genfstab -U /mnt >> /mnt/etc/fstab`
12. chroot 進新安裝的系統，執行 `arch-chroot /mnt`，**以下位於 chroot 裡的命令會以 "(in chroot)" 開頭**。
13. (in chroot) 安裝其它軟體包: 使用 `pacman` 安裝所有 "系統程式" 分類的軟體包。  
    * plasma 和其它軟體包群組必須用 `pacman` 安裝，不然 `pacstrap` 會全部用預設選項安裝。
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
    `wd719x` 和 `aic94xx` 是 SCSI 的 firmware，一般電腦沒有。`xhci_pci` 是 USB 3.0 的 firmware (它改名叫 `xhci-pci`，所以找不到)。
18. (in chroot) 設定 root 密碼: 執行 `passwd`。
19. (in chroot) 安裝 Boot Loader (採用 systemd-boot 多 Linux 方案)
    * systemd-boot 已經包含在 Arch Linux 的 systemd 軟體包裡，不用另外安裝。
    * 如果曾安裝過其它 UEFI Boot Loader，刪除舊的 EFI boot entry: 執行 `efibootmgr -b <boot entry number> -B`。
    * 安裝 EFI boot manager: 執行 `bootctl install`。
    * 編輯 systemd-boot 設定檔 `/boot/loader/loader.conf`。
      ```
      default arch.conf
      timeout 3
      ```
    * 新增一個 boot entry `/boot/loader/entries/arch.conf`。
      ```
      title Arch Linux
      linux /vmlinuz-linux
      initrd /intel-ucode.img
      initrd /initramfs-linux.img
      options root=UUID=<執行 `lsblk -f` 找出 UUID> rw nvme_core.default_ps_max_latency_us=0
      ```
    * 如果安裝了 linux-lts，記得也為它新增一個 boot entry。
    * 如果安裝成功，執行 `bootctl list` 應該會看到上面加入的 boot entry；
      執行 `efibootmgr -v` 應該會看到 "Linux Boot Manager ... File(\EFI\systemd\systemd-bootx64.efi)"
    * 未來如果更新 systemd-boot，需要手動更新 boot manager (執行 `bootctl update`)，
      或者安裝 systemd-boot-pacman-hook@A 自動在更新 systemd-boot 後更新 boot manager。
    * [systemd-boot - ArchWiki](https://wiki.archlinux.org/index.php/Systemd-boot)
    * `nvme_core.default_ps_max_latency_us=0` 是為了[修正 NVMe SSD 睡死問題][NVMeProblem]。
20. 設定開機時進入圖形界面: 執行 `systemctl enable sddm`。
21. 系統安裝完後，systemd 的藍牙服務未啟用: 執行 `sudo systemctl enable bluetooth`。
22. 建立一般使用者並開啟 sudo
    * 執行 `useradd -m -G <additional_groups> -s <login_shell> <username>` (`<login_shell>` 必須存在於 `/etc/shells`)，
      然後執行 `passwd <username>` 設定密碼。
    * 執行 `EDITOR=nvim visudo` 並 uncomment `%wheel ALL=(ALL) ALL`，然後把使用者加入該群組 `usermod -a -G wheel <username>`。
    * 調整 sudo timeout，讓 sudo 不用隔一段時間重新輸入密碼: 執行 `EDITOR=nvim visudo -f /etc/sudoers.d/<username>`，
      加入 `Defaults timestamp_timeout=-1` 後儲存離開。
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
    * 解決關機時出現 `A stop job is running for ... (... / 1min 30s)`，需要等待很長時間的問題:  
      建立 `/etc/systemd/system.conf.d/DefaultTimeoutStopSec.conf`，內容為
      ```
      [Manager]
      DefaultTimeoutStopSec=10s
      ```
      儲存後重開機。  
      參考資料: [systemd - A stop job is running for Session c2 of user - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/273876/a-stop-job-is-running-for-session-c2-of-user)
    * 預設情況下，使用者密碼輸入錯誤 3 次，就會鎖定 10 分鐘
        * 此功能由 `pam_faillock` 模組提供 (以前是 `pam_tally2`)。
        * 完全關閉此功能: 編輯 `/etc/security/faillock.conf`，修改為 `deny = 0`。
        * 不關閉此功能，取消當下的鎖定: 以 root 登入 (因為 sudo 也被鎖起來了)，執行 `faillock --user <username> --reset`。
        * 參考資料: [Security - ArchWiki](https://wiki.archlinux.org/index.php/Security#Lock_out_user_after_three_failed_login_attempts)。
    * `tmpfs /root/.cache tmpfs rw,nosuid,nodev,relatime,size=50%,mode=755,uid=0,gid=0 0 0`
    * 由於許多程式都會在 `~/.cache` 快取，卻不會自動清理不再使用的快取，因此把它掛載為 tmpfs，每次關機自動清理:   
      在不登入的情況下清空 `~/.cache`，然後在 `/etc/fstab` 中加入 `tmpfs /home/jisa/.cache tmpfs rw,nosuid,nodev,relatime,size=50%,mode=755,uid=1000,gid=1000 0 0`，儲存後重開機。  
      (雖然重開機後第一次執行程式會比較慢(其實感覺不太出來)，但是之後因為快取位於 tmpfs 上，反而會比較快。)  
      [~/.cache][Cache]
    * 預設情況下 systemd-journald 可以儲存高達 4 GB 的日誌，會佔用太多儲存空間，修改成只儲存 1 週內的日誌:  
      建立 `/etc/systemd/journald.conf.d/MaxRetentionSec.conf`，內容為
      ```
      [Journal]
      MaxRetentionSec=1week
      ```
      儲存後重開機。
* 桌面環境 (KDE) 設定
    * 設定語言及地區
        * 到 System Settings > Regional Settings > Language 加入"繁體中文"，並移到最上面。
        * 到 System Settings > Regional Settings > Formats 改為"台灣 - 繁體中文"。
        * 這兩項設定會修改 `~/.config/plasma-localerc`，不會修改其它檔案 (像是 `/etc/locale.conf` 或 `~/.config/locale.conf`)，
          所以用 VT 的時候 locale 還是 `/etc/locale.conf` 指定的 `en_US.UTF-8`。
    * 設定 KDE Plasma 外觀
        * 設定 Plasma Style 為 Breeze Dark。
        * 設定 Colors 為 Breeze。
    * 關閉 KDE Wallet subsystem 以避免它一直跳出視窗要求輸入密碼: 執行 `echo -e '[Wallet]\nEnabled=false' > ~/.config/kwalletrc`。
    * Baloo 搜尋功能佔用太多 CPU 和 RAM，關閉它: 到 System Settings > Search 關閉 Baloo 搜尋功能 (或執行 `balooctl disable`)，
      然後執行 `balooctl purge` 刪除已建立的索引 (`~/.local/share/baloo/index`)。
    * Windows 鍵無法開啟 "應用程式選單": 如果到應用程式選單的快捷鍵設定按下 Windows 鍵，會被識別成 "Meta 鍵" 而無法作為快捷鍵 (因為 Meta 鍵是修飾鍵，必須配合其它按鍵使用)，
      但如果將快捷鍵設定為 "Alt+F1"，就可以使用 Windows 鍵開啟應用程式選單，目前原理不明。
    * 隱私設定
         * 到 設定 > 工作空間行為 > 活動 > 活動，修改 Default 的設定，勾選 "請勿追蹤此活動的使用量"。
         * 到 設定 > 工作空間行為 > 活動 > 隱私，紀錄以開啟的文件選 "不要保留"。
    * 字型設定: 把字型檔放到 `~/.local/share/fonts`，[fontconfig 設定檔](archlinux-03-configuration-files.md)
      放到 `~/.config/fontconfig/fonts.conf` (這個 fontconfig 設定檔非常重要，如果沒有它，放進去的字型檔會把預設的配置搞的亂七八糟)。
* 環境變數設定
    * 環境變數設定:
        * 新增 [~/.envars](archlinux-03-configuration-files.md)。
        * 在 `~/.bashrc` 中加入`[[ -f ~/.envars ]] && . ~/.envars`。
        * 執行 `ln -s ../../../.envars ~/.config/plasma-workspace/env/envars.sh`。
        * 執行 `sudo ln -s ~jisa/.envars /root`。
        * [環境變數][EnvVars]
* Shell 設定
    * 修改 [~/.bash_profile](archlinux-03-configuration-files.md) 和 [~/.bashrc](archlinux-03-configuration-files.md)。
    * 由於 root 沒有 `~/.bash_profile` 和 `~/.bashrc`，所以 `sudo -i` 出來的結果是黑白的，執行 `sudo ln -s ~jisa/{.bash_profile,.bashrc} /root`。

## 軟體包

* 軟體包名稱沒有後綴的來自 Arch Linux 官方軟體庫，有 `@A` 後綴的來自 Arch User Repository (AUR)，有 `@O` 後綴的代表其它安裝方式。
* 更新前軟體包前，建議先更新鏡像伺服器列表: 執行 `sudo systemctl start reflector.service && journalctl --no-pager -b -u reflector.service`。
* 更新前記得閱讀 Arch Linux 首頁的 news (或訂閱 arch-announce)，確認是否有需要人工干預的更新。  
  在更新重要軟體包 (如: kernel, xorg, systemd, glibc) 前，先進行備份，並到論壇看看是否有災情，不要在要使用電腦執行重要工作前更新。  
  [System maintenance - ArchWiki](https://wiki.archlinux.org/index.php/System_maintenance#Read_before_upgrading_the_system)
* pacman 會保留所有下載過的軟體包作為快取，佔用很大儲存空間，可以執行 `sudo pacman -Scc` 清理全部，或執行 `sudo paccache -r` 保留最新的三個版本並清除其它更舊的版本。
* 使用 `sudo pacman -S --needed <package>` 可以避免重新安裝已經安裝(且為最新版本)的軟體包。
* 使用 `sudo pacman -D --asdeps <package>` 可以指定軟體包為 "作為其他軟體包的依賴安裝"，
  使用 `sudo pacman -D --asexplicit <package>` 可以指定軟體包為 "單獨指定安裝"。
* 使用 `pacman -Qm` 可以列出所有已安裝的，非 Arch Linux 官方軟體庫的軟體包 (如: AUR)。
* 使用 AUR 所安裝的 Python 軟體包，需在 Python 更新後重新 `makepkg`(3.8 -> 3.9 才要，3.8.1 -> 3.8.2 不用)。

### 系統程式

* 基本
    * 最小可用: base linux linux-lts linux-firmware  
        - base 元軟體包 (meta package) 包含 bash bzip2 coreutils file filesystem findutils gawk gcc-libs gettext glibc grep gzip iproute2 
          iputils licenses pacman pciutils procps-ng psmisc sed shadow systemd systemd-sysvcompat tar util-linux xz
        - 開啟 pacman 彩色輸出: uncomment `/etc/pacman.conf` 中的 `Color` 選項 (用 `alias` 的話 `sudo` 時會失效)。
        - linux-lts 是 Linux LTS kernel，作為萬一最新的 kernel 無法使用時的備用。
    * 基本工具: base-devel bash-completion cmake diffutils less lsb-release man-db neovim rsync tree wget xdg-user-dirs xdg-utils
        - base-devel 軟體包群組包含 autoconf automake binutils bison fakeroot file findutils flex gawk gcc gettext grep groff gzip libtool 
          m4 make pacman patch pkgconf sed sudo texinfo which
        - 避免 less 在家目錄底下建立紀錄檔 `~/.lesshst`: 在 `~/.bashrc` 中加入 `export LESSHISTFILE=/dev/null`。
        - pacman 依賴於 base-devel 軟體包群組裡的其它軟體包。
        - 如果在建立使用者後才裝 xdg-user-dirs，
          之後必須手動執行 `LC_ALL=C xdg-user-dirs-update --force && echo -n en_US > ~/.config/user-dirs.locale` 建立英文 XDG 資料夾
    * 檔案系統: dosfstools e2fsprogs exfat-utils ntfs-3g
    * 管理工具: htop lsof polkit usbutils

* 開機
    * CPU microcode: intel-ucode
    * Bootloader: efibootmgr systemd-boot-pacman-hook@A

* 網路
    * 網路管理: networkmanager(依賴於: wpa_supplicant，可選依賴於: ppp)
        - NetworkManager 內建 DHCP client，不須另外安裝 dhclient 或 dhcpcd。
    * 無線網路: ipw2100-fw ipw2200-fw
        - NetworkManager 可以用來連線無線網路，所以不用再裝 iwd 或 iw。
    * 防火牆 ufw
        - 需要 `systemctl enable ufw`，plasma-firewall 可以作為 ufw 的 GUI 前端。
        - 警告: 不能同時啟用 `ufw` 和 `iptables/ip6tables` 服務。

* 圖形界面與多媒體
    * Display server: xorg-server
    * Display drivers: mesa(可選依賴於: libva-mesa-driver mesa-vdpau) xf86-video-intel vulkan-intel libva(可選依賴於: intel-media-driver)  
        -  intel-media-driver: backend for Intel GPUs (>= Broadwell) (Intel UHD Graphics 為 Skylake 微架構 > Broadwell 微架構 > Haswell 微架構)。
    * 輸入: xf86-input-libinput
    * 音訊: (ALSA is a set of built-in Linux kernel modules. Therefore, manual installation is not necessary.)
    * Display manager: sddm
        - 之後還需要在新安裝的系統裡執行 `systemctl enable sddm` 才會開機進入圖形界面。
    * 桌面環境: plasma konsole dolphin
        - plasma 是一個軟體包群組，安裝除了 discover kdeplasma-addons kwallet-pam oxygen plasma-browser-integration plasma-systemmonitor 
          plasma-thunderbolt plasma-vault plasma-workspace-wallpapers 以外的軟體包，phonon-qt5-backend 選擇 phonon-qt5-vlc。
        - 安裝軟體包群組時如何只安裝或排除特定幾個，參考 <https://wiki.archlinux.org/index.php/Pacman#Installing_package_groups>。
        - plasma 軟體包群組包含 bluedevil breeze breeze-gtk discover drkonqi kactivitymanagerd kde-cli-tools kde-gtk-config kdecoration 
          kdeplasma-addons kgamma5 khotkeys kinfocenter kmenuedit kscreen kscreenlocker ksshaskpass ksysguard kwallet-pam 
          kwayland-integration kwayland-server kwin kwrited libkscreen libksysguard milou oxygen plasma-browser-integration 
          plasma-desktop plasma-disks plasma-firewall plasma-integration plasma-nm plasma-pa plasma-sdk plasma-systemmonitor 
          plasma-thunderbolt plasma-vault plasma-workspace plasma-workspace-wallpapers polkit-kde-agent powerdevil sddm-kcm 
          systemsettings xdg-desktop-portal-kde
        - konsole: 配色 "微風"，背景透明 "10%"，字型 "Noto Mono 12pt"。
        - dolphin: 到 Dolphin 設定 > 一般 > 行為 選擇 "對所有資料夾使用相同的顯示模式"，不然 Dolphin 會在每個資料夾下建立 ".directory" 檔案。
        - dolphin: 到系統設定 > 工作空間行為 > 一般行為 > 點擊行為 選擇 "按兩下開啟檔案或資料夾 (按一下選取)"。
        - dolphin: Dolphin 提供的桌面沒有捷徑功能，必須依靠 `.desktop` 的方式實現，新增 
          [~/Desktop/root.desktop](archlinux-03-configuration-files.md), 
          [~/Desktop/home.desktop](archlinux-03-configuration-files.md), 
          [~/Desktop/trash.desktop](archlinux-03-configuration-files.md) 三個檔案。
        - dolphin: 為了讓圖示正確，"檔案 > 建立新的 > 文字檔案..." 建立的檔案中有一個空格和換行，如果要建立空白檔案的功能，必須自己新增模板。
          執行 `mkdir -p ~/.local/share/templates/.source && touch ~/.local/share/templates/.source/empty-file` 建立零位元組的空白檔案，
          然後新增 [~/.local/share/templates/empty-file.desktop](archlinux-03-configuration-files.md)。
          參考資料：[KDE Neon > Dolphin > Create New > Text File: File not empty. • KDE Community Forums](https://forum.kde.org/viewtopic.php?f=224&t=142366)。
    * GUI 函式庫: gtk3
    * 字型: ttf-dejavu noto-fonts noto-fonts-cjk noto-fonts-compat@O
        - noto-fonts-compat@O: 只依賴於 noto-fonts，從 <https://repo.manjaro.org/> 找到一個鏡像伺服器下載 
          `/stable/community/x86_64/noto-fonts-compat-<version>.pkg.tar.xz` 後用 `pacman -U` 安裝。

### 應用程式

* 工具
    * 螢幕截圖: spectacle
    * 壓縮: ark p7zip unrar
        - p7zip: p7zip 可以壓縮和解壓縮 Zip 壓縮檔，所以不用再裝 zip 和 unzip。
        - unrar: 雖然 p7zip 可以解壓縮 rar 壓縮檔，但 ark 需要 unrar 才能解壓縮 rar 壓縮檔，所以還是得裝。
    * 計算機: kcalc grpn@A
    * 文字搜尋: the_silver_searcher

* 文書
    * 文字編輯: neovim(可選依賴於: python-pynvim xsel) kate
        - neovim: 設定檔 `~/.config/nvim/init.vim` ([檔案內容](archlinux-03-configuration-files.md))。
        - kate: 字型 "Noto Mono 11pt"。
    * PDF 閱讀: okular
    * Office: libreoffice-fresh libreoffice-fresh-zh-tw
        - 分別在 Writer, Calc, Impress, Draw 的 "檢視 > 使用者界面" 調整成 "分頁標籤"。  
        - Writer 的 "基本字型 (西方語言)" 和 "基本字型 (亞洲語言)" 都改為 "Noto Sans CJK TC"。

* 多媒體
    * viewnior kcolorchooser kolourpaint vlc kid3

* 網路
    * 瀏覽器: firefox firefox-i18n-zh-tw firefox-adblock-plus firefox-clearurls
        - 新增檔案: `~/.mozilla`, `~/.cache/mozilla`
    * (JDownloader 2)@O(依賴於: jre-openjdk)
        - 執行 `sudo mkdir /opt/jd2 && sudo chown jisa:jisa /opt/jd2` (因為 JDownloader 2 會更新檔案，所以需要權限)
        - 到官方網站下載 Other 的 MULTIOS JAR without Installer（只有一個 `JDownloader.jar`，Linux 的 Installer 會多安裝 JRE，這個不會）複製到 `/opt/jd2` 資料夾中
        - 執行 `java -jar /opt/jd2/JDownloader.jar` 啟動 JDownloader 2，第一次執行會下載必須的檔案到 `~/.local/opt/jd2`
        - 手動建立應用程式選單項目，`/opt/jd2/themes/standard/org/jdownloader/images/logo/icon.ico` 可以用來作為 Desktop Entry 的 icon
    * transmission-qt
    * VPN: networkmanager-openconnect(依賴於: openconnect)
        - Pulse Connect Secure 連線方式: (1) 執行 `sudo openconnect --protocol=pulse https://vpn.example.com/` (2) 到 NetworkManager 新增 `Pulse Connect Secure (openconnect)`，VPN 協定 `Pulse Connect Secure`，閘道 `vpn.example.com`，其餘留空即可，連線時需要先按連線 VPN 主機的按鈕。
        - networkmanager-openconnect 和 openconnect 不會新增任何檔案。

* 教育
    * 翻譯: stardict
    * Python 函式庫: python-sympy python-numpy python-matplotlib(依賴於: pyside2) python-scipy

* 開發
    * 除錯: ltrace strace
    * 專案管理: git
        - 不要建立設定擋在 `~/.gitconfig`: 執行 `mkdir ~/.config/git && touch ~/.config/git/config`，然後執行 `git config --global user.name "USER_NAME"` 等設定。
        - git: 2020/8/13 後，GitHub 禁止 git 使用密碼登入，需改用 Personal access token 代替密碼登入。建立 Personal access token 後，
          執行 `git config --global credential.helper store && echo 'https://<USERNAME>:<TOKEN>@github.com' > ~/.config/git/credentials && chmod 600 ~/.config/git/credentials`，之後就可以不用輸入密碼。注意是明碼儲存。
    * Qt5: qt5-tools(依賴於: qt5-webkit) qt5-doc qt5-examples qtcreator pyside2
    * Python: python python-pip ipython jupyterlab
        - ipython: 修改設定檔位置: 在 `~/.bashrc` 中加入 `export IPYTHONDIR=~/.config/ipython` (預設在 `~/.ipython`)
        - jupyterlab: 修改設定檔位置: 在 `~/.bashrc` 中加入 `export JUPYTER_CONFIG_DIR=~/.config/jupyter` (預設在 `~/.jupyter`)
        - jupyterlab: 避免到處建立 `.ipynb_checkpoints`: 執行 `jupyter lab --generate-config`，在 `${JUPYTER_CONFIG_DIR}/jupyter_lab_config.py` 中加入 `c.FileCheckpoints.checkpoint_dir = '/home/jisa/.cache/ipynb_checkpoints'` (因為前面設定 `~/.cache` 是 tmpfs，所以關機後就會清除)
    * 虛擬機器: virtualbox(依賴於: virtualbox-host-modules-arch) virtualbox-guest-iso virtualbox-ext-oracle@A
        - virtualbox: 安裝完後執行 `sudo usermod -a -G vboxusers $USER` 並重開機，才能找到 USB 裝置。
        - virtualbox-ext-oracle@A: **警告**: virtualbox 和 virtualbox-ext-oracle@A 的版本必須相同，否則無法啟動虛擬機器。
    * Qemu: qemu qemu-arch-extra
    * RISC-V 裸機工具鏈: riscv64-elf-binutils riscv64-elf-gcc riscv64-elf-gdb riscv64-elf-newlib
        - 注意: `riscv32-elf-*` 和 `riscv64-elf-*` 是裸機 (baremetal) 工具鏈，無法用來編譯 Linux kernel。
    * RISC-V Linux 工具鏈: riscv64-linux-gnu-binutils riscv64-linux-gnu-gcc riscv64-linux-gnu-gdb riscv64-linux-gnu-glibc riscv64-linux-gnu-linux-api-headers
        - 注意: `	riscv64-linux-gnu-*` 是 Linux 工具鏈，無法用來編譯裸機程式。
    * 編譯 Linux kernel 所需的工具: xmlto inetutils bc cpio
        - 根據 [Kernel/Traditional compilation - ArchWiki](https://wiki.archlinux.org/index.php/Kernel/Traditional_compilation#Install_the_core_packages)
          執行 `sudo pacman -S --needed base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz` 安裝所需工具。
    * IDE: visual-studio-code-bin@A
        - visual-studio-code-bin@A 跟官方軟體庫的 code 的差別在於: 前者是 Microsoft 官方發布的 binary 包，包含一些 proprietary 的功能；
          後者是從原始碼建置的開源版本。
        - 選用此版本的原因在於: code 會另外安裝 electron，而此版本自帶 electron，所以不用多安裝。
        - 新增檔案: `~/.config/Code`, `~/.vscode`, `~/.cache/vscode-cpptools`, `~/.pki`
        - 會佔用很大空間的快取或資料庫，可以手動刪除: 
            - `~/.config/Code/User/workspaceStorage` (曾開過的工作區資訊，有些 extensions (如：vscode.cpptools) 會儲存很大的資料庫)
            - `~/.config/Code/{Cache,CachedData,CachedExtensions,CachedExtensionVSIXs}`
            - `~/.cache/vscode-cpptools/ipch` (IntelliSense precompiled headers)
        - [Settings Sync](https://code.visualstudio.com/docs/editor/settings-sync) 功能需要 `gnome-keyring` 才能登入 GitHub (目前未使用此功能，所以沒安裝)。
    * 資料庫: sqlitebrowser
    * Rust: rust
        - `cargo` 會新增 `~/.cargo`。

* 系統
    * 軟體包: pacman-contrib pacman-cleanup-hook@A reflector pamac-cli@A
        - pamac-cli@A: `pamac checkupdates -a` 可以在不修改系統資料庫 (`/var/lib/pacman/sync`) 的情況下檢查更新，
          因為它會維持自己的資料庫 (`/tmp/pamac/dbs/sync`)，所以也不需要 root 權限。
    * 語言包: poppler-data qt5-translations
    * 輸入法: fcitx5 fcitx5-qt fcitx5-gtk fcitx5-configtool fcitx5-chewing  
        - 於 `/etc/environment` 加入
          ```
          GTK_IM_MODULE=fcitx
          QT_IM_MODULE=fcitx
          XMODIFIERS=@im=fcitx
          SDL_IM_MODULE=fcitx
          ```
          安裝後 fcitx5 會自動被加到 /etc/xdg/autostart 裡，所以可以自動啟動。
          若沒有自動啟動可以執行 `ln -s /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/`。  
          <https://wiki.archlinux.org/index.php/Fcitx_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E6%A1%8C%E9%9D%A2%E7%8E%AF%E5%A2%83%E4%B8%8B%E8%87%AA%E5%8A%A8%E5%90%AF%E5%8A%A8>
    * 備份: timeshift@A
    * 磁碟: baobab partitionmanager
        - baobab: mate-disk-usage-analyzer 被包在 `mate-utils` 裡，`mate-utils` 又有太多其它東西，所以不採用。
    * Java: jre-openjdk java-openjfx
        - 修正字型很丑的問題：在 `/etc/environment` 加入 `_JAVA_OPTIONS=-Dawt.useSystemAAFontSettings=on`。  
          參考資料：[Java Runtime Environment fonts - ArchWiki](https://wiki.archlinux.org/index.php/Java_Runtime_Environment_fonts#Overriding_the_automatically_picked_up_settings)、
          [environment variables - Where can I set global Java Options? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/151733/where-can-i-set-global-java-options)

## 其它

* 觸控板無法同時開啟邊緣滾動和兩指滾動 (目前無解)  
  以前觸控版的驅動程式使用 xf86-input-synaptics 可以同時開啟邊緣滾動和兩指滾動，但由於 xf86-input-synaptics 已經停止開發，
  所以 Arch Linux 建議安裝 libinput，[libinput 的官方說明文件](https://wayland.freedesktop.org/libinput/doc/latest/scrolling.html)
  明確指出雖然兩者都有支援，但**一次只能開啟一個**。儘管有人表示[同時安裝 lininput、xf86-input-libinput 和 xf86-input-synaptics 就可以同時開啟兩種滾動](https://forum.manjaro.org/t/enable-both-two-finger-scroll-and-edge-scroll-in-manejaro-kde/88144/8)，但由於無法測試而不採用。
* Arch Linux 預設沒有 `/etc/skel/.dir_colors` 或 `/etc/DIR_COLORS`，所以也沒有 `~/.dir_colors`，若有需要可以執行 `dircolors -p > ~/.dir_colors` 生成。
* 關閉螢幕: 執行 `xset dpms force off`，滑鼠動一下或按下鍵盤就會解除，參考資料: [Display Power Management Signaling - ArchWiki](https://wiki.archlinux.org/index.php/Display_Power_Management_Signaling#Modify_DPMS_and_screensaver_settings_with_a_command)。

## 參考資料

* [Installation guide - ArchWiki](https://wiki.archlinux.org/index.php/installation_guide)
* [General recommendations - ArchWiki](https://wiki.archlinux.org/index.php/General_recommendations)
* Manjaro Architect 自動安裝的軟體包

[HWSpec]:      archlinux-02-details-and-miscellaneous.md#_1
[VBoxGuest]:   archlinux-02-details-and-miscellaneous.md#virtualbox-guest
[SSD4KAlign]:  archlinux-02-details-and-miscellaneous.md#ssd-4k
[SSDTRIM]:     archlinux-02-details-and-miscellaneous.md#ssd-trim
[NVMeProblem]: archlinux-02-details-and-miscellaneous.md#nvme-ssd
[BIOS/UEFI]:   archlinux-02-details-and-miscellaneous.md#bios-uefi
[BootLoader]:  archlinux-02-details-and-miscellaneous.md#boot-loader
[EnvVars]:     archlinux-02-details-and-miscellaneous.md
[Cache]:       archlinux-02-details-and-miscellaneous.md
