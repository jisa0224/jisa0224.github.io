# 【CS:APP 筆記】x86_64 旗標暫存器與大小判斷

章節：3.6.2  
頁數：P. 203

執行完 `cmp a, b` (假設 a、b 是暫存器或記憶體的內容)之後

CPU 會根據 `a - b` 的結果設定 `ZF`、`SF`、`OF`、`CF` 以及其它這裡用不到的旗標暫存器

<table>
    <tbody>
        <tr>
            <th style="text-align: center; vertical-align: middle;">旗標</th>
            <th style="text-align: center; vertical-align: middle;">設定</th>
            <th style="text-align: center; vertical-align: middle;"><strong>無號數</strong>運算的意義</th>
            <th style="text-align: center; vertical-align: middle;"><strong>有號數</strong>運算的意義</th>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">ZF</td>
            <td>任何運算其結果為 0 時，旗標值設定為 1，否則旗標值設定為 0。</td>
            <td>運算結果為 0</td>
            <td>運算結果為 0</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">SF</td>
            <td>除乘除以外之任何運算，運算結果的最高位元。</td>
            <td>無意義</td>
            <td>運算結果為負數</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">OF</td>
            <td>兩運算子最高位元相同，但與運算結果最高位元不同時設為 1。</td>
            <td>無意義</td>
            <td>正/負溢位</td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">CF</td>
            <td>加法：兩數相加*時發生溢位。<br />
            減法：兩數相減**時發生借位，即被減數小於欲減數。<br />
            左移：將最高位元移到 CF。<br />
            右移：將最低位元移到 CF。</td>
            <td>加法：溢位<br />
            減法：運算結果為負數，無法表示(因為是無號數)</td>
            <td>無意義</td>
        </tr>
    </tbody>
</table>

\*兩數相加：記得無號數和有號數的相加在位元層面上完全相同，例如： 1111<sub>2</sub> + 1111<sub>2</sub> = <span style="color: #ff0000;">1</span>1110<sub>2</sub> ，如果解讀成無號數 15<sub>10</sub> + 15<sub>10</sub> = 14<sub>10</sub> 就會溢位，但如果解讀成有號數 -1<sub>10</sub> + -1<sub>10</sub> = -2<sub>10</sub> 就不會溢位。  
\*\*兩數相減：因為不清楚減法是怎麼做的，所以我不確定實際上是怎麼做的，只知道是借位。

<table>
    <tbody>
        <tr>
            <th style="text-align: center; vertical-align: middle;">無號數</th>
            <th style="text-align: center; vertical-align: middle;">有號數</th>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">
                <table>
                    <tbody>
                        <tr>
                            <th style="text-align: center; vertical-align: middle;"> </th>
                            <th style="text-align: center; vertical-align: middle;">正常</th>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a &gt; b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &gt; 0</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a = b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b = 0</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a &lt; b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &lt; 0</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">CF</td>
                        </tr>
                    </tbody>
                </table>
            </td>
            <td style="text-align: center; vertical-align: middle;">
                <table>
                    <tbody>
                        <tr>
                            <th style="text-align: center; vertical-align: middle;"> </th>
                            <th style="text-align: center; vertical-align: middle;">正常</th>
                            <th style="text-align: center; vertical-align: middle;">溢位</th>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a &gt; b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &gt; 0</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &lt; 0</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;">OF SF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a = b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b = 0</td>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2"> </td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;" rowspan="2">a &lt; b</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &lt; 0</td>
                            <td style="text-align: center; vertical-align: middle;">a - b &gt; 0</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">SF</td>
                            <td style="text-align: center; vertical-align: middle;">OF</td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td style="text-align: center; vertical-align: middle;">
                <table>
                    <tbody>
                        <tr>
                            <th style="text-align: center; vertical-align: middle;">大小</th>
                            <th style="text-align: center; vertical-align: middle;">名稱</th>
                            <th style="text-align: center; vertical-align: middle;">別名</th>
                            <th style="text-align: center; vertical-align: middle;">旗標</th>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">=</td>
                            <td style="text-align: center; vertical-align: middle;">e</td>
                            <td style="text-align: center; vertical-align: middle;">z</td>
                            <td style="text-align: center; vertical-align: middle;">ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">!=</td>
                            <td style="text-align: center; vertical-align: middle;">ne</td>
                            <td style="text-align: center; vertical-align: middle;">nz</td>
                            <td style="text-align: center; vertical-align: middle;">~ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&gt;</td>
                            <td style="text-align: center; vertical-align: middle;">a</td>
                            <td style="text-align: center; vertical-align: middle;">nbe</td>
                            <td style="text-align: center; vertical-align: middle;">~CF &amp; ~ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&gt;=</td>
                            <td style="text-align: center; vertical-align: middle;">ae</td>
                            <td style="text-align: center; vertical-align: middle;">nb</td>
                            <td style="text-align: center; vertical-align: middle;">~CF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&lt;</td>
                            <td style="text-align: center; vertical-align: middle;">b</td>
                            <td style="text-align: center; vertical-align: middle;">nae</td>
                            <td style="text-align: center; vertical-align: middle;">CF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&lt;=</td>
                            <td style="text-align: center; vertical-align: middle;">be</td>
                            <td style="text-align: center; vertical-align: middle;">na</td>
                            <td style="text-align: center; vertical-align: middle;">CF | ZF</td>
                        </tr>
                    </tbody>
                </table>
            </td>
            <td style="text-align: center; vertical-align: middle;">
                <table>
                    <tbody>
                        <tr>
                            <th style="text-align: center; vertical-align: middle;">大小</th>
                            <th style="text-align: center; vertical-align: middle;">名稱</th>
                            <th style="text-align: center; vertical-align: middle;">別名</th>
                            <th style="text-align: center; vertical-align: middle;">旗標</th>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">=</td>
                            <td style="text-align: center; vertical-align: middle;">e</td>
                            <td style="text-align: center; vertical-align: middle;">z</td>
                            <td style="text-align: center; vertical-align: middle;">ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">!=</td>
                            <td style="text-align: center; vertical-align: middle;">ne</td>
                            <td style="text-align: center; vertical-align: middle;">nz</td>
                            <td style="text-align: center; vertical-align: middle;">~ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&lt; 0</td>
                            <td style="text-align: center; vertical-align: middle;">s</td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;">SF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">! (&lt; 0)</td>
                            <td style="text-align: center; vertical-align: middle;">ns</td>
                            <td style="text-align: center; vertical-align: middle;"> </td>
                            <td style="text-align: center; vertical-align: middle;">~SF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&gt;</td>
                            <td style="text-align: center; vertical-align: middle;">g</td>
                            <td style="text-align: center; vertical-align: middle;">nle</td>
                            <td style="text-align: center; vertical-align: middle;">~(SF ^ OF) &amp; ~ZF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&gt;=</td>
                            <td style="text-align: center; vertical-align: middle;">ge</td>
                            <td style="text-align: center; vertical-align: middle;">nl</td>
                            <td style="text-align: center; vertical-align: middle;">~(SF ^ OF)</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&lt;</td>
                            <td style="text-align: center; vertical-align: middle;">l</td>
                            <td style="text-align: center; vertical-align: middle;">nge</td>
                            <td style="text-align: center; vertical-align: middle;">SF ^ OF</td>
                        </tr>
                        <tr>
                            <td style="text-align: center; vertical-align: middle;">&lt;=</td>
                            <td style="text-align: center; vertical-align: middle;">le</td>
                            <td style="text-align: center; vertical-align: middle;">ng</td>
                            <td style="text-align: center; vertical-align: middle;">(SF ^ OF) | ZF</td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table>

註：e 指 equal，n 指 not，z 指 zero，s 指 signed，a 指 above，b 指 below，g 指 greater，l 指 less。

參考資料：  
[6.1 旗標暫存器](http://slvs.tc.edu.tw/~baochyi/teacher/assembly/c0601.htm)  
[關於 Carry Flag 的笨問題 / 組合語言 / 程式設計俱樂部](http://www.programmer-club.com.tw/ShowSameTitleN/assembly/4593.html)  
[Zero flag - Wikipedia](https://en.wikipedia.org/wiki/Zero_flag)  
[Negative flag - Wikipedia](https://en.wikipedia.org/wiki/Negative_flag)  
[Overflow flag - Wikipedia](https://en.wikipedia.org/wiki/Overflow_flag)  
[Carry flag - Wikipedia](https://en.wikipedia.org/wiki/Carry_flag)
 
