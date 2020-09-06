# 【CS:APP 筆記】x86_64 中的 JMP 指令整理

章節：3.6.3  
頁數：P. 206

## 理論情況

對於 JMP 指令，在邏輯上應該會有6種，分別是

<table>
  <tbody>
    <tr>
      <th style="text-align: center; vertical-align: middle;">指令</th>
      <th style="text-align: center; vertical-align: middle;">功能</th>
      <th style="text-align: center; vertical-align: middle;">跳躍</th>
      <th style="text-align: center; vertical-align: middle;">取值</th>
      <th style="text-align: center; vertical-align: middle;">x86_64 指令集</th>
      <th style="text-align: center; vertical-align: middle;">備註 </th>
    </tr>
    <tr>
      <td>jmpr <em>imm</em></td>
      <td>IP ← IP + <em>imm</em></td>
      <td style="text-align: center; vertical-align: middle;">相對</td>
      <td style="text-align: center; vertical-align: middle;">直接</td>
      <td>JMP <i>rel8</i>: jump short<br />JMP <i>rel16</i>: jump near, relative<br />JMP <i>rel32</i>: jump near, relative</td>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td>jmpr <em>reg</em></td>
      <td>IP ← IP + R[<em>reg</em>]</td>
      <td style="text-align: center; vertical-align: middle;">相對</td>
      <td style="text-align: center; vertical-align: middle;">間接</td>
      <td style="text-align: center; vertical-align: middle;">✘</td>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td>jmpr <em>mem</em></td>
      <td>IP ← IP + M[<em>mem</em>]</td>
      <td style="text-align: center; vertical-align: middle;">相對</td>
      <td style="text-align: center; vertical-align: middle;">間接</td>
      <td style="text-align: center; vertical-align: middle;">✘ </td>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td>jmpa <em>imm</em></td>
      <td>IP ← <em>imm</em></td>
      <td style="text-align: center; vertical-align: middle;">絕對</td>
      <td style="text-align: center; vertical-align: middle;">直接</td>
      <td>JMP <i>ptr16:16</i>: jump far, absolute<br />JMP <i>ptr16:32</i>: jump far, absolute</td>
      <td>如果不想用到分段的話，<br />其實可以先把位址放到暫存器裡，<br />再用 JMP <i>r64</i> 來跳躍</td>
    </tr>
    <tr>
      <td>jmpa <em>reg</em></td>
      <td>IP ← R[<em>reg</em>]</td>
      <td style="text-align: center; vertical-align: middle;">絕對</td>
      <td style="text-align: center; vertical-align: middle;">間接</td>
      <td>JMP <i>r16</i>: jump near, absolute indirect<br />JMP <i>r32</i>: jump near, absolute indirect<br />JMP <i>r64</i>: jump near, absolute indirect</td>
      <td>&nbsp;</td>
    </tr>
    <tr>
      <td>jmpa <em>mem</em></td>
      <td>IP ← M[<em>mem</em>]</td>
      <td style="text-align: center; vertical-align: middle;">絕對</td>
      <td style="text-align: center; vertical-align: middle;">間接</td>
      <td>JMP <i>m16</i>: jump near, absolute indirect<br />JMP <i>m32</i>: jump near, absolute indirect<br />JMP <i>m64</i>: jump near, absolute indirect<br />JMP <i>m16:16</i>: jump far, absolute indirect<br />JMP <i>m16:32</i>: jump far, absolute indirect<br />JMP <i>m16:64</i>: jump far, absolute indirect</td>
      <td>&nbsp;</td>
    </tr>
  </tbody>
</table>

其中

  - IP 為 instruction pointer
  - jmpr 為相對跳躍(relative jump)，其參數為距離(現在這條 JMP 指令的)下一條的位移(displacement)
  - jmpa 為絕對跳躍(absolute jump)，其參數為一個記憶體位址
  - *imm* 為立即數，*reg* 為暫存器，*mem* 為指標(可以是立即數或是 `imm + reg1 + reg2 * scale` 這樣的形式)
  - R\[*reg*\] 為暫存器內容，M\[*mem*\] 為 dereference

## x86\_64 指令集的情況

在這裡會用 `echo -n -e '\xHH\xHH' > file` 或是 nasm 來得到二進位檔  
用 nasm 時記得在最前面加上 `BITS 64`，不然會出現 `error: instruction not supported in 16-bit mode`

然後用不同的工具得到其反組譯後的結果來進行對照  
AT\&T 語法：`objdump -b binary -m i386 -D file`  
Intel 語法(應該是 MASM)：`objdump -b binary -m i386 -M intel -D file`  
Intel 語法(NASM)：`ndisasm -b 64 file`  
註：在這裡因為二進位檔裡的內容只有指令而沒有 ELF 相關的東西，所以要指定模式

<table>
  <tbody>
    <tr>
      <th style="text-align: center; vertical-align: middle;" rowspan="2">助憶碼<br />Opcode</th>
      <th style="text-align: center; vertical-align: middle;" rowspan="2">功能</th>
      <th style="text-align: center; vertical-align: middle;" colspan="4">範例</th>
    </tr>
    <tr>
      <th style="text-align: center; vertical-align: middle;">二進位碼</th>
      <th style="text-align: center; vertical-align: middle;">AT&amp;T 語法</th>
      <th style="text-align: center; vertical-align: middle;">Intel 語法<br />(應該是 MASM)</th>
      <th style="text-align: center; vertical-align: middle;"> Intel 語法<br />(NASM)</th>
    </tr>
    <tr>
      <td>JMP <em>rel8</em> <br />EB</td>
      <td>RIP ← RIP + 0xc</td>
      <td>EB 0A</td>
      <td>jmp 0xc</td>
      <td>jmp 0xc</td>
      <td>jmp short 0xc</td>
    </tr>
    <tr>
      <td rowspan="2">JMP <em>rel32</em> <br />E9</td>
      <td>RIP ← RIP + 0xf</td>
      <td>E9 0A 00 00 00</td>
      <td>jmp 0xf</td>
      <td>jmp 0xf</td>
      <td>jmp 0xf</td>
    </tr>
    <tr>
      <td>RIP ← RIP + 0x402680</td>
      <td>E9 74 26 40 00</td>
      <td>jmp 0x402680</td>
      <td>jmp 0x402680</td>
      <td>jmp 0x402680</td>
    </tr>
    <tr>
      <td>JMP <em>r64</em> <br />FF</td>
      <td>RIP ← R[RAX]</td>
      <td>FF E0</td>
      <td>jmp *%eax</td>
      <td>jmp eax</td>
      <td>jmp rax</td>
    </tr>
    <tr>
      <td rowspan="3">JMP <em>m64</em> <br />FF</td>
      <td>RIP ← M[R[RAX]]</td>
      <td>FF 20</td>
      <td>jmp *(%eax)</td>
      <td>jmp DWORD PTR [eax]</td>
      <td>jmp [rax]</td>
    </tr>
    <tr>
      <td>RIP ← M[0x402680 + R[RAX] * 8]</td>
      <td>FF 24 C5 80 26 40 00</td>
      <td>jmp *0x402680(,%eax,8)</td>
      <td>jmp DWORD PTR [eax*8+0x402680]</td>
      <td>jmp [rax*8+0x402680]</td>
    </tr>
    <tr>
      <td>RIP ← M[0x402680] </td>
      <td>FF 24 25 80 26 40 00</td>
      <td>jmp *0x402680(,%eiz,1)</td>
      <td>jmp DWORD PTR [eiz*1+0x402680]</td>
      <td>jmp [0x402680]</td>
    </tr>
  </tbody>
</table>

從以上可以看到

  - 只要是間接取值的(也就是參數為暫存器或指標位址)，AT\&T 語法裡就會有 `( )` 和 `*` 出現，Intel 語法裡則是 `[ ]`。
  - 不論是 AT\&T 還是 Intel 語法都無法直接看出是相對還是絕對跳躍，但是因為 x86\_64 指令的關係(見最上面的表)，就算不標明是絕對還是相對，也不會認錯，因為只有直接數、ptrX:X 或 mX:X 是相對跳躍，其它的都是絕對跳躍。
  - 特別注意 `jmp rax` 和 `jmp [rax]` 的差別，以及 `jmp 0x402680` 和 `jmp [0x402680]` 的差別，不要搞混了。 
  - eiz 是一個偽暫存器(psuedo-register)，其內容恆為0。
  - 如果想要 `RIP ← (0x402680 + R[RAX] * 8)` 的話，需要 `lea rax, [rax*8+0x402680]` 然後 `jmp rax` 才行。

參考資料：  
[Intel® 64 and IA-32 Architectures Software Developer Manuals](https://software.intel.com/en-us/articles/intel-sdm)  
[shell - echo bytes to a file - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/118247/echo-bytes-to-a-file)  
[reverse engineering - Disassembling A Flat Binary File Using objdump - Stack Overflow](https://stackoverflow.com/questions/14290879/disassembling-a-flat-binary-file-using-objdump)  
[assembly - x86 jmp asterisk %eax - Stack Overflow](https://stackoverflow.com/questions/30802831/x86-jmp-asterisk-eax)  
[assembly - x86 jmp to register - Stack Overflow](https://stackoverflow.com/questions/10272027/x86-jmp-to-register)  
[x86 64 - What does an asterisk \* before an address mean in x86-64 AT\&T assembly? - Stack Overflow](https://stackoverflow.com/questions/9223756/what-does-an-asterisk-before-an-address-mean-in-x86-64-att-assembly)  
[assembly - How can I tell if jump is absolute or relative? - Stack Overflow](https://stackoverflow.com/questions/31544052/how-can-i-tell-if-jump-is-absolute-or-relative)  
[assembly - What is register %eiz? - Stack Overflow](https://stackoverflow.com/questions/2553517/what-is-register-eiz)
 
