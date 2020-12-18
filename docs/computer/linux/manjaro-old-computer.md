# Manjaro (舊電腦)

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
    1. Set Virtual Console
    2. List Devices (optional): 注意不要裝到隨身碟去
    3. Partition Disk: 使用 `parted` 分割(不會格式化)，如果已經分割過了就不用
    8. Mount Partitions: 這裡會格式化和掛載分割區，注意不要格式化的分割區要選 "Do not format"
    9. Configure Installer Mirrorlist
    10. Refresh Pacman Keys
    13. Back
4.  Install Custom System: 選這個才會安裝圖形相關的軟體包，Install CLI System 不會有
    1.  Install Base Packages
        - Install Base: 選 `linux56`
        - Choose additional modules for your kernels: 按照預設即可，如果需要之後再補裝即可，網路卡模組會在之後的步驟中安裝
        - Install Hardware Dirver: Display 和 Network 都選 "Auto-install free drivers"
    2.  Install Unconfigured Desktop Environments
        1.  Install Display Server
        2.  Install Desktop environment: 只安裝 `plasma`  
            Install Common Packages: 只安裝 `bash-completion ttf-dejavu xdg-user-dirs xdg-utils`  
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
    3.  Install Bootloader
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

### 參考資料

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
    安裝 `manjaro-kde-settings sddm-breath2-theme manjaro-settings-manager-knotifier  manjaro-settings-manager-kcm`  
    然後到 System Settings > Startup & Shutdown > Login Screen (SDDM) 選擇 "Breath2"
4.  中文語言設定  
    安裝 `noto-fonts-cjk`  
    到 System Settings > Regional Settings > Language 加入"繁體中文"，並移到最上面  
    到 System Settings > Regional Settings > Formats 改為"台灣 - 繁體中文"  
    到 System Settings > Locale 加入 "zh_TW.UTF-8"，然後按右鍵選 "Set as default display language and format"(註：這裡設 定的內容即為 `locale` 指令顯示的內容)  
    然後重開機
5.  安裝 `dbus-x11` 取代 `dbus`
6.  `sudo pacman-mirrors --country Taiwan,Japan,United_States && sudo pacman -Syyu`
7.  關機前要先關閉 Wi-Fi，不然有時候會出現 `a stop job is running for WPA supplicant` 約十分鐘後才關機。  
    (自動化方式：在 `~/.config/plasma-workspace/shutdown` 建立 shell script，內容為 `nmcli radio wifi off`，並設定為可執 行)
8.  到 System Settings > Search 關閉搜尋功能(因為它佔用太多CPU和RAM，此功能由 baloo 提供)
9.  關閉 KDE Wallet subsystem 以避免它一直跳出視窗要求輸入密碼，在 `~/.config/kwalletrc` 中加入以下內容
    ```
    [Wallet]
    Enabled=false
    ```

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

### 工具類

- konsole dolphin spectacle
- ark p7zip unrar
- kcalc grpn<sup>AUR</sup>
- the_silver_searcher

相關設定：

- konsole  
  配色 "黑底白字"，背景顏色 "#2E3436"，背景透明 "10%"，字型 "Monospace 12pt"
- dolphin  
  到設定 > 一般 > 行為選擇 "對所有資料夾使用相同的顯示模式"，不然 Dolphin 會在每個資料夾下建立 ".directory" 檔案
- p7zip  
  `p7zip` 可以壓縮和解壓縮 Zip 壓縮檔，所以不用再裝 `zip` 和 `unzip`

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
- scrcpy<sup>AUR</sup>

相關設定：

- scrcpy<sup>AUR</sup>  
  只要有 `adb` 就可以執行，建置軟體包之前把 `PKGBUILD` 的 `depends` 刪掉 `android-tools`

### 網路類

- chromium pepper-flash
- JDownloader 2<sup>sh</sup>
- transmission-qt
- 4kvideodownloader<sup>AUR</sup>

相關設定：

- JDownloader 2<sup>sh</sup>
    - 不使用 root 權限安裝到 `~/.local/jd2`。
    - 修正字型很丑的問題：到 設定 > 進階設定 開啟 "LAFSettings: Text Anti Alias" 和 "LAFSettings: Speedmeter Anti Aliasing"

### 教育類

- stardict
- Mathematica 12.0<sup>sh</sup>
- MATLAB R2020a<sup>其它</sup>(dep: libselinux<sup>AUR</sup>(dep: libsepol<sup>AUR</sup>))
- python-sympy python-numpy python-matplotlib(dep: pyside2) python-scipy python-scikit-learn python-pytorch torchvision<sup>pip3</sup> python-tensorflow tensorboard python-pandas
- jupyter-calysto_scheme-git<sup>AUR</sup>(dep: jupyter-metakernel<sup>AUR</sup>)

相關設定：

- Mathematica 12.0<sup>sh</sup>  
  不使用 root 權限安裝在 `~/.local`，安裝與啟用說明跟安裝檔在一起，另外還在 `~/.local/share/applications/wolfram-mathematica12.desktop` 加入 `Categories=Education;`。
- torchvision<sup>pip3</sup>
    - 由於 AUR 編譯不過，所以使用 pip3 安裝在使用者資料夾中。
    - 注意 PyTorch 和 TorchVision 的版本必須相符。
    - 注意移除時必須使用 `pip3 uninstall` 才會連同 `~/.local/bin` 裡的東西一起刪除。

### 開發類

- base-devel cmake ltrace strace git
- sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf python-pysdl2<sup>AUR</sup>
- qt5-tools(dep: qt5-webkit) qt5-doc qt5-examples qtcreator pyside2
- python python-pip ipython jupyterlab
- virtualbox linux57-virtualbox-host-modules virtualbox-guest-iso virtualbox-ext-oracle<sup>AUR</sup>
- bochs riscv64-linux-gnu-binutils riscv64-linux-gnu-gcc riscv64-linux-gnu-gdb qemu qemu-arch-extra
- visual-studio-code-bin<sup>AUR</sup>
- CLion<sup>其它</sup> PyCharm<sup>其它</sup>

相關設定：

- virtualbox-ext-oracle<sup>AUR</sup>  
  **警告！！**：virtualbox 和 virtualbox-ext-oracle<sup>AUR</sup> 的版本必須相同，否則無法啟動虛擬機。
- visual-studio-code-bin<sup>AUR</sup>
    - visual-studio-code-bin<sup>AUR</sup> 跟 community 的 code 的差別在於：前者是 Microsoft 官方發布的 binary 包，包含一些 proprietary 的功能；後者是從原始碼建置的開源版本。
    - 選用此版本的原因在於：code 會另外安裝 electron，而此版本自帶 electron，所以不用多安裝。
    - 新增檔案：~/.cache/vscode-cpptools, ~/.config/Code, ~/.vscode
- CLion<sup>其它</sup>
    - 安裝方式：解壓縮 `CLion-2020.1.1.tar.gz` 到 `~/.local/clion-2020.1.1`，然後執行 `~/.local/clion-2020.1.1/bin/clion.sh`。
    - 新增檔案：~/.config/JetBrains/CLion2020.1, ~/.local/share/JetBrains/CLion2020.1, ~/.local/share/applications/jetbrains-clion.desktop, ~/.gnome/apps/jetbrains-clion.desktop
    - "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔
- PyCharm<sup>其它</sup>
    - 安裝方式：解壓縮 `pycharm-professional-2020.1.1.tar.gz` 到 `~/.local/pycharm-2020.1.1`，然後執行 `~/.local/pycharm-2020.1.1/bin/pycharm.sh`
    - 新增檔案：~/.config/JetBrains/PyCharm2020.1, ~/.local/share/JetBrains/PyCharm2020.1, ~/.local/share/applications/jetbrains-pycharm.desktop, ~/.gnome/apps/jetbrains-pycharm.desktop
    - "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔

### 系統類

- poppler-data qt5-translations
- ibus ibus-chewing
- tree htop lsof
- pamac-cli pamac-gtk
- timeshift
- gufw
- baobab partitionmanager
- linux58-bbswitch
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
- linux57-bbswitch
    1. 新增 `/etc/modprobe.d/bbswitch.conf`，內容為
       ```
       blacklist nouveau
       blacklist nvidia
       options bbswitch load_state=0 unload_state=1
       ```
    2. 新增 `/etc/modules-load.d/bbswitch.conf`，內容為
       ```
       bbswitch
       ```
    3. 重開機
    參考資料：[Bumblebee - ArchWiki](https://wiki.archlinux.org/index.php/Bumblebee#Power_management)
- jre-openjdk  
  修正字型很丑的問題：在 `~/.bashrc` 加入 `export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on'`。參考資料：[Java Runtime Environment fonts - ArchWiki](https://wiki.archlinux.org/index.php/Java_Runtime_Environment_fonts#Overriding_the_automatically_picked_up_settings)

### 以前安裝過的軟體包的相關設定

- cling<sup>AUR</sup>
    兩者分別安裝好後，執行
    ``` shell
    pip install --user /opt/cling/share/cling/Jupyter/kernel
    jupyter-kernelspec install --user /opt/cling/share/cling/Jupyter/kernel/cling-cpp17
    ```
    新增和修改的檔案：
    ```
    ~/.cling_history        (執行過 cling 之後才會出現，只有直接執行 cling 的才有，從 JupyterLab 執行不會有)
    ~/.ipynb_checkpoints    (Jupyter Lab 開啟過的檔案的同個資料夾底下會出現，可以用 `find` 尋找並刪除)
    ~/.ipython              (執行過 ipython 之後才會出現，JupyterLab 會用到 ipython)
    ~/.jupyter              (Jupyter Lab 的使用者設定)
    ~/.local/share/jupyter  (Jupyter Lab 執行期資料)
    ~/.local/bin/jupyter-cling-kernel                    (`pip install` 後新增)
    ~/.local/lib/python3.8/site-packages/clingkernel*    (`pip install` 後新增)
    ~/.local/share/jupyter/kernels/cling-cpp17           (`jupyter-kernelspec install` 後新增)
    ```
    移除方式：`pip uninstall clingkernel` 和 `jupyter-kernelspec uninstall cling-cpp17`
    註：不要使用 Jupyter 官方推薦的 xeus-cling，很難用，常常發生 gcc 能過編譯但 xeus-cling 顯示錯誤。
    註：`pip install -e` 會修改 `/opt/cling/.../kernel` 和 `/usr/lib/python3.8/site-packages`，所以不要用。
- code  
  新增檔案：~/.cache/vscode-cpptools, ~/.config/Code - OSS, ~/.config/Electron(執行過 `electron7` 之後才有), ~/.vscode-oss
- ghc ghc-static stack-static<sup>AUR</sup> stylish-haskell<sup>stack</sup> ihaskell<sup>stack</sup>
    ghc 會產生 `~/.ghc`
    
    community 提供的 stack 會安裝一大堆 haskell 動態連結函式庫，stack-static<sup>AUR</sup> 是靜態連結的，所以只有一個執行檔。
    stack 會產生 `~/.stack`，如果用 stack build 的話還會在專案資料夾中產生 `.stack-work`
    
    [stylish-haskell](https://github.com/jaspervdj/stylish-haskell) 是 Haskell 的程式碼格式化工具，使用 `stack install stylish-haskell` 安裝，安裝完後會產生 `~/.local/bin/stylish-haskell`，vim 可用 `:!stylish-haskell` 進行格式化。 BUG: 設定檔不起作用
    
    使用 `stack install ihaskell` 安裝，之後 `ihaskell install` 註冊 Jupyter kernel
    新增和修改的檔案：
    ```
    ~/.local/bin/ihaskell                     (`stack install ihaskell` 後產生)
    ~/.local/share/jupyter/kernels/haskell    (`ihaskell install` 後產生)
    ~/.ihaskell                               (執行過 ihaskell 後產生)
    ```
    註：`:load` 可以使用相對位置或絕對位置，但不能用 `~`，且相對位置是相對於 `*.ipnb` 的位置，而不是開啟 Jupyter Lab 時 shell 的工  作資料夾。
       1. 平常使用 `~` 都是由 shell 轉換成家目錄的絕對位置，所以不論是 C 的 `argv` 還是 Haskell 的 `getArgs` 得到的都是家目錄的絕對位置，但不清楚為什麼 ghc 可以用，ihaskell 卻不行。
       2. Jupyter 的預設工作資料夾是 `*.ipynb` 所在的資料夾，可用 `:!pwd` 顯示、 `:!cd` 切換。
    
    安裝 ihaskell_labextension 的方法：
    ``` shell
    git clone https://github.com/gibiansky/IHaskell
    cd IHaskell/ihaskell_labextension
    npm install
    npm run build
    cp -r /usr/share/jupyter/lab ~/.local/share/jupyter/lab    # 用 `jupyter-lab path` 找到 Application directory
    JUPYTERLAB_DIR=~/.local/share/jupyter/lab jupyter labextension install .
    echo 'export JUPYTERLAB_DIR="/home/jisa/.local/share/jupyter/lab"' >> ~/.profile    # 須重新登入才會起作用
    # 以下非必要
    rm -rf node_modules/
    npm cache clean --force
    rm -rf ~/.cache/yarn
    # 之後可刪除 IHaskell 資料夾
    ```
    註：因為不想改變 /usr 的內容，但 jupyter labextension 又沒有提供安裝到使用者資料夾的選項，只能這樣做
- racket
  新增檔案：~/.racket
- octave  
  新增檔案：~/.config/octave, ~/.octave_hist

### 備註

在 2020/7/19 stable-update 後更新為 5.7 的 Linux kernel(及 kernel module)

在 2020/9/8 stable-update 後更新為 5.8 的 Linux kernel(及 kernel module)，命令：`sudo mhwd-kernel -i linux58 rmc`(rmc: remove current kernel)

## 其它

### 系統備份：使用 Timeshift

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

### 觸控板無法同時開啟邊緣滾動和兩指滾動（目前無解）

以前觸控版的驅動程式使用 xf86-input-synaptics 可以同時開啟邊緣滾動和兩指滾動，但由於 xf86-input-synaptics 已經停止開發，所以 Manjaro 預裝 libinput，[libinput 的官方說明文件](https://wayland.freedesktop.org/libinput/doc/latest/scrolling.html)明確指出雖然兩者都有支援，但**一次只能開啟一個**。儘管有人表示[同時安裝 lininput、xf86-input-libinput 和 xf86-input-synaptics 就可以同時開啟兩種滾動](https://forum.manjaro.org/t/enable-both-two-finger-scroll-and-edge-scroll-in-manejaro-kde/88144/8)，但由於無法測試而不採用。

## TODO

1. mimeapps.list
2. papirus-icon-theme, papirus-maia-icon-theme 客製化(去除 action 等圖示)