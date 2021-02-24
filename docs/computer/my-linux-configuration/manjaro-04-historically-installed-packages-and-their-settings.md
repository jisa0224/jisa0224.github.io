# Manjaro (四) 以前安裝過的軟體包及相關設定

## 工具類

* scrcpy<sup>AUR</sup>  
  只要有 `adb` 就可以執行，建置軟體包之前把 `PKGBUILD` 的 `depends` 刪掉 `android-tools`

## 文書處理類

* wps-office<sup>AUR</sup> wps-office-mime<sup>AUR</sup> wps-office-mui-zh-tw<sup>AUR</sup> ttf-wps-fonts<sup>AUR</sup>
  wps-office 和 wps-office-mime 共用同一個 PKGBUILD  
  ttf-wps-fonts 是 WPS Office 裡方程式所需的字型  
  使用 fcitx5 作為輸入法框架時，wps-office 需要以 `QT_IM_MODULE=fcitx5` 啟動，否則無法切換輸入法。  
  <https://wiki.archlinux.org/index.php/WPS_Office_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#Fcitx5_%E6%97%A0%E6%B3%95%E8%BE%93%E5%85%A5%E4%B8%AD%E6%96%87>

* typora<sup>AUR</sup>

## 多媒體類

## 網路類

* chromium
    * Chromium 自 88 版開始，停止 Google 帳戶同步功能，所以只好改用 Google Chrome。
    * 使用久了之後會儲存大量的快取，"清除瀏覽資料" 裡的 "Cookie 和其他網站資料" 可以清除 `~/.config/chromium` 裡的快取，"快取圖片和檔案" 可以清除 `~/.cache/chromium` 裡的快取。

* pepper-flash
  * Flash Player reaches end-of-life on December 31, 2020. After this date, it will be removed from the Arch repos since it is no longer supported.
  * Chromium 自 88 版開始，停止支援 Flash（裝了也沒用）。

## 教育類

* python-sympy python-scikit-learn python-pytorch-opt python-torchvision<sup>archlinuxcn</sup> python-tensorflow-opt tensorboard python-pandas
    * python-pytorch-opt 和 python-tensorflow-opt 是有 AVX2 CPU optimizations 的版本（執行 `lscpu` 或 `cat /proc/cpuinfo` 可以看 CPU 有沒有支援 AVX2）。
    * 由於 AUR 的 python-torchvision 編譯不過，所以使用 archlinuxcn(Arch Linux Chinese Community Repository) 提供的 <https://repo.archlinuxcn.org/x86_64/python-torchvision-0.8.2-3-x86_64.pkg.tar.zst>。
    * 注意 PyTorch 和 TorchVision 的版本必須相符，版本資訊參考 <https://github.com/pytorch/vision#installation>。

* octave  
  新增檔案：~/.config/octave, ~/.octave_hist

* racket
  新增檔案：~/.racket

* cling<sup>AUR</sup>
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

## 開發類

* sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf python-pysdl2<sup>AUR</sup>

* ghc ghc-static stack-static<sup>AUR</sup> stylish-haskell<sup>stack</sup> ihaskell<sup>stack</sup>
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

* code  
  新增檔案：~/.cache/vscode-cpptools, ~/.config/Code - OSS, ~/.config/Electron(執行過 `electron7` 之後才有), ~/.vscode-oss

* CLion<sup>其它</sup>
    * 安裝方式：解壓縮 `CLion-2020.1.1.tar.gz` 到 `~/.local/clion-2020.1.1`，然後執行 `~/.local/clion-2020.1.1/bin/clion.sh`。
    * 新增檔案：~/.config/JetBrains/CLion2020.1, ~/.local/share/JetBrains/CLion2020.1, ~/.local/share/applications/jetbrains-clion.desktop, ~/.gnome/apps/jetbrains-clion.desktop
    * "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔

* PyCharm<sup>其它</sup>
    * 安裝方式：解壓縮 `pycharm-professional-2020.1.1.tar.gz` 到 `~/.local/pycharm-2020.1.1`，然後執行 `~/.local/pycharm-2020.1.1/bin/pycharm.sh`
    * 新增檔案：~/.config/JetBrains/PyCharm2020.1, ~/.local/share/JetBrains/PyCharm2020.1, ~/.local/share/applications/jetbrains-pycharm.desktop, ~/.gnome/apps/jetbrains-pycharm.desktop
    * "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔

* bochs qemu qemu-arch-extra riscv64-elf-binutils riscv64-elf-newlib riscv64-elf-gcc riscv64-elf-gdb

## 系統類

* linux58-bbswitch
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

* ibus ibus-chewing  
  於 `~/.xprofile` 加入
  ``` shell
  export GTK_IM_MODULE=ibus
  export XMODIFIERS=@im=ibus
  export QT_IM_MODULE=ibus
  ibus-daemon -drx
  ```
  ibus 會安裝 Python 2，看以後更新會不會改用 Python 3