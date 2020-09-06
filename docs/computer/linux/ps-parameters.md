# ps 參數整理

## 預設

  - 除 `-pid` 以外，參數前有 `-` 的是 Unix 風格，沒有的是 BSD 風格
  - 只顯示「當前使用者」在「當前TTY」的 process
  - BSD 風格顯示執行檔名和參數，Unix 風格只顯示執行檔名
  - 使用 BSD 風格的參數都會顯示 STAT，Unix 風格不顯示 STAT

```
  PID TTY          TIME CMD
 8905 pts/0    00:00:00 bash
11683 pts/0    00:00:00 ps
```

## process 選擇

### 顯示所有 process

  - `a` 顯示「所有使用者」且「有TTY」的 process
  - `x` 顯示所有「當前使用者」的 process，不論它有沒有TTY
  - `ax` 顯示所有 process
  - `-e`, `-A` 顯示所有 process

### 根據狀態顯示

  - `r` 顯示執行中的process
  - `T` 顯示「當前TTY」的process，只加T時只有多STAT
  - `-N` 反向選擇

### 根據列表顯示

以下所有的 *list* 內容必須用空格或逗號分割，"1 2"、1,2 或 "1,2"，*userlist* 和 *grplist*
可以輸入數字或名稱。

  - `p pidlist`, `pid`, `-pid`, `-p pidlist` 顯示「PID」為 *pidlist* 或 *pid* 的 process
  - `q pidlist`,`-q pidlist` 顯示「PID」為 *pidlist* 的 process (快速模式)
  - `--ppid pidlist` 顯示「PPID」為 *pidlist* 的 process
  - `-s sesslist` 顯示「Session ID」為 *sesslist* 的 process
  - `-C cmdlist` 顯示「執行檔名」為 *cmdlist* 的 process
  - `-U userlist` 顯示「Real UID」為 *userlist* 的 process
  - `-u userlist` 顯示「Effective UID」為 *userlist* 的 process
  - `-G grplist` 顯示「Real GID」為 *grplist* 的 process
  - `-g grplist` 顯示「Effective GID」為 *grplist* 的 process
  - `t ttylist`, `-t ttylist` 顯示「TTY」為 *ttylist* 的 process

<span style="color: #ff0000;">注意：「顯示所有 process」的參數會把「根據列表顯示」的效果蓋掉！</span>

## 顯示 thread

BSD 風格參數單獨使用時顯示範圍等於 `x`

  - `H` 顯示thread (像普通 process)
  - `m`, `-m` 顯示 thread (以 - 代替 thread)
  - `-L` 顯示 thread 及其 LWP(=SPID)和 NLWP (要 `-f` 才會顯示)
  - `-T` 顯示 thread 及其 SPID

## 輸出樣式

BSD 風格參數單獨使用時顯示範圍等於 `x`  
以下命令皆指定一個 process 作為範例

### BSD 風格輸出樣式

  - `l` BSD long-format
    
    ```
    F   UID   PID  PPID PRI  NI    VSZ   RSS WCHAN  STAT TTY        TIME COMMAND
    0  1001 10130 10104  20   0 616000 40260 poll_s Sl+  pts/1      0:00 vim a.c
    ```

  - `j` BSD job control format
    
    ```
    PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND
    10104 10130 10130 10104 pts/1    10130 Sl+   1001   0:00 vim a.c
    ```

  - `s` signal format
    
    ```
    UID   PID          PENDING          BLOCKED          IGNORED           CAUGHT STAT TTY        TIME COMMAND
    1001 10130 0000000000000000 0000000000000000 0000000000003000 00000001ed804eff Sl+  pts/1      0:00 vim a.c
    ```

  - `u` user-oriented format
    
    ```
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    jisa0    10130  0.2  0.2 616000 40260 pts/1    Sl+  17:30   0:00 vim a.c
    ```

  - `v` virtual memory format
    
    ```
      PID TTY      STAT   TIME  MAJFL   TRS   DRS   RSS %MEM COMMAND
    10130 pts/1    Sl+    0:00      0  2416 613583 40260  0.2 vim a.c
    ```

  - `X` registar format
    
    ```
      PID   STACKP      ESP      EIP TMOUT ALARM STAT TTY        TIME COMMAND
    10130 e8696310 e8695890 ae698073     -     - Sl+  pts/1      0:00 vim a.c
    ```

### Unix 風格輸出樣式

  - `-f` full-format，會顯示命令的參數
    
    ```
    UID        PID  PPID  C STIME TTY      STAT   TIME CMD
    jisa0    10130 10104  0 17:30 pts/1    Sl+    0:00 vim a.c
    ```

  - `-F` extra full-format (imply `-f`)
    
    ```
    UID        PID  PPID  C    SZ   RSS PSR STIME TTY      STAT   TIME CMD
    jisa0    10130 10104  0 154000 40260  0 17:30 pts/1    Sl+    0:00 vim a.c
    ```

  - `-l` long-format
    
    ```
    F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY        TIME CMD
    0 S  1001 10130 10104  0  80   0 - 154000 poll_s pts/1     0:00 vim a.c
    ```

  - `-ly` long-format 換掉一些參數
    
    ```
    S   UID   PID  PPID  C PRI  NI   RSS    SZ WCHAN  TTY        TIME CMD
    S  1001 10130 10104  0  80   0 40260 154000 poll_s pts/1     0:00 vim a.c
    ```

  - `-j` jobs format
    
    ```
    PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND
    10104 10130 10130 10104 pts/1    10130 Sl+   1001   0:00 vim a.c
    ```

其它

  - `o`, `-o` "format" 使用者自訂樣式
  - `O`, `-O` "format" 等於 o 再加一些東西
  - `f` 輸出樹狀圖
  - `w`, `-w` wide output
  - `ww`, `-ww` unlimited wide output

參考資料：`man ps` 和 `ps --help all`
 
