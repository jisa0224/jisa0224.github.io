# 掛載 Virtualbox VDI 磁碟映像檔

使用 Linux 提供的 nbd (Network Block Device) 功能，加上 QEMU 提供的 qemu-nbd 工具，就可以掛載磁碟映像檔。

以下所有命令皆以 root 執行。

```
pacman -S qemu                    # 安裝 QEMU
modprobe nbd                      # 載入 Linux nbd 核心模組，載入後會出現 /dev/nbd0, /dev/nbd1, ...
qemu-nbd -c /dev/nbd0 disk.vdi    # 用 QEMU 提供的工具把 /dev/nbd0 連線到 disk.vdi，連線後 /dev/nbd0 為整顆磁碟，/dev/nbd0p1, /dev/nbd0p2, ... 為分割區
mount /dev/nbd0p1 /mnt            # 掛載分割區
```

卸載就反向進行。

```
umount /dev/nbd0p1
qemu-nbd -d /dev/nbd0
rmmod nbd
```

參考資料：[Mount a VirtualBox drive image (vdi)? - Ask Ubuntu](https://askubuntu.com/questions/19430/mount-a-virtualbox-drive-image-vdi/50290#50290)