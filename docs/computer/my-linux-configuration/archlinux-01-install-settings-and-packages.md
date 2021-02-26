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
11. 安裝其它軟體包 (見下面章節)，可以
    * 繼續用 `pacstrap` 安裝。
    * 等一下 chroot 進新安裝的系統裡用 `pacman` 安裝。
    * 重開機進入新安裝的系統裡用 `pacman` 安裝。
    (不管選擇什麼時候裝，至少分類在 "基本"、"開機" 和 "網路" 的軟體包必須裝上。)  
    (plasma 和其它 package group 必須用 `pacman` 安裝，不然 `pacstrap` 會全部用預設選項安裝。)
12. 產生 fstab: 執行 `genfstab -U /mnt >> /mnt/etc/fstab`
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
    `wd719x` 和 `aic94xx` 是 SCSI 的 firmware，一般電腦沒有。`xhci_pci` 是 USB 3.0 的 firmware (它改名叫 `xhci-pci`，所以找不到)。
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
      參考資料: [systemd - A stop job is running for Session c2 of user - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/273876/a-stop-job-is-running-for-session-c2-of-user)
    * 系統安裝完後，systemd 的藍牙服務未開啟: 執行 `sudo systemctl enable bluetooth` 設定開機後自動啟動藍牙服務。
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
    * 到 System Settings > Search 關閉 Baloo 搜尋功能，因為它佔用太多 CPU 和 RAM。
    * KDE Dolphin 提供的桌面沒有捷徑功能，必須依靠 `.desktop` 的方式實現，新增以下三個檔案: 
        * [~/Desktop/root.desktop](archlinux-03-configuration-files.md)
        * [~/Desktop/home.desktop](archlinux-03-configuration-files.md)
        * [~/Desktop/trash.desktop](archlinux-03-configuration-files.md)
    * 字型設定: 把字型檔放到 `~/.local/share/fonts`，[fontconfig 設定檔](archlinux-03-configuration-files.md)
      放到 `~/.config/fontconfig/fonts.conf` (這個 fontconfig 設定檔非常重要，如果沒有它，放進去的字型檔會把預設的配置搞的亂七八糟)。
* Shell 設定
    * 環境變數設定: 在 `/etc/environment` 中加入以下內容
      ```
      EDITOR=nvim
      ```
      [環境變數][EnvVars]
    * `~/.bash_profile`: The personal initialization file, executed for login shells
      ``` shell
      [[ -f ~/.bashrc ]] && . ~/.bashrc
      ```
      註：`~/.profile` 不會被讀取，原因不明。
    * `~/.bashrc`: The individual per-interactive-shell startup file ([檔案內容](archlinux-03-configuration-files.md))
    * 由於 root 沒有 `~/.bash_profile` 和 `~/.bashrc`，所以 `sudo -i` 出來的結果是黑白的，執行 `sudo ln -s ~jisa/{.bash_profile,.bashrc} /root`。
    * `~/.dircolors`，設定 "orphaned syminks and the files they point to" 不要閃爍: 
      * 如果沒有 `~/.dir_colors` 的話 `cp /etc/skel/.dir_colors ~`。
      * 把 `ORPHAN 01;05;37;41` 改成 `ORPHAN 01;37;41`。
      * 把 `MISSING 01;05;37;41` 改成 `MISSING 01;37;41`。
* 其它設定
    * 由於許多程式都會在 `~/.cache` 快取，卻不會自動清理不再使用的快取，因此把它掛載為 tmpfs，每次關機自動清理:   
      在不登入的情況下清空 `~/.cache`，然後在 `/etc/fstab` 中加入 `tmpfs /home/jisa/.cache tmpfs rw,nosuid,nodev,relatime,size=50%,mode=755,uid=1000,gid=1000 0 0`，儲存後重開機。  
      (雖然重開機後第一次執行程式會比較慢(其實感覺不太出來)，但是之後因為快取位於 tmpfs 上，反而會比較快。)  
      [~/.cache][Cache]

## 軟體包

* 軟體包名稱沒有後綴的來自 Arch Linux 官方軟體庫，有 `@A` 後綴的來自 Arch User Repository (AUR)，
  有 `@M` 後綴的來自 Manjaro 官方軟體庫 (用手動下載而非加入 pacman 的 mirror)，有 `@O` 後綴的代表其它安裝方式。
* [Manjaro 官方軟體庫 鏡像伺服器列表](https://repo.manjaro.org/)
* pacman 會保留所有下載過的軟體包作為快取，佔用很大儲存空間，可以執行 `sudo pacman -Scc` 清理。
* `sudo pacman -D --asdeps <package>` 可以指定軟體包為"作為其他軟體包的依賴安裝"，`sudo pacman -D --asexplicit <package>` 可以指定軟體包為"單獨指定安裝"。
* 更新 mirror: [Mirrors - ArchWiki](https://wiki.archlinux.org/index.php/Mirrors)
* 使用 AUR 所安裝的 Python 軟體包，需在 Python 更新後重新 `makepkg`(3.8 -> 3.9 才要，3.8.1 -> 3.8.2 不用)。

### 系統程式

* 基本
    * 最小可用: base linux linux-lts linux-firmware  
        - base 是一個 package group，它包含 bash bzip2 coreutils file filesystem findutils gawk gcc-libs gettext glibc grep gzip iproute2 
          iputils licenses pacman pciutils procps-ng psmisc sed shadow systemd systemd-sysvcompat tar util-linux xz)  
        - 開啟 pacman 彩色輸出: uncomment `/etc/pacman.conf` 中的 `Color` 選項 (用 `alias` 的話 `sudo` 時會失效)。
        - linux-lts 是 Linux LTS kernel，作為萬一最新的 kernel 無法使用時的備用。
    * 基本工具: bash-completion diffutils less lsb-release man-db neovim rsync wget which xdg-user-dirs xdg-utils  
        - 如果在建立使用者後才裝 `xdg-user-dirs`，
          之後必須手動執行 `LC_ALL=C xdg-user-dirs-update --force && echo -n en_US > ~/.config/user-dirs.locale` 建立英文 XDG 資料夾
    * 檔案系統: dosfstools e2fsprogs exfat-utils ntfs-3g
    * 管理工具: htop lsof polkit procps-ng psmisc sudo usbutils

* 開機
    * CPU microcode: intel-ucode
    * Bootloader: efibootmgr systemd-boot-pacman-hook@A

* 網路
    * 網路管理: networkmanager ppp
        - NetworkManager 內建 DHCP client，不須另外安裝 dhclient 或 dhcpcd。
    * 防火牆 ufw
        - 需要 `systemctl enable ufw`，plasma-firewall 可以作為 ufw 的 GUI 前端。
        - 警告: 不能同時啟用 `ufw` 和 `iptables/ip6tables` 服務。
    * 無線網路: ipw2100-fw ipw2200-fw iw wpa_supplicant

* 圖形界面與多媒體
    * Display server: xorg-server
    * Display drivers: mesa(可選依賴於: libva-mesa-driver mesa-vdpau) xf86-video-intel vulkan-intel libva(可選依賴於: intel-media-driver)  
        - Intel UHD Graphics 為 Skylake 微架構 > Broadwell > Haswell。
    * 輸入: xf86-input-libinput
    * 音訊: (ALSA is a set of built-in Linux kernel modules. Therefore, manual installation is not necessary.)
    * Display manager: sddm
        - 之後還需要在新安裝的系統裡執行 `systemctl enable sddm` 才會開機進入圖形界面。
    * 桌面環境: plasma konsole dolphin
        - plasma 是一個 package group，安裝除了 discover kwallet-pam oxygen plasma-systemmonitor plasma-thunderbolt 以外的軟體包，
          phonon-qt5-backend 選擇 phonon-qt5-vlc。
        - 安裝 package group 時如何只安裝或排除特定幾個，參考 <https://wiki.archlinux.org/index.php/Pacman#Installing_package_groups>。
        - konsole 和 dolphin 的設定在下面。
    * GUI 函式庫: gtk3
    * 字型: ttf-dejavu noto-fonts noto-fonts-cjk noto-fonts-compat@M
        - noto-fonts-compat@M: 在 Manjaro community 軟體庫，只依賴於 noto-fonts。

### 應用程式

* 工具
    * 螢幕截圖: spectacle
    * 壓縮: ark p7zip unrar
        - p7zip: p7zip 可以壓縮和解壓縮 Zip 壓縮檔，所以不用再裝 zip 和 unzip。
        - unrar: 雖然 p7zip 可以解壓縮 rar 壓縮檔，但 ark 需要 unrar 才能解壓縮 rar 壓縮檔，所以還是得裝。
    * 計算機: kcalc grpn@A
    * 文字搜尋: the_silver_searcher

* 文書
    * 文字編輯: kate neovim(可選依賴於: python-pynvim xsel)
        - kate: 字型 "Noto Mono 11pt"。
        - neovim: 設定檔 `~/.config/nvim/init.vim` ([檔案內容](archlinux-03-configuration-files.md))。
    * PDF 閱讀: okular
    * Office: libreoffice-fresh libreoffice-fresh-zh-tw
        - 分別在 Writer, Calc, Impress, Draw 的 "檢視 > 使用者界面" 調整成 "分頁標籤"。  
        - Writer 的 "基本字型 (西方語言)" 和 "基本字型 (亞洲語言)" 都改為 "Noto Sans CJK TC"。

* 多媒體: viewnior kcolorchooser kolourpaint vlc kid3

* 網路
    * 瀏覽器: google-chrome@A
        - Chromium 自 88 版開始，停止 Google 帳戶同步功能，所以只好改用 Google Chrome。
        - 使用久了之後會儲存大量的快取，"清除瀏覽資料" 裡的 "Cookie 和其他網站資料" 可以清除 `~/.config/google-chrome` 裡的快取，
          "快取圖片和檔案" 可以清除 `~/.cache/google-chrome` 裡的快取。
    * (JDownloader 2)@O(依賴於: jre-openjdk)
        - 到官方網站下載 Other 的 MULTIOS JAR without Installer（只有一個 `JDownloader.jar`，Linux 的 Installer 會多安裝 JRE，這個不會）複製到 `~/.local/opt/jd2` 資料夾中
        - 執行 `java -jar ~/.local/opt/jd2/JDownloader.jar` 啟動 JDownloader 2，第一次執行會下載必須的檔案到 `~/.local/opt/jd2`
        - `~/.local/opt/jd2/themes/standard/org/jdownloader/images/logo/icon.ico` 可以用來作為 Desktop Entry 的 icon
    * transmission-qt 4kvideodownloader@A

* 教育
    * 翻譯: stardict
    * 數學: (Mathematica 12.0)@O (MATLAB R2020a)@O(依賴於: libselinux@A(依賴於: libsepol@A))
        - Mathematica: 不使用 root 權限安裝在 `~/.local/opt`，安裝與啟用說明跟安裝檔在一起，
          另外還在 `~/.local/share/applications/wolfram-mathematica12.desktop` 加入 `Categories=Education;`。
    * Python 函式庫: python-numpy python-matplotlib(依賴於: pyside2) python-scipy
    * jupyter-calysto_scheme-git@A(依賴於: jupyter-metakernel@A)

* 開發
    * 二進位檔: base-devel ltrace strace
    * 專案管理: cmake git
        - git: 2020/8/13 後，GitHub 禁止 git 使用密碼登入，需改用 Personal access token 代替密碼登入。建立 Personal access token 後，
          執行 `git config --global credential.helper store && echo 'https://<USERNAME>:<TOKEN>@github.com' > ~/.git-credentials`，
          之後就可以不用輸入密碼。注意是明碼儲存。
    * Qt5: qt5-tools(依賴於: qt5-webkit) qt5-doc qt5-examples qtcreator pyside2
    * Python: python python-pip ipython jupyterlab
    * 虛擬機器: virtualbox virtualbox-guest-iso virtualbox-ext-oracle@A
        - virtualbox: 安裝完後執行 `sudo usermod -a -G vboxusers $USER` 並重開機，才能找到 USB 裝置。
        - virtualbox-ext-oracle@A: **警告**: virtualbox 和 virtualbox-ext-oracle@A 的版本必須相同，否則無法啟動虛擬機器。
    * IDE: visual-studio-code-bin@A
        - visual-studio-code-bin@A 跟官方軟體庫的 code 的差別在於: 前者是 Microsoft 官方發布的 binary 包，包含一些 proprietary 的功能；
          後者是從原始碼建置的開源版本。
        - 選用此版本的原因在於: code 會另外安裝 electron，而此版本自帶 electron，所以不用多安裝。
        - 新增檔案: `~/.config/Code`, `~/.vscode`, `~/.cache/vscode-cpptools`
        - 會佔用很大空間的快取或資料庫，可以手動刪除: 
            - `~/.config/Code/User/workspaceStorage` (曾開過的工作區資訊，有些 extensions (如：vscode.cpptools) 會儲存很大的資料庫)
            - `~/.config/Code/{Cache,CachedData,CachedExtensions,CachedExtensionVSIXs}`
            - `~/.cache/vscode-cpptools/ipch` (IntelliSense precompiled headers)

* 系統
    * 終端機: konsole  
        - konsole: 配色 "微風"，背景透明 "10%"，字型 "Noto Mono 12pt"。
    * 檔案管理: dolphin tree  
        - dolphin: 到 Dolphin 設定 > 一般 > 行為 選擇 "對所有資料夾使用相同的顯示模式"，不然 Dolphin 會在每個資料夾下建立 ".directory" 檔案。
        - dolphin: 到系統設定 > 工作空間行為 > 一般行為 > 點擊行為 選擇 "按兩下開啟檔案或資料夾 (按一下選取)"。
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
    * 軟體包: reflector (arch 沒有 pamac-cli pamac-gtk)  
      [AUR helpers - ArchWiki](https://wiki.archlinux.org/index.php/AUR_helpers)
    * 備份: timeshift
    * 磁碟: baobab partitionmanager
        - baobab: mate-disk-usage-analyzer 被包在 `mate-utils` 裡，`mate-utils` 又有太多其它東西，所以不採用。
    * Java: jre-openjdk
        - 修正字型很丑的問題：在 `/etc/environment` 加入 `_JAVA_OPTIONS=-Dawt.useSystemAAFontSettings=on`。  
          參考資料：[Java Runtime Environment fonts - ArchWiki](https://wiki.archlinux.org/index.php/Java_Runtime_Environment_fonts#Overriding_the_automatically_picked_up_settings)、
          [environment variables - Where can I set global Java Options? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/151733/where-can-i-set-global-java-options)

## 其它

* 更新前記得閱讀 Arch Linux 首頁的 news (或訂閱 arch-announce)，確認是否有需要人工干預的更新。  
  在更新重要軟體包 (如: kernel, xorg, systemd, glibc) 前，先進行備份，並到論壇看看是否有災情，不要在要使用電腦執行重要工作前更新。  
  [System maintenance - ArchWiki](https://wiki.archlinux.org/index.php/System_maintenance#Read_before_upgrading_the_system)
* 觸控板無法同時開啟邊緣滾動和兩指滾動 (目前無解)  
  以前觸控版的驅動程式使用 xf86-input-synaptics 可以同時開啟邊緣滾動和兩指滾動，但由於 xf86-input-synaptics 已經停止開發，
  所以 Arch Linux 建議安裝 libinput，[libinput 的官方說明文件](https://wayland.freedesktop.org/libinput/doc/latest/scrolling.html)
  明確指出雖然兩者都有支援，但**一次只能開啟一個**。儘管有人表示[同時安裝 lininput、xf86-input-libinput 和 xf86-input-synaptics 就可以同時開啟兩種滾動](https://forum.manjaro.org/t/enable-both-two-finger-scroll-and-edge-scroll-in-manejaro-kde/88144/8)，但由於無法測試而不採用。

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