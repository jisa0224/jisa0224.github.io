# 使用 Qemu 和 Visual Studio Code 除錯 Linux kernel (RISC-V)

## 目標

* 編譯 RISC Linux kernel
* 編譯靜態連結的 Busybox 作為 initramfs
* 在 Qemu 上執行 kernel 和 initramfs
* 使用 GDB 除錯
* 使用 Visual Studio Code 閱讀 Linux kernel 原始碼
* 使用 Visual Studio Code 除錯 Linux kernel

註：由於本機是 x86_64，所以需要特別指定 `ARCH=riscv`。

## 準備工具

``` shell
sudo pacman -S --needed base-devel xmlto kmod inetutils bc libelf git cpio perl tar xz    # 編譯 Linux kernel
sudo pacman -S --needed riscv64-linux-gnu-binutils riscv64-linux-gnu-gcc riscv64-linux-gnu-gdb riscv64-linux-gnu-glibc riscv64-linux-gnu-linux-api-headers    # RISC-V Linux 工具鏈
# 注意: 不能用 riscv64-elf-*，裸機工具鏈無法用來編譯 Linux kernel
sudo pacman -S --needed qemu qemu-arch-extra
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
make ARCH=riscv CROSS_COMPILE=riscv64-linux-gnu- menuconfig
```

分別開啟或關閉以下選項

```
Kernel hacking  --->
    Compile-time checks and compiler options  --->
        [*] Compile the kernel with debug info
        [*]   Provide GDB scripts for kernel debugging
    -*- Kernel debugging
```

最後就可以開始編譯

``` shell
make ARCH=riscv CROSS_COMPILE=riscv64-linux-gnu- -j$(nproc)
```

註：RISC-V 沒有 `make bzImage` 可用，如果執行 `make vmlinux` 不會產生 `arch/riscv/boot/Image.gz`，所以只能用 `make`。

## 編譯 Busybox

``` shell
cd $WORK/busybox
make distclean
make CROSS_COMPILE=riscv64-linux-gnu- menuconfig
```

```
Settings  --->
    --- Build Options
    [*] Build static binary (no shared libs)
```

``` shell
make CROSS_COMPILE=riscv64-linux-gnu- -j$(nproc)
make CROSS_COMPILE=riscv64-linux-gnu- install      # Busybox 會被複製到 $WORK/busybox/_install，並建立連結
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
qemu-system-riscv64 -nographic -serial mon:stdio -machine virt -kernel linux/arch/riscv/boot/Image -initrd initramfs.cpio.gz -append 'console=ttyS0'
```

## Qemu + GDB 除錯

在第一個 shell 執行

``` shell
cd $WORK
qemu-system-riscv64 -s -S -nographic -serial mon:stdio -machine virt -kernel linux/arch/riscv/boot/Image -initrd initramfs.cpio.gz -append 'console=ttyS0'
```

在第二個 shell 執行

``` shell
cd $WORK
riscv64-linux-gnu-gdb -q -n -ex 'target remote :1234' linux/vmlinux
```

此時就會進入 GDB 的畫面，可以開始下斷點除錯

```
Reading symbols from linux/vmlinux...
Remote debugging using :1234
0x0000000000001000 in ?? ()
(gdb) b start_kernel
Breakpoint 1 at 0xffffffe00000272e: file init/main.c, line 849.
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
                "${workspaceFolder}/arch/riscv/include/**"
            ],
            "defines": [
                "__GNUC__",
                "__KERNEL__"
            ],
            "compilerPath": "/usr/bin/riscv64-linux-gnu-gcc",
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
            "miDebuggerPath": "/usr/bin/riscv64-linux-gnu-gdb",
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
qemu-system-riscv64 -s -S -nographic -serial mon:stdio -machine virt -kernel linux/arch/riscv/boot/Image -initrd initramfs.cpio.gz -append 'console=ttyS0'
```

接著在 Visual Studio Code **先加入一個斷點** (如 `init/main.c` 的 `star_kernel()`，要加在 `{` 那行)，然後才按下 "開始偵錯"

(如果沒加入斷點，它就會直接開始執行，即使 stopAtEntry 設為 true 也沒用，可能是 bug)

## 參考資料

* [Kernel/Traditional compilation - ArchWiki](https://wiki.archlinux.org/index.php/Kernel/Traditional_compilation)
* [Running 64- and 32-bit RISC-V Linux on QEMU — RISC-V - Getting Started Guide](https://risc-v-getting-started-guide.readthedocs.io/en/latest/linux-qemu.html)
* [在QEMU上執行64 bit RISC-V Linux. 本篇文章主要是用來記錄我的學習紀錄，嘗試在Virtual… | by Swark | Swark | Medium](https://medium.com/swark/%E5%9C%A8qemu%E4%B8%8A%E5%9F%B7%E8%A1%8C64-bit-risc-v-linux-2a527a078819)
* [使用 VSCode + qemu 搭建 Linux 内核调试环境 – CodeTalks](https://howardlau.me/programming/debugging-linux-kernel-with-vscode-qemu.html)
* [手把手教你利用VS Code+Qemu+GDB调试Linux内核 - 知乎](https://zhuanlan.zhihu.com/p/105069730)
* [visual studio code - HowTo use the VSC to navigate Linux kernel source - Stack Overflow](https://stackoverflow.com/questions/49198816/howto-use-the-vsc-to-navigate-linux-kernel-source)