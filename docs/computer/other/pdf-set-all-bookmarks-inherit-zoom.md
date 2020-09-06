# 將 pdf 的所有書籤一次改為承襲縮放

pdf 的書籤縮放率可以選擇「符合頁面（Fit page）」、「實際大小（Actual size）」、「符合寬度（Fit width）」、「符合可見（Fit visible）」與「承襲縮放（Inherit zoom）」，使用 Adobe Acrobat 就可以對每一個書籤進行調整。

但如果要一次將全部的書籤改為「承襲縮放」，可以使用 [JPdfBookmarks](https://sourceforge.net/projects/jpdfbookmarks/) 將書籤匯出修改後再匯入儲存。

1. 啟動 JPdfBookmarks 並開啟 pdf 檔

2. Tools > Dump 匯出書籤

   也可以使用 `./jpdfbookmarks_cli <pdf檔名>.pdf --dump --out bookmarks.txt`

3. 編輯匯出的書籤檔

   每一行都是一個書籤項目，在最後面的就是縮放率和其參數，JPdfBookmarks 裡出現的縮放率有：FitNative, FitWidth, FitContentWidth, FitHeight, FitContentHeight, FitPage, FitContent, FitRect, TopLeftZoom 九種，分別有不同的參數，其中比較常見的是

   ```
   FitPage
   FitWidth,[top value]
   TopLeftZoom,[top value],[left value],[zoom value]
   ```

   `TopLeftZoom,[top value],[left value],0.0` 就是「承襲縮放」，所以應該像這樣修改

   ```
   FitPage               ->  TopLeftZoom,0,0,0.0
   FitWidth,[top value]  ->  TopLeftZoom,[top value],0,0.0
   ```

4. Tools > Load 匯入書籤後儲存即可

   也可以使用 `./jpdfbookmarks_cli <pdf檔名>.pdf --apply bookmarks.txt --out <新的pdf檔名>.pdf`

參考資料：  
[Inherit Zoom setting for all bookmarks (Court requirements for filing electronic documents) – Share your feedback on Acrobat DC](https://acrobat.uservoice.com/forums/590923-acrobat-for-windows-and-mac/suggestions/18918343-inherit-zoom-setting-for-all-bookmarks-court-requ)  
[jpdfbookmarks/FitType.java at master · SemanticBeeng/jpdfbookmarks](https://github.com/SemanticBeeng/jpdfbookmarks/blob/master/jpdfbookmarks_core/src/it/flavianopetrocchi/jpdfbookmarks/FitType.java)