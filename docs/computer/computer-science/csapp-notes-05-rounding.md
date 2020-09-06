# 【CS:APP 筆記】數值修約(rounding)

章節：2.3.7  
頁數：P. 105
  
對有號數而言

  - `>>` (右移)：round down，需要加上 $2^n-1$ 才會變成 round toward 0
  - x86\_64 `idiv`：round toward 0
  - C 語言中的 `/`：round toward 0

參考資料：  
[Intel® 64 and IA-32 Architectures Software Developer Manuals](https://software.intel.com/en-us/articles/intel-sdm)
 
