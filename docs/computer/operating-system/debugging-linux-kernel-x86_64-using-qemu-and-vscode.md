# 使用 Qemu 和 Visual Studio Code 除錯 Linux kernel (x86_64)

## 目標

* 編譯 x86_64 Linux kernel
* 編譯靜態連結的 Busybox 作為 initramfs
* 在 Qemu 上執行 kernel 和 initramfs
* 使用 GDB 除錯
* 使用 Visual Studio Code 閱讀 Linux kernel 原始碼
* 使用 Visual Studio Code 除錯 Linux kernel

註：由於本機就是 x86_64，所以不用特別指定 `ARCH`。

## 準備工具

``` shell
sudo pacman -S --needed base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz    # 編譯 Linux kernel
sudo pacman -S --needed musl kernel-headers-musl    # 編譯靜態連結的 Busybox
sudo pacman -S --needed qemu
```

另外安裝 Visual Studio Code

## 準備環境與下載檔案

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
```

## 編譯 Linux kernel

``` shell
cd $WORK/linux
make distclean
make menuconfig
```

分別開啟或關閉以下選項

```
Processor type and features ---->
    [] Randomize the address of the kernel image (KASLR)
Kernel hacking  --->
    [*] Kernel debugging
    Compile-time checks and compiler options  --->
        [*] Compile the kernel with debug info
        [*]   Provide GDB scripts for kernel debugging
```

最後就可以開始編譯

``` shell
make -j$(nproc) bzImage
```

註：執行 `make bzImage` 可以只編譯 kernel 而不編譯 kernel modules (`make` 會編譯全部)，速度比較快 (在本機使用 `-j8` 只須 5 分鐘)。

註：Qemu 沒辦法直接讀取未壓縮的 vmlinux，所以不能用 `make vmlinux`。

## 編譯 Busybox

``` shell
cd $WORK/busybox
make distclean
make menuconfig
```

```
Settings  --->
    --- Build Options
    [*] Build static binary (no shared libs)
```

``` shell
make -j$(nproc) CC=musl-gcc    # Arch Linux 自帶的 gcc 不包含一些靜態函式庫 (如 libcrypt.a)，所以連結時會出錯，改用 musl 就沒問題
make install CC=musl-gcc       # Busybox 會被複製到 $WORK/busybox/_install，並建立連結
```

## 建立 initramfs

``` shell
cd $WORK
mkdir initramfs
cp -r busybox/_install/* initramfs
cd initramfs
mkdir -p bin sbin usr/{bin,sbin} etc proc sys
echo '#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
exec /bin/sh' > init
chmod +x init
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
```

## Qemu 執行

``` shell
cd $WORK
qemu-system-x86_64 -kernel linux/arch/x86_64/boot/bzImage -initrd initramfs.cpio.gz
```

## Qemu + GDB 除錯

在第一個 shell 執行

``` shell
cd $WORK
qemu-system-x86_64 -s -S -kernel linux/arch/x86_64/boot/bzImage -initrd initramfs.cpio.gz
```

在第二個 shell 執行

``` shell
cd $WORK
gdb -q -n -ex 'target remote :1234' linux/vmlinux
```

此時就會進入 GDB 的畫面，可以開始下斷點除錯

```
Reading symbols from linux/vmlinux...
Remote debugging using :1234
0x000000000000fff0 in exception_stacks ()
(gdb) b start_kernel
Breakpoint 1 at 0xffffffff82b39aa1: file init/main.c, line 849.
(gdb) c
Continuing.

Breakpoint 1, start_kernel () at init/main.c:849
849     {
```

## 讓 Visual Studio Code 的 C/C++ IntelliSense 可以掃描到 header files

在 `$WORK/linux` 開啟 Visual Studio Code

Ctrl-P 開啟 "C/C++: Edit Configurations (JSON)"

``` json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/include/**",
                "${workspaceFolder}/arch/x86/include/**"
            ],
            "defines": [
                "__GNUC__",
                "__KERNEL__"
            ],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
```

## 使用 Visual Studio Code 除錯

執行與偵錯 > "建立 launch.json 檔案" > "C++ (GDB/LLDB)"

``` json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "miDebuggerServerAddress": "localhost:1234",
            "program": "${workspaceFolder}/vmlinux",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "啟用 gdb 的美化顯示",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

在第一個 shell 執行

``` shell
cd $WORK
qemu-system-x86_64 -s -S -kernel linux/arch/x86_64/boot/bzImage -initrd initramfs.cpio.gz
```

接著在 Visual Studio Code **先加入一個斷點** (如 `init/main.c` 的 `star_kernel()`，要加在 `{` 那行)，然後才按下 "開始偵錯"

(如果沒加入斷點，它就會直接開始執行，即使 stopAtEntry 設為 true 也沒用，可能是 bug)

## 參考資料

* [Kernel/Traditional compilation - ArchWiki](https://wiki.archlinux.org/index.php/Kernel/Traditional_compilation)
* [使用 VSCode + qemu 搭建 Linux 内核调试环境 – CodeTalks](https://howardlau.me/programming/debugging-linux-kernel-with-vscode-qemu.html)
* [手把手教你利用VS Code+Qemu+GDB调试Linux内核 - 知乎](https://zhuanlan.zhihu.com/p/105069730)
* [visual studio code - HowTo use the VSC to navigate Linux kernel source - Stack Overflow](https://stackoverflow.com/questions/49198816/howto-use-the-vsc-to-navigate-linux-kernel-source)