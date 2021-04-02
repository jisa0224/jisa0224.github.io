# Qemu RISC-V VirtIO board 開機流程

Qemu 支援以下幾種 RISC-V 機器，本文將介紹 `virt` 的開機流程。

```
$ qemu-system-riscv64 -machine help
Supported machines are:
microchip-icicle-kit Microchip PolarFire SoC Icicle Kit
none                 empty machine
sifive_e             RISC-V Board compatible with SiFive E SDK
sifive_u             RISC-V Board compatible with SiFive U SDK
spike                RISC-V Spike board (default)
virt                 RISC-V VirtIO board
```

本文會同時藉由 GDB 除錯及 Qemu 原始碼來分析。

通用的 GDB 除錯流程為

* 在第一個視窗執行 `qemu-system-riscv64 -s -S -nographic -serial mon:stdio -machine virt` (需要退出 Qemu 可以按下 `Ctrl-A` 後按 `X`)
* 在第二個視窗執行 `riscv64-elf-gdb -q -n -ex 'target remote :1234'`

## 與開機相關的 Qemu 程式碼

``` c
// [Qemu 原始碼]/hw/riscv/virt.c

#if defined(TARGET_RISCV32)
# define BIOS_FILENAME "opensbi-riscv32-generic-fw_dynamic.bin"
#else
# define BIOS_FILENAME "opensbi-riscv64-generic-fw_dynamic.bin"
#endif

static const struct MemmapEntry {
    hwaddr base;
    hwaddr size;
} virt_memmap[] = {
    [VIRT_DEBUG] =       {        0x0,         0x100 },
    [VIRT_MROM] =        {     0x1000,        0xf000 },
    [VIRT_TEST] =        {   0x100000,        0x1000 },
    [VIRT_RTC] =         {   0x101000,        0x1000 },
    [VIRT_CLINT] =       {  0x2000000,       0x10000 },
    [VIRT_PCIE_PIO] =    {  0x3000000,       0x10000 },
    [VIRT_PLIC] =        {  0xc000000, VIRT_PLIC_SIZE(VIRT_CPUS_MAX * 2) },
    [VIRT_UART0] =       { 0x10000000,         0x100 },
    [VIRT_VIRTIO] =      { 0x10001000,        0x1000 },
    [VIRT_FLASH] =       { 0x20000000,     0x4000000 },
    [VIRT_PCIE_ECAM] =   { 0x30000000,    0x10000000 },
    [VIRT_PCIE_MMIO] =   { 0x40000000,    0x40000000 },
    [VIRT_DRAM] =        { 0x80000000,           0x0 },
};

static void virt_machine_init(MachineState *machine)
{
    ...
    const struct MemmapEntry *memmap = virt_memmap;
    ...
    target_ulong start_addr = memmap[VIRT_DRAM].base;
    ...
    firmware_end_addr = riscv_find_and_load_firmware(machine, BIOS_FILENAME,
                                                     start_addr, NULL);

    if (machine->kernel_filename) {
        kernel_start_addr = riscv_calc_kernel_start_addr(machine,
                                                         firmware_end_addr);

        kernel_entry = riscv_load_kernel(machine->kernel_filename,
                                         kernel_start_addr, NULL);

        ...
        }
    } else {
       /*
        * If dynamic firmware is used, it doesn't know where is the next mode
        * if kernel argument is not set.
        */
        kernel_entry = 0;
    }
    ...
    /* Compute the fdt load address in dram */
    fdt_load_addr = riscv_load_fdt(memmap[VIRT_DRAM].base,
                                   machine->ram_size, s->fdt);
    /* load the reset vector */
    riscv_setup_rom_reset_vec(start_addr, virt_memmap[VIRT_MROM].base,
                              virt_memmap[VIRT_MROM].size, kernel_entry,
                              fdt_load_addr, s->fdt);
    ...
}

// [Qemu 原始碼]/include/hw/riscv/boot.h

target_ulong riscv_find_and_load_firmware(MachineState *machine,
                                          const char *default_machine_firmware,
                                          hwaddr firmware_load_addr,
                                          symbol_fn_t sym_cb);

// [Qemu 原始碼]/hw/riscv/boot.c

void riscv_setup_rom_reset_vec(hwaddr start_addr, hwaddr rom_base,
                               hwaddr rom_size, uint64_t kernel_entry,
                               uint32_t fdt_load_addr, void *fdt)
{
    int i;
    uint32_t start_addr_hi32 = 0x00000000;

    #if defined(TARGET_RISCV64)
    start_addr_hi32 = start_addr >> 32;
    #endif
    /* reset vector */
    uint32_t reset_vec[10] = {
        0x00000297,                  /* 1:  auipc  t0, %pcrel_hi(fw_dyn) */
        0x02828613,                  /*     addi   a2, t0, %pcrel_lo(1b) */
        0xf1402573,                  /*     csrr   a0, mhartid  */
#if defined(TARGET_RISCV32)
        0x0202a583,                  /*     lw     a1, 32(t0) */
        0x0182a283,                  /*     lw     t0, 24(t0) */
#elif defined(TARGET_RISCV64)
        0x0202b583,                  /*     ld     a1, 32(t0) */
        0x0182b283,                  /*     ld     t0, 24(t0) */
#endif
        0x00028067,                  /*     jr     t0 */
        start_addr,                  /* start: .dword */
        start_addr_hi32,
        fdt_load_addr,               /* fdt_laddr: .dword */
        0x00000000,
                                     /* fw_dyn: */
    };

    /* copy in the reset vector in little_endian byte order */
    for (i = 0; i < ARRAY_SIZE(reset_vec); i++) {
        reset_vec[i] = cpu_to_le32(reset_vec[i]);
    }
    rom_add_blob_fixed_as("mrom.reset", reset_vec, sizeof(reset_vec),
                          rom_base, &address_space_memory);
    riscv_rom_copy_firmware_info(rom_base, rom_size, sizeof(reset_vec),
                                 kernel_entry);

    return;
}

// [Qemu 原始碼]/include/hw/riscv/boot_opensbi.h

/** Expected value of info magic ('OSBI' ascii string in hex) */
#define FW_DYNAMIC_INFO_MAGIC_VALUE     0x4942534f

/** Maximum supported info version */
#define FW_DYNAMIC_INFO_VERSION         0x2

/** Possible next mode values */
#define FW_DYNAMIC_INFO_NEXT_MODE_U     0x0
#define FW_DYNAMIC_INFO_NEXT_MODE_S     0x1
#define FW_DYNAMIC_INFO_NEXT_MODE_M     0x3

/** Representation dynamic info passed by previous booting stage */
struct fw_dynamic_info {
    /** Info magic */
    target_long magic;
    /** Info version */
    target_long version;
    /** Next booting stage address */
    target_long next_addr;
    /** Next booting stage mode */
    target_long next_mode;
    /** Options for OpenSBI library */
    target_long options;
    /**
     * Preferred boot HART id
     *
     * It is possible that the previous booting stage uses same link
     * address as the FW_DYNAMIC firmware. In this case, the relocation
     * lottery mechanism can potentially overwrite the previous booting
     * stage while other HARTs are still running in the previous booting
     * stage leading to boot-time crash. To avoid this boot-time crash,
     * the previous booting stage can specify last HART that will jump
     * to the FW_DYNAMIC firmware as the preferred boot HART.
     *
     * To avoid specifying a preferred boot HART, the previous booting
     * stage can set it to -1UL which will force the FW_DYNAMIC firmware
     * to use the relocation lottery mechanism.
     */
    target_long boot_hart;
};

// [Qemu 原始碼]/hw/riscv/boot.c

void riscv_rom_copy_firmware_info(hwaddr rom_base, hwaddr rom_size,
                              uint32_t reset_vec_size, uint64_t kernel_entry)
{
    struct fw_dynamic_info dinfo;
    size_t dinfo_len;

    dinfo.magic = fw_dynamic_info_data(FW_DYNAMIC_INFO_MAGIC_VALUE);
    dinfo.version = fw_dynamic_info_data(FW_DYNAMIC_INFO_VERSION);
    dinfo.next_addr = fw_dynamic_info_data(kernel_entry);
    dinfo.next_mode = fw_dynamic_info_data(FW_DYNAMIC_INFO_NEXT_MODE_S);
    dinfo.options = 0;
    dinfo.boot_hart = 0;
    dinfo_len = sizeof(dinfo);

    /**
     * copy the dynamic firmware info. This information is specific to
     * OpenSBI but doesn't break any other firmware as long as they don't
     * expect any certain value in "a2" register.
     */
    if (dinfo_len > (rom_size - reset_vec_size)) {
        error_report("not enough space to store dynamic firmware info");
        exit(1);
    }

    rom_add_blob_fixed_as("mrom.finfo", &dinfo, dinfo_len,
                           rom_base + reset_vec_size,
                           &address_space_memory);
}
```

## 說明

* 若未指定 firmware，則載入 opensbi-riscv64-generic-fw_dynamic.bin 到 0x80000000 (`VIRT_DRAM` 的開頭)
* 若有指定 kernel，則載入到 `kernel_start_addr` (該位址等於 `VIRT_DRAM` + firmware 大小，然後進行 2 MiB 對齊的值，即 0x80200000)
* 複製 reset vector 到 0x1000 (`VIRT_MROM` 的開頭)，reset vector 包含
  * 一段跳轉到 firmware 的程式碼
  * firmware 的進入點位址 (`start`)
  * Flattened Device Tree 儲存的記憶體位址 (`fdt_laddr`)
* 準備 OpenSBI (fw_dynamic) 所需的 fw_danamic_info 資料，寫入到 reset vector 的後面，reset vector 裡存著 kernel 進入點的記憶體位址

據 [riscv/opensbi: RISC-V Open Source Supervisor Binary Interface](https://github.com/riscv/opensbi) 說明，OpenSBI 有三種方式啟動下一階段程式

* Firmware with Payload (FW_PAYLOAD): 直接將下一階段程式黏在 OpenSBI 後面
* Firmware with Jump Address (FW_JUMP): 直接跳轉到一個硬編碼的記憶體位址
* Firmware with Dynamic Information (FW_DYNAMIC): 利用暫存器傳遞關於下一階段程式的資訊 (像是程式進入點的記憶體位址)

    The previous booting stage will pass information to FW_DYNAMIC by creating struct `fw_dynamic_info` in memory and 
    passing it's address to FW_DYNAMIC via a2 register of RISC-V CPU.

## 執行

由 GDB 的 `info all-registers` 可以看到 (以下省略無法顯示和不太重要的暫存器)，開機後

* 資料暫存器都是 0 (zero, ra, sp, gp, tp, t0-t6, fp, s1, a0-a11)
* pc = 0x1000，即 `VIRT_MROM` 的開頭位址
* CSR 都是 0 (mstatus, medeleg, mie, mtvec, mscratch, mepc, mcause, mtval, mip, mvendorid, marchid, mimpid, mhartid)
* misa = 0x800000000014112d (RV64ACDFIMSU)
* priv = 0x3 (Machine)，特權等級是 M

`VIRT_MROM` 的內容為

* reset vector 前半 (負責跳轉到 firmware 的程式碼)
  ```
  (gdb) disassemble/r 0x1000,+24
  Dump of assembler code from 0x1000 to 0x1018:
  => 0x0000000000001000:  97 02 00 00     auipc   t0,0x0
     0x0000000000001004:  13 86 82 02     addi    a2,t0,40 # 0x1028
     0x0000000000001008:  73 25 40 f1     csrr    a0,mhartid
     0x000000000000100c:  83 b5 02 02     0x202b583
     0x0000000000001010:  83 b2 82 01     0x182b283
     0x0000000000001014:  67 80 02 00     jr      t0
  End of assembler dump.
  ```
* reset vector 後半 (`start` 和 `fdt_laddr`)
  ```
  (gdb) x/4xw 0x1018
  0x1018: 0x80000000      0x00000000      0x87e00000      0x00000000
  ```
* 要傳遞給 OpenSBI 的 `fw_danamic_info` (位於 reset vector 正後方)
  ```
  (gdb) x/6xg 0x1028
  0x1028: 0x000000004942534f      0x0000000000000002
  0x1038: 0x0000000000000000      0x0000000000000001
  0x1048: 0x0000000000000000      0x0000000000000000
  ```

在即將跳轉到 firmware (OpenSBI) 前

```
0x0000000000001000 in ?? ()
(gdb) set disassemble-next-line on
(gdb) b *0x1014
Breakpoint 1 at 0x1014
(gdb) c
Continuing.

Breakpoint 1, 0x0000000000001014 in ?? ()
=> 0x0000000000001014:  67 80 02 00     jr      t0
```

* t0 = 0x80000000，即接下來 firmware (OpenSBI) 的進入點位址 (`start`)
* a1 = 0x87e00000，即要傳遞給 Linux kernel 的 Flattened Device Tree 的記憶體位址 (`fdt_laddr`)
* a2 = 0x1028，即要傳遞給 OpenSBI 的 `fw_dynamic_info` 的記憶體位址

## 使用簡易的 kernel 測試

以下使用一個小型的裸機程式 `sbi_demo.S` 來測試。

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