# RISC-V SBI 介紹

## x86 的 BIOS (Basic Input/Output System)

在 x86 架構的 PC 裡，開機後會執行 BIOS 進行一些系統初始化，接著 BIOS 會準備一組「BIOS 中斷呼叫 (BIOS interrupt calls)」，
在 16-bit real mode 下執行的程式，可以使用這組中斷執行一些平台相關的功能，例如

* `int 10h` 就可以用來在螢幕上顯示文字
* `int 13h` 可以讀寫磁碟，MBR 上的 boot loader 可以利用這個中斷載入位於磁碟上的作業系統核心

不管是哪一家公司做的 BIOS，只要它遵守這個**標準**，boot loader 不需要修改就可以在各種 x86 機器上執行。

## RISC-V 的 SBI (Supervisor Binary Interface)

RISC-V 只是一個 CPU 指令集，各家公司可以配合不同的週邊設備產生出無數種平台，SBI **標準**可以讓作業系統（或裸機程式）使用同一套指令就能存取這些平台共同的部份，像是文字輸入/輸出。

目前 SBI 有幾個實現: BBL (Berkeley Boot Loader), Coreboot, U-Boot, OpenSBI 等。

## OpenSBI

OpenSBI 有以下幾個特點

* RISC-V 官方實做
* Qemu 預設的 firmware (`-bios` 選項為空時使用)
* 跳轉到下一階段程式前會進入 S (Supervisor) 模式（也可以設定 OpenSBI 進入別的模式)

Linux 在 RISC-V 架構上執行時，要求進入 kernel 前必須是 S 模式，因此必須使用 OpenSBI (或其它 SBI 實現) 來引導 kernel。

## SBI 使用方式

[RISC-V SBI specification](https://github.com/riscv/riscv-sbi-doc)

以下使用一個小型的裸機程式 `sbi_demo.S` 來示範 SBI 使用方式。

``` assembly
.global _start

_start:
        # Print a character to console
        li a7, 0x01        # Extension: Console Putchar (EID #0x01)
        li a0, 0x4B        # ASCII 'K'
        ecall
        
        # Stop current hart (to prevent host CPU keep running at 100%)
        li a7, 0x48534D    # Hart State Management Extension (EID #0x48534D "HSM")
        li a6, 0x01        # Function: HART stop (FID #1)
        ecall
        
        # Never goes here
```

然後編譯

``` shell
riscv64-elf-gcc -c -o sbi_demo.o sbi_demo.S                          # 只編譯，不連結
riscv64-elf-ld -e _start -Ttext=0x80200000 -o sbi_demo sbi_demo.o    # 設置 entry point 為 `_start`，程式開頭為 0x80200000 (Qemu RISC-V VirtIO board 指定的開頭)
```

執行 `qemu-system-riscv64 -nographic -serial mon:stdio -machine virt -kernel sbi_demo` 啟動虛擬機器

```
OpenSBI v0.8
   ____                    _____ ____ _____
  / __ \                  / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|____/_____|
        | |
        |_|

Platform Name       : riscv-virtio,qemu
Platform Features   : timer,mfdeleg
Platform HART Count : 1
Boot HART ID        : 0
Boot HART ISA       : rv64imafdcsu
BOOT HART Features  : pmp,scounteren,mcounteren,time
BOOT HART PMP Count : 16
Firmware Base       : 0x80000000
Firmware Size       : 92 KB
Runtime SBI Version : 0.2

MIDELEG : 0x0000000000000222
MEDELEG : 0x000000000000b109
PMP0    : 0x0000000080000000-0x000000008001ffff (A)
PMP1    : 0x0000000000000000-0xffffffffffffffff (A,R,W,X)
K
```

可以看到出現 `K`，之後機器進入空轉 (需要退出 Qemu 可以按下 `Ctrl-A` 後按 `X`)。