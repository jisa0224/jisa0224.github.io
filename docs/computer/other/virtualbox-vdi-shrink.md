# 縮小 VirtualBox vdi 虛擬硬碟檔大小

Oracle VM VirtualBox Disk Image

## 清理空間（guest: Windows, 可選）

1. 我的電腦 > 對著硬碟按右鍵 > 內容 > 一般 > 磁碟清理 > 磁碟清理
2. 我的電腦 > 對著硬碟按右鍵 > 內容 > 一般 >  磁碟清理 > 磁碟清理 > 更多選項 > 程式和功能
3. 我的電腦 > 對著硬碟按右鍵 > 內容 > 一般 >  磁碟清理 > 磁碟清理 > 更多選項 > 系統還原和陰影複製

## 磁碟重整（guest: Windows）

我的電腦 > 對著硬碟按右鍵 > 內容 > 工具 > 重組

## 將未用到的磁碟空間寫 0

### guest 為 Linux

在 guest 執行 `dd if=/dev/zero of=bigemptyfile status=progress && rm bigemptyfile`

(host 的 vdi 檔不會變大，不用擔心)

### guest 為 Windows

下載 [SDelete - Windows Sysinternals | Microsoft Docs](https://docs.microsoft.com/zh-tw/sysinternals/downloads/sdelete) 後，
在命令提示字元 (cmd.exe) 執行 `sdelete64.exe -z C:`

（64-bit Windows 使用 `sdelete64.exe`，32-bit Windows 使用 `sdelete.exe`，把 `C:` 換成要清理的磁碟）

## 使用 VirtualBox 工具縮小 vdi

先將虛擬機關機

### guest 為 Linux

在 host 執行 `VBoxManage modifymedium disk <虛擬磁碟檔檔名>.vdi --compact`

（只支援 vdi）

### guest 為 Windows

## 參考資料

* [[VirtualBox] 降低 VM 中 .vdi 硬碟檔案的大小 | EPH 的程式日記](https://ephrain.net/virtualbox-%E9%99%8D%E4%BD%8E-vm-%E4%B8%AD-vdi-%E7%A1%AC%E7%A2%9F%E6%AA%94%E6%A1%88%E7%9A%84%E5%A4%A7%E5%B0%8F/)
* [How to compact VirtualBox's VDI file size? - Super User](https://superuser.com/questions/529149/how-to-compact-virtualboxs-vdi-file-size)