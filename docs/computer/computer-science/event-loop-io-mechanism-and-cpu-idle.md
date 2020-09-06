# 事件迴圈、I/O 機制與 CPU idle

本文中會提到的概念

  - 事件迴圈
  - 輪詢
  - Linux 中的 I/O 機制
  - 阻塞/非阻塞、同步/異步
  - CPU halt
  - CPU 使用率與 idle process

 

對於部份遊戲（例如：線上遊戲）來說，它們的程式邏輯大概會像是這樣子的

``` c
while(true) {
    if(按下滑鼠) {
    ...
    }
    if(按下鍵盤) {
    ...
    }
    if(收到網路封包) {
    ...
    }
    ...
}
```

有一個不斷執行的主迴圈，不斷檢查有沒有新事件發生，有就進行處理。

這種程式設計模式被稱為事件驅動程式設計(Event-driven programming)，通常有一個主迴圈（事件迴圈, Event loop）會一直檢查是否有新的事件（例如：I/O 事件），當有事件的時候就把該事件交給相關的事件處理器(Event Handler，通常是一個 call-back function)<sup>\[1\]</sup>。

那麼要如何得知事件有無發生，如果以 Linux 的 I/O 為例

Linux 中的 I/O 機制可分為

  - 同步 I/O (synchronous IO)
      - 阻塞 I/O (blocking IO)
      - 非阻塞 I/O (nonblocking IO)
      - I/O 多路複用 (IO multiplexing)
      - 信號驅動 I/O (signal driven IO)
  - 異步 I/O (asynchronous IO)

關於這些 I/O 機制的介紹，以及阻塞/非阻塞、同步/異步的說明，請看 <a href='{% post_path "轉載-Linux-IO模式及-select、poll、epoll详解" %}' target='_blank' rel='noopener'>[轉載] Linux IO模式及 select、poll、epoll详解</a><sup>\[2\]</sup>。

以上面的遊戲程式碼來看，如果它不需要不斷更新資料（例如：畫面）的話（例如：踩地雷），可以用阻塞 I/O 一直等到按下按鍵，如果這個踩地雷同時支援鍵盤和滑鼠的話，可以用多個非阻塞 I/O 或一個 I/O 多路複用來達成。

如果沒有輸入也要不斷更新資料（例如：貪食蛇），可能就是給它們加個超時限制。

 

在這邊我有另一個好奇的是，阻塞狀態下的 CPU 在做什麼？

首先，作業系統有一個基本原理

> 在同一時間，一個 CPU 核心（或超執行緒）只會且必有一個 process 在執行。<sup>\[3\]</sup>

這個原理很容易理解，畢竟 CPU 只要給電，就會不斷執行，可是我們去看自己電腦的 CPU 使用率的時候不是 100% ，這就與這個條件矛盾了。

這時就要先回過頭來理解「CPU 使用率」到底是什麼。

CPU 使用率是由作業系統的 process/task scheduler
計算出來，代表所有時間片段中有多少的時間有在使用<sup>\[4\]</sup>。

現代多工作業系統多是使用「分時」的方式達成，給每一個程式分配時間片段，如果某個程式正處於阻塞狀態，例如它正等待硬碟讀完資料或等待接收網路封包，那該給它的時間片段作業系統就可以不用給它。

所以對於計算密集的程式來說，如果資料都已被讀到主記憶體中，因為它只需要 CPU 計算，不會處於阻塞狀態，自然 CPU 使用率就是 100 %。

如果所有可以排程的 process 都處於阻塞狀態，那麼多餘的那些時間片段還是必須拿來執行一些東西（別忘了基本原理！），這些空閒的時間片段會被組成一個特別的 process ，叫做 idle process/task，像是 Windows 上的 System Idle Process，Linux 則是在核心一啟動時就會執行一個 id 為 0 的 process。<sup>\[5-7\]</sup>

idle process 可以是直接寫在 process/task scheduler 裡的程式片段，或者有著極低優先權的一個獨立的 process，每個 CPU 核心（超執行緒）會有一個<sup>\[5-7\]</sup>。

不同 CPU 架構和作業系統有不同方式來執行 idle process。<sup>\[5-7\]</sup>

一種最簡單的方式是 Busy waiting(Busy looping)，就是讓 CPU 跑個空迴圈<sup>\[5\]</sup>，像是

``` c
nothing:
    goto nothing;
```

在這種情況下，CPU 永遠都在執行，也就是 100%。

早期的作業系統就是這麼做的，像是 DOS、OS/2、早期的 Windows 等<sup>\[5\]</sup>。

不過現代作業系統有更好的方法，利用 CPU 提供的 `HLT`、`WAIT`、`MWAIT` （在不同 CPU 架構）等指令<sup>\[5\]</sup>，可以讓 CPU 進到低耗能的 idle 狀態，而當中斷發生時（例如：時間中斷、I/O 操作），才會從 idle 狀態醒來<sup>\[5-7\]</sup>。

 

參考資料

\[1\] [Event-driven programming - Wikipedia](https://en.wikipedia.org/wiki/Event-driven_programming) \[accessed on 2018/11/17\]  
\[2\] [Linux IO模式及 select、poll、epoll详解 - 人云思云 - SegmentFault 思否](https://segmentfault.com/a/1190000003063859) \[accessed on 2018/11/17\]  
\[3\] [What does an idle CPU do? | Many But Finite](https://manybutfinite.com/post/what-does-an-idle-cpu-do/) \[accessed on 2018/11/17\]  
\[4\] [What does CPU usage for a process actually mean - Super User](https://superuser.com/questions/675990/what-does-cpu-usage-for-a-process-actually-mean) \[accessed on 2018/11/17\]  
\[5\] [linux kernel - What does an idle CPU process do? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/361245/what-does-an-idle-cpu-process-do)  
\[6\] [cpu - What is the code for the idle process? - Stack Overflow](https://stackoverflow.com/questions/5112097/what-is-the-code-for-the-idle-process)  
\[7\] [Idle (CPU) - Wikipedia](https://en.wikipedia.org/wiki/Idle_%28CPU%29)
 
