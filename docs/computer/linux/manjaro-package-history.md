# Manjaro 以前安裝過的軟體包及相關設定

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
- CLion<sup>其它</sup>
    - 安裝方式：解壓縮 `CLion-2020.1.1.tar.gz` 到 `~/.local/clion-2020.1.1`，然後執行 `~/.local/clion-2020.1.1/bin/clion.sh`。
    - 新增檔案：~/.config/JetBrains/CLion2020.1, ~/.local/share/JetBrains/CLion2020.1, ~/.local/share/applications/jetbrains-clion.desktop, ~/.gnome/apps/jetbrains-clion.desktop
    - "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔
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
- linux58-bbswitch
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
- pepper-flash
  Flash Player reaches end-of-life on December 31, 2020. After this date, it will be removed from the Arch repos since it is no longer supported.
- PyCharm<sup>其它</sup>
    - 安裝方式：解壓縮 `pycharm-professional-2020.1.1.tar.gz` 到 `~/.local/pycharm-2020.1.1`，然後執行 `~/.local/pycharm-2020.1.1/bin/pycharm.sh`
    - 新增檔案：~/.config/JetBrains/PyCharm2020.1, ~/.local/share/JetBrains/PyCharm2020.1, ~/.local/share/applications/jetbrains-pycharm.desktop, ~/.gnome/apps/jetbrains-pycharm.desktop
    - "歡迎畫面 > Configure > Create Desktop Entry" 可以建立 `.desktop` 檔
- racket
  新增檔案：~/.racket
- scrcpy<sup>AUR</sup>  
  只要有 `adb` 就可以執行，建置軟體包之前把 `PKGBUILD` 的 `depends` 刪掉 `android-tools`
- octave  
  新增檔案：~/.config/octave, ~/.octave_hist