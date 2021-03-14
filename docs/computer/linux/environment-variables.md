# 環境變數

在 `~/.bashrc` 和 `~/.bash_profile` 內加入的環境變數**不會**被「用 Desktop Environment 啟動的程式」載入，只有「用 Shell 啟動的程式」會。

如果要讓所有程式都可以使用的環境變數，應該放在 `~/.xprofile` 或 `~/.pam_environment` 裡。

但根據 [Environment Variables : archlinux](https://www.reddit.com/r/archlinux/comments/d6ca8b/environment_variables/f0scdch?utm_source=share&utm_medium=web2x&context=3) 的說法：

> Exporting them in `~/.bashrc` does not make them available to GUI apps, only in terminal emulators/TTY and only if bash is your default shell.
> 
> Exporting from `~/.profile` only works if you do not boot directly to a Display Manager but to a TTY shell instead. And even so, only if your default shell sources that file at login, which some shells do not (e.g. `fish`).
> 
> Exporting them in `~/.xprofile` only applies if you use some Display Managers as it is explained in the [wiki](https://wiki.archlinux.org/index.php/Xprofile). If you use `startx` or `xinit`, you should export them in your `~/.xinitrc` or source your `~/.xprofile` from there. Some DMs only source `~/.xsession` instead, so in that case, one should just symlink your `~/.xprofile` to `~/.xsession`.
> 
> Exporting them in `~/.xinitrc` only works if one uses `startx`. Both `~/.xinitrc` and `~/.xprofile` are Xorg specific and won't work under Wayland or other Display Servers. I honestly have no idea what is the cleanest way of doing it under wayland and those are the kinds of things that keep me from it.

所以最好的地方就是 `~/.pam_environment`。

注意：`~/.pam_environment` 的語法和 Shell 的語法不同。

重要：根據 <https://github.com/linux-pam/linux-pam/commit/ecd526743a27157c5210b0ce9867c43a2fa27784> 說明，未來可能 `~/.pam_environment` 不會被讀取，因此只能改放在 `/etc/environment`。

備註：雖然有一說 `~/.config/environment.d` 也具有同等效果，但實測發現沒用，並不是所有 Desktop Environment 都會讀取這個資料夾裡的檔案。

參考資料：

* [Environment variables - ArchWiki](https://wiki.archlinux.org/index.php/Environment_variables)
* `man pam_env.conf`