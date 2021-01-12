# Manjaro

## 新電腦注意事項

### NVMe SSD 問題

新的電腦使用 NVMe SSD 取代傳統的機械硬碟，原廠電腦有一個硬碟，後來又加購一個。

但在使用時發現，如果將 /home 放在第二個硬碟上，並執行 I/O 頻繁的程式（如：在 VirtualBox guest 裡執行 Pacman 系統升級，或在 host 安裝 Mathematica），
host 和 guest 就會直接卡住（但執行中的程式只要不讀取硬碟就可以繼續執行），只能強制重開機。

從 `journalctl` 有發現 `kernel: nvme nvme1: I/O 320 QID 4 timeout, aborting`(數字可能不同)，確定問題出在 NVMe SSD 上。

根據網路資料，確認過不是溫度太高、RAM 用完造成，也更換過一顆新的硬碟，所以問題出在 Linux 上（因為沒發現 Windows 有這個問題）。

因為可能是 I/O 太頻繁的關係，但之前往硬碟寫了 200 多 GB 的資料也沒事，所以也有可能和 VirtualBox 有關。
根據網路資料，(1) System: 打勾 "Enable I/O APIC" (2) SATA controller: 打勾 "Use host I/O cache" (3) VDI: 打勾 "Solid-state drive"，無效。

根據網路資料，可能是 Linux 的 NVMe 驅動程式中的省電模式有問題，關掉省電模式就可以解決。
修改 /etc/default/grub，在 `GRUB_CMDLINE_LINUX_DEFAULT` 加上 `nvme_core.default_ps_max_latency_us=0`，儲存後 `update-grub`。
`cat /sys/module/nvme_core/parameters/default_ps_max_latency_us` 原本 100000，修改後為 0。
經過長期測試發現有效。

參考資料：  
[Fixing NVME SSD Problems On Linux – TEKBYTE](https://tekbyte.net/2020/fixing-nvme-ssd-problems-on-linux/)  
[完整學習機器學習實錄1——安裝 Ubuntu 18.04 - HackMD](https://hackmd.io/@William-Mou/ryNms2F-E?type=view)

### Linux + SSD

要開啟 TRIM 避免消耗，在磁碟機 mount 選項中加入 `discard`。

參考資料：  
[Solid state drive (正體中文) - ArchWiki](https://wiki.archlinux.org/index.php/Solid_state_drive_(%E6%AD%A3%E9%AB%94%E4%B8%AD%E6%96%87)#TRIM)

### UEFI + GPT

新的電腦使用 UEFI 取代傳統的 BIOS，UEFI+GPT 分割表需要多分割一個「EFI 系統分割區」（UEFI+MBR 分割表就不需要），網路建議 EFI 系統分割區至少 512 MB。
使用 parted 的操作方式見下方。

參考資料：  
[Partitioning - ArchWiki](https://wiki.archlinux.org/index.php/partitioning#UEFI/GPT_layout_example)  
[EFI system partition - ArchWiki](https://wiki.archlinux.org/index.php/EFI_system_partition#GPT_partitioned_disks)

## 系統安裝

### VirtualBox 注意事項

1. 安裝時，如果進入 GRUB 後沒畫面，圖形控制器改用 VMSVGA。
2. 安裝後，如果進入 GRUB 後沒畫面，圖形控制器改用 VBoxSVGA。
3. 安裝後，圖形控制器改用 VBoxSVGA 才可以在改變 VirtualBox 視窗大小後自動調整解析度。
4. 安裝後不需要再裝 VirtualBox Guest Additions，Manjaro 已經自動裝好了。
5. 使用共用資料夾，需要把使用者加入 `vboxsf` 群組才有存取權限，執行 `sudo gpasswd -a $USER vboxsf` 後重新登入即可。

### 安裝 Manjaro Architect

安裝目標：安裝 KDE Plasma 5 桌面環境，但不要預裝一大堆用不到的軟體包。

使用光碟：manjaro-architect-20.0.3-200607-linux56.iso

以下沒有特別提到的設定選項，就按照預設或依實際情況填寫(如使用者名稱等)。

進入 Manjaro Architect Installer 後，依下列順序執行：

1.  Prepare Installation
    1.  Set Virtual Console
    2.  List Devices (optional): 注意不要裝到隨身碟去（新電腦的兩顆 SSD 是 nvme0n1 和 nvme1n1）
    3.  Partition Disk: 使用 `parted` 分割(不會格式化)
        ```
        # nvme0n1
        mktable gpt
        mkpart fat32 0% 512MB    # nvme0n1p1  /boot/efi
        set 1 esp on
        mkpart ext4 512MB 25%    # nvme0n1p2  /
        mkpart ext4 25% 100%     # nvme0n1p3  /home
        ```
        (parted 用 `數字%` 可以自動對齊，SSD 要對齊效能才會好。)
    8.  Mount Partitions: 這裡會格式化和掛載分割區，注意不要格式化的分割區要選 "Do not format"
        會先 mount / 和 /home，之後 會有 "Select UEFI Partition" 才 mount nvme0n1p1 到 /boot/efi
        mount 選項除了預設的，還要開 `discard`
    9.  Configure Installer Mirrorlist
    10. Refresh Pacman Keys
    13. Back
4.  Install Custom System: 選這個才會安裝圖形相關的軟體包，Install CLI System 不會有
    1.  Install Base Packages
        - Install Base: 選 `linux58`
        - Choose additional modules for your kernels: 按照預設即可，如果需要之後再補裝即可，網路卡模組會在之後的步驟中安裝
        - Install Hardware Dirver: Display 和 Network 都選 "Auto-install free drivers"
    2.  Install Unconfigured Desktop Environments
        1.  Install Display Server
        2.  Install Desktop environment: 只安裝 `plasma`  
            Install Common Packages: 按照預設選項。如果預設全部都是空的，就只安裝 `bash-completion ttf-dejavu xdg-user-dirs xdg-utils`  
            (註：如果在這裡沒有裝 `xdg-user-dirs`，之後必須手動執行 `LC_ALL=C xdg-user-dirs-update --force` 建立 XDG 資料夾)
        3.  Install Display Manager: 選 `sddm`
        4.  Install Networking Capabilities
            1. Display Wireless Device (optional)
            2. Install Wireless Device Packages
            3. Install Network Connection Manager: 選 `NetworkManager`
            4. Install CUPS / Printer Packages
            5. Back
        5.  Install Multimedia Support
            1. Install Sound Driver(s)
            2. Install Codecs
            3. Install Accessibility Packages
            4. Back
        6. Back
    3.  Install Bootloader: 選 `grub`
    4.  Configure Base
        1. Generate FSTAB
        2. Set Hostname
        3. Set System Locale: 都選 `en_US.UTF-8`，安裝好後再調成中文，不然家目錄底下的資料夾會是中文的。  
           （註：但也可以直接用中文安裝，之後再 `LC_ALL=C xdg-user-dirs-update --force` 轉換成英文。）
        4. Set Desktop Keyboard Layout: 選 `us`
        5. Set Timezone and Clock
        6. Set Root Password
        7. Add New User(s)
    5.  Install Custom Packages: 留空即可，可以之後再裝
    9.  Back
6.  Done

參考資料：  
[Installation with Manjaro-Architect ISO - Technical Issues and Assistance / Tutorials - Manjaro Linux Forum](https://forum.manjaro.org/t/installation-with-manjaro-architect-iso/20429)  
[Install Desktop Environments - Manjaro Linux](https://wiki.manjaro.org/index.php/Install_Desktop_Environments)

## 系統設定

以下設定接續在「安裝 Manjaro Architect」後執行

1.  顯示 GRUB 開機選單及輸出開機資訊  
    編輯 `/etc/default/grub`
    - 修改 `GRUB_TIMEOUT`
    - 刪除 `GRUB_TIMEOUT_STYLE`
    - `GRUB_CMDLINE_LINUX_DEFAULT` 刪除 `quiet`
    之後執行 `sudo update-grub`
2.  調整 sudo timeout，讓 sudo 不用隔一段時間重新輸入密碼。  
    執行 `sudo EDITOR=vi visudo -f /etc/sudoers.d/$USER`，加入 `Defaults timestamp_timeout=-1` 後儲存離開
3.  Manjaro 對 KDE 的客製化(設定工具與主題)  
    安裝 `manjaro-kde-settings sddm-breath2-theme manjaro-settings-manager-knotifier manjaro-settings-manager-kcm`  
    然後到 System Settings > Startup & Shutdown > Login Screen (SDDM) 選擇 "Breath2"
4.  中文語言設定  
    安裝 `noto-fonts-cjk`  
    到 System Settings > Regional Settings > Language 加入"繁體中文"，並移到最上面  
    到 System Settings > Regional Settings > Formats 改為"台灣 - 繁體中文"  
    到 System Settings > Locale 加入 "zh_TW.UTF-8"，然後按右鍵選 "Set as default display language and format"(註：這裡設 定的內容即為 `locale` 指令顯示的內容)  
    然後重開機
5.  `sudo pacman-mirrors --country Taiwan,Japan,United_States && sudo pacman -Syyu`
6.  到 System Settings > Search 關閉搜尋功能(因為它佔用太多CPU和RAM，此功能由 baloo 提供)
7.  關閉 KDE Wallet subsystem 以避免它一直跳出視窗要求輸入密碼，在 `~/.config/kwalletrc` 中加入以下內容
    ```
    [Wallet]
    Enabled=false
    ```
8.  系統安裝完後，systemd 的藍牙服務未開啟，`sudo systemctl enable bluetooth` 設定開機後自動啟動藍牙服務，`sudo systemctl start bluetooth` 立即啟動藍牙服務。

## 使用者設定

### Bash 初始化 script

**~/.bash_profile**: The personal initialization file, executed for login shells

``` shell
[[ -f ~/.bashrc ]] && . ~/.bashrc
```

**~/.bashrc**: The individual per-interactive-shell startup file

``` shell
# 命令列提示 PS1
# root
PS1='\[\033[01;31m\]\h\[\033[01;34m\] \W \$\[\033[00m\] '
# non-root
PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '

# 指令別名
alias ls='ls --color=auto'
alias ll='ls --color=auto -lh'
alias lld='ls --color=auto -ldh'
alias la='ls --color=auto -a'
alias lla='ls --color=auto -alh'
alias grep='grep --colour=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias cp="cp -i"                          # confirm before overwriting something
alias df='df -hT -x tmpfs -x devtmpfs'    # human-readable sizes and ignore tmpfs
alias du='du -h'                          # human-readable sizes
alias free='free -h'                      # human-readable sizes
alias more=less
alias nv='nvim'

# 環境變數
export EDITOR=/usr/bin/nvim
```

註：`~/.profile` 不會被讀取，原因不明。

### root 的 Bash 初始化 script

由於 root 沒有這些 Bash 初始化 script，所以 `sudo -i` 出來的結果是黑白的，`EDITOR` 也不對，所以執行 `sudo ln -s ~jisa/{.bash_profile,.bashrc,.xprofile} /root`

### dircolors

如果沒有 `~/.dir_colors` 的話 `cp /etc/skel/.dir_colors ~`

避免 "orphaned syminks and the files they point to" 一直閃，  
把 `ORPHAN 01;05;37;41` 改成 `ORPHAN 01;37;41`，  
`MISSING 01;05;37;41` 改成 `MISSING 01;37;41`。

### 字型

把字型檔放到 `~/.local/share/fonts`，並在 `~/.config/fontconfig/fonts.conf` 中加入以下內容

``` xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
    <!-- 預設字型 -->
    <alias binding="strong">
        <family>sans-serif</family>
        <prefer><family>Noto Sans</family></prefer>
    </alias>
    <alias binding="strong">
        <family>serif</family>
        <prefer><family>Noto Serif</family></prefer>
    </alias>
    <alias binding="strong">
        <family>monospace</family>
        <prefer>
            <family>DejaVu Sans Mono</family>
            <family>Source Han Mono TC</family>
            <family>Noto Mono</family>
        </prefer>
    </alias>
</fontconfig>
```

### 桌面捷徑

由於 KDE Plasma 的桌面沒有捷徑功能，必須依靠 `.desktop` 的方式實現。在 `~/Desktop` 新增以下三個檔案

root.desktop

``` 
[Desktop Entry]
Icon=drive-harddisk-root
Name=根目錄
Type=Link
URL[$e]=file:/
```

home.desktop

```
[Desktop Entry]
Icon=user-home
Name=家目錄
Type=Link
URL[$e]=file:$HOME
```

trash.desktop

```
[Desktop Entry]
EmptyIcon=user-trash
Icon=user-trash-full
Name=垃圾桶
Type=Link
URL[$e]=trash:/
```

## 軟體包

1. 不含在 "Manjaro Architect" 和 "系統設定" 安裝的軟體包
2. 未特別注記來源者，代表來自 Manjaro 官方庫
3. 使用 AUR 所安裝的 Python 軟體包，需在 Python 更新後重新 `makepkg`(3.8 -> 3.9 才要，3.8.1 -> 3.8.2 不用)。

### 工具類

- konsole dolphin spectacle
- ark p7zip unrar
- kcalc grpn<sup>AUR</sup>
- the_silver_searcher

相關設定：

- konsole  
  配色 "微風"，背景透明 "10%"，字型 "Monospace 12pt"
- dolphin  
  到設定 > 一般 > 行為選擇 "對所有資料夾使用相同的顯示模式"，不然 Dolphin 會在每個資料夾下建立 ".directory" 檔案
- p7zip  
  p7zip 可以壓縮和解壓縮 Zip 壓縮檔，所以不用再裝 zip 和 unzip。
- unrar  
  雖然 p7zip 可以解壓縮 rar 壓縮檔，但 ark 需要 unrar 才能解壓縮 rar 壓縮檔，所以還是得裝。

### 文書處理類

- kate
- neovim python-pynvim xsel
- okular
- wps-office<sup>AUR</sup> wps-office-mime<sup>AUR</sup> wps-office-mui-zh-tw<sup>AUR</sup> ttf-wps-fonts<sup>AUR</sup>
- typora<sup>AUR</sup>

相關設定：

- kate  
  字型 "思源等寬"
- neovim  
  設定檔 `~/.config/nvim/init.vim`
- wps-office<sup>AUR</sup>  
  wps-office 和 wps-office-mime 共用同一個 PKGBUILD  
  ttf-wps-fonts 是 WPS Office 裡方程式所需的字型
- typora<sup>AUR</sup>  
  調整字型：在「偏好設定>外觀>開啟主題佈景資料夾」開啟的資料夾中新增 `base.user.css`，內容為
  ``` css
  body {
    font-family: 'Source Han Sans TC';
  }
  ```

### 多媒體類

- viewnior
- kcolorchooser
- kolourpaint
- vlc
- kid3

### 網路類

- chromium
- JDownloader 2<sup>其它</sup>
- transmission-qt
- 4kvideodownloader<sup>AUR</sup>

相關設定：

- JDownloader 2<sup>其它</sup>
    - 到官方網站下載 Other 的 MULTIOS JAR without Installer（只有一個 `JDownloader.jar`，Linux 的 Installer 會多安裝 JRE，這個不會）複製到 `~/.local/opt/jd2` 資料夾中
    - 執行 `java -jar ~/.local/opt/jd2/JDownloader.jar` 啟動 JDownloader 2，第一次執行會下載必須的檔案到 `~/.local/opt/jd2`
    - `~/.local/opt/jd2/themes/standard/org/jdownloader/images/logo/icon.ico` 可以用來作為 Desktop Entry 的 icon

### 教育類

- stardict
- Mathematica 12.0<sup>sh</sup>
- MATLAB R2020a<sup>其它</sup>(dep: libselinux<sup>AUR</sup>(dep: libsepol<sup>AUR</sup>))
- python-sympy python-numpy python-matplotlib(dep: pyside2) python-scipy python-scikit-learn python-pytorch-opt torchvision<sup>archlinuxcn</sup> python-tensorflow-opt tensorboard python-pandas
- jupyter-calysto_scheme-git<sup>AUR</sup>(dep: jupyter-metakernel<sup>AUR</sup>)

相關設定：

- Mathematica 12.0<sup>sh</sup>  
  不使用 root 權限安裝在 `~/.local/opt`，安裝與啟用說明跟安裝檔在一起，另外還在 `~/.local/share/applications/wolfram-mathematica12.desktop` 加入 `Categories=Education;`。
- python-pytorch-opt 和 python-tensorflow-opt
  這兩個是有 AVX2 CPU optimizations 的版本（執行 `lscpu` 或 `cat /proc/cpuinfo` 可以看 CPU 有沒有支援 AVX2）。
- torchvision<sup>archlinuxcn</sup>
    - 由於 AUR 編譯不過，所以使用 archlinuxcn(Arch Linux Chinese Community Repository) 提供的 <https://repo.archlinuxcn.org/x86_64/python-torchvision-0.8.2-3-x86_64.pkg.tar.zst>。
    - 注意 PyTorch 和 TorchVision 的版本必須相符，版本資訊參考 <https://github.com/pytorch/vision#installation>。

### 開發類

- base-devel cmake ltrace strace git
- sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf python-pysdl2<sup>AUR</sup>
- sfml
- qt5-tools(dep: qt5-webkit) qt5-doc qt5-examples qtcreator pyside2
- python python-pip ipython jupyterlab
- virtualbox(dep: linux<核心版本>-virtualbox-host-modules) virtualbox-guest-iso virtualbox-ext-oracle<sup>AUR</sup>
- bochs riscv64-elf-binutils riscv64-elf-gcc riscv64-elf-gdb riscv64-elf-newlib qemu qemu-arch-extra
- visual-studio-code-bin<sup>AUR</sup>

相關設定：

- git
  2020/8/13 後，GitHub 禁止 git 使用密碼登入，需改用 Personal access token 代替密碼登入。建立 Personal access token 後，執行 `git config --global credential.helper store && echo 'https://<USERNAME>:<TOKEN>@github.com' > ~/.git-credentials`，之後就可以不用輸入密碼。注意是明碼儲存。
- virtualbox
  安裝完後執行 `sudo usermod -a -G vboxusers $USER` 並重開機，才能找到 USB 裝置。
- virtualbox-ext-oracle<sup>AUR</sup>  
  **警告！！**：virtualbox 和 virtualbox-ext-oracle<sup>AUR</sup> 的版本必須相同，否則無法啟動虛擬機。
- visual-studio-code-bin<sup>AUR</sup>
    - visual-studio-code-bin<sup>AUR</sup> 跟 community 的 code 的差別在於：前者是 Microsoft 官方發布的 binary 包，包含一些 proprietary 的功能；後者是從原始碼建置的開源版本。
    - 選用此版本的原因在於：code 會另外安裝 electron，而此版本自帶 electron，所以不用多安裝。
    - 新增檔案：~/.cache/vscode-cpptools, ~/.config/Code, ~/.vscode

### 系統類

- poppler-data qt5-translations
- ibus ibus-chewing
- tree htop lsof
- pamac-cli pamac-gtk
- timeshift
- gufw
- baobab partitionmanager
- jre-openjdk

相關設定：

- ibus  
  於 `~/.xprofile` 加入
  ``` shell
  export GTK_IM_MODULE=ibus
  export XMODIFIERS=@im=ibus
  export QT_IM_MODULE=ibus
  ibus-daemon -drx
  ```
  ibus 會安裝 Python 2，看以後更新會不會改用 Python 3
- baobab  
  mate-disk-usage-analyzer 被包在 `mate-utils` 裡，`mate-utils` 又有太多其它東西，所以不採用
- jre-openjdk  
  修正字型很丑的問題：在 `~/.bashrc` 加入 `export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on'`。參考資料：[Java Runtime Environment fonts - ArchWiki](https://wiki.archlinux.org/index.php/Java_Runtime_Environment_fonts#Overriding_the_automatically_picked_up_settings)

### 備註

*   在安裝系統的時候，於 Install Wireless Device Packages 預設勾選 dialog, iw, rp-pppoe, wireless_tools, wpa_actiond，但無法安裝。後來使用上沒問題就沒有去把它們裝上。
*   觸控板無法同時開啟邊緣滾動和兩指滾動（目前無解）  
    以前觸控版的驅動程式使用 xf86-input-synaptics 可以同時開啟邊緣滾動和兩指滾動，但由於 xf86-input-synaptics 已經停止開發，所以 Manjaro 預裝 libinput，[libinput 的官方說明文件](https://wayland.freedesktop.org/libinput/doc/latest/scrolling.html)明確指出雖然兩者都有支援，但**一次只能開啟一個**。儘管有人表示[同時安裝 lininput、xf86-input-libinput 和 xf86-input-synaptics 就可以同時開啟兩種滾動](https://forum.manjaro.org/t/enable-both-two-finger-scroll-and-edge-scroll-in-manejaro-kde/88144/8)，但由於無法測試而不採用。
*   於 2020/11/09 執行 `sudo mhwd-kernel -i linux59` 升級 kernel 和 virtualbox-host-modules 到 5.9.x 版 kernel
*   於 2021/1/1 執行 `sudo mhwd-kernel -i linux510` 升級 kernel 和 virtualbox-host-modules 到 5.10.x 版 kernel