# Systemd 速查表

## Systemd 基本概念

* 整體概念: `man systemd`
* 各種 Unit 的功能 (先看概念，詳細選項之後再看):  
  `man systemd.service`, `man systemd.socket`, `man systemd.target`, `man systemd.device`, `man systemd.mount`, `man systemd.automount`, 
  `man systemd.timer`, `man systemd.swap`, `man systemd.path`, `man systemd.slice`, `man systemd.scope`
* 特殊 Unit: `man systemd.special`

## Unit 操作

* 操作服務的程式: `systemctl --help`, `man systemctl`

## 撰寫 Unit

* 每種 Unit 的共通選項: `man systemd.unit`
* 各種 Unit 的選項:  
  `man systemd.service`, `man systemd.socket`, `man systemd.target`, `man systemd.device`, `man systemd.mount`, `man systemd.automount`, 
  `man systemd.timer`, `man systemd.swap`, `man systemd.path`, `man systemd.slice`, `man systemd.scope`

## cgroups 與資源管理

* 顯示 systemd cgroups 資訊的程式: `man systemd-cgls`, `man systemd-cgtop`
* 在 Unit 檔中指定資源管理: `man systemd.resource-control`
* 立即修改執行中 Unit 的資源管理: `systemctl set-property UNIT PROPERTY=VALUE...`
* 啟動 transient service/scope/slice 的程式: `man systemd-run`
* 把已經啟動的程式加入新的 scope: <https://unix.stackexchange.com/questions/525740/how-do-i-create-a-systemd-scope-for-an-already-existing-process-from-the-command>
* 把已經啟動的程式加入現有的 scope

## Systemd Container

<https://wiki.archlinux.org/index.php/Systemd-nspawn>
<https://wiki.archlinux.org/index.php/Systemd-nspawn_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)>

* `man systemd-nspawn`, `man machinectl`

## D-Bus

<https://www.freedesktop.org/wiki/Software/dbus/>
<https://www.freedesktop.org/wiki/IntroductionToDBus/>

* `man busctl`

## Systemd 組件和工具程式列表

以 `ctl` 結尾的:

* Boot Loader: `man systemd-boot`, `man bootctl`
* `man busctl`
* 核心傾印: `man systemd-coredump`, `man coredumpctl`
* 家目錄管理: `man systemd-homed.service`, `man homectl` (預設未啟用)
* hostname: `man hostnamectl`
* 系統紀錄: `man systemd-journald.service`, `man journalctl`
* `man kernel-install`
* locale: `man systemd-localed`, `man localectl`
* 登入管理: `man systemd-logind.service`, `man loginctl`
* systemd container: `man systemd-machined.service`, `man machinectl`, `systemd-nspawn`
* 網路管理: `systemd-networkd.service`, `man networkctl` (預設未啟用，我使用 NetworkManager)
* `man portablectl`
* DNS 解析: `systemd-resolved.service`, `man resolvectl` (預設未啟用)
* 服務管理: `man systemctl`
* 時間管理: `man timedatectl`, `man systemd-timesyncd.service`
* udev 工具: `man udevadm`
* 使用者/群組管理: `man userdbctl`

以 `systemd-` 開頭的:



## 參考資料

* systemd 的 man pages
* [systemd](https://www.freedesktop.org/wiki/Software/systemd/)
* [Arch Linux - systemd](https://archlinux.org/packages/core/x86_64/systemd/)
* [systemd - ArchWiki](https://wiki.archlinux.org/index.php/Systemd)
* [systemd/User - ArchWiki](https://wiki.archlinux.org/index.php/systemd/User)
* [systemd攻略 - 简书](https://www.jianshu.com/p/8b3fba13fcad)