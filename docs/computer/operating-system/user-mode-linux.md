# User-Mode Linux

[The User-mode Linux Kernel Home Page](http://user-mode-linux.sourceforge.net/)

假設整個工作目錄在 `$WORK`

``` shell
cd $WORK

# Download and extract Linux kernel source code (using LTS version)
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.26.tar.xz
tar xf linux-5.10.26.tar.xz
mv linux-5.10.26 linux

# Download and extract Busybox source code
wget https://busybox.net/downloads/busybox-1.33.0.tar.bz2
tar xf busybox-1.33.0.tar.bz2
mv busybox-1.33.0 busybox

# Compile User Mode Linux
cd $WORK/linux
make distclean
make ARCH=um defconfig
make ARCH=um -j$(nproc) vmlinux

# Compile Busybox
cd $WORK/busybox
make distclean
make menuconfig
# Settings  --->
#     --- Build Options
#     [*] Build static binary (no shared libs)
# 編輯 Makefile.flags，刪除 `LDLIBS += m rt crypt` 中的 `crypt`
make -j$(nproc)
make install    # Busybox 會被複製到 $WORK/busybox/_install，並建立連結

# Create rootfs
cd $WORK
dd if=/dev/zero of=rootfs.img bs=1KiB count=10KiB    # total 10 MiB
mkfs.ext4 rootfs.img
mkdir /tmp/rootfsimg
sudo mount -o loop rootfs.img /tmp/rootfsimg
sudo cp -r busybox/_install/* /tmp/rootfsimg
sudo umount /tmp/rootfsimg

./linux/vmlinux uml_dir=~/.cache/uml ubd0r=rootfs.img
```