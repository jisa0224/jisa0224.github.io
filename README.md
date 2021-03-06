# Jisa's Notebook(jisa0224.github.io) 文章原始碼

使用 [MkDocs](https://www.mkdocs.org/) 及 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 主題，架設在 GitHub Pages 上的個人部落格。

MkDocs 使用 [Python-Markdown](https://python-markdown.github.io/) 轉換成 HTML，其提供了許多內建和第三方 [extensions](https://python-markdown.github.io/extensions/) 可供使用，另外還有很常用的 [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)。

## 下載文章原始碼並配置環境

```
git clone https://github.com/jisa0224/jisa0224.github.io
cd jisa0224.github.io
for b in $(git branch -r | grep -v HEAD | grep -v master); do git branch $(basename $b) $b; done
git remote remove origin
git checkout dev
./sitectl.sh init
./sitectl.sh upgrade
```

## sitectl.sh 的其它指令

```
./sitectl.sh upgrade
./sitectl.sh run
./sitectl.sh upload
./sitectl.sh mkdocs --version
```

## 注意事項

如果移動文章原始碼資料夾，必須刪除並重新建立 Python venv，因為它會紀錄建立時的絕對路徑，可以使用 `./sitectl.sh init`

## 發文時的 Markdown 語法細節

1. 文章標題、段落標題與目錄：整個文章必須以 `#` 作為文章標題，之後再用 `##` 及更下階的語法指定段落標題。
   1. 可以用 front matter(YAML Style Meta-Data) 的 `title` 來指定文章標題，但用 `title` 指定的標題不會顯示在整篇文章最前面，只能在導覽列和瀏覽器的標題欄看到。
   2. `#` 指定的標題不會顯示在目錄裡，只有 `##` 及更下階的標題才會。
   3. 如果有 `##` 出現在 `#` 之前，目錄就不會顯示。
   4. 第二個及以後的 `#` 和低階的標題不會顯示在目錄裡。
   5. 如果整篇文章沒有 `#` 的話，就會以 front matter 的 `title` 作為第一個（也是唯一一個）`#` 顯示在整篇文章最前面。
2. 行內 HTML：
   1. 預設無法在行內 HTML 裡使用 Markdown。
   2. 啟用 Python-Markdown 的 [Markdown in HTML](https://python-markdown.github.io/extensions/md_in_html/) extension 可以在行內 HTML 裡使用 Markdown。
   3. 使用時需要在最外層的 HTML tag 加上 `markdown="1"` 屬性(attribute)。
3. 內部文章連結：使用常規 Markdown 語法即可，使用相對檔案位置連結到 `*.md` 檔，MkDocs 會自動轉換成 build 完的位置。
4. 內部圖片連結：`![圖片替代文字](圖片檔案位置 "圖片標題"){: width="圖片寬度" height="圖片高度"}`
   1. 文章專屬的圖片資料夾：建立一個與文章檔案同名（不含副檔名）的資料夾，將圖片放在裡面，使用常規 Markdown 語法，圖片檔案位置指向該資料夾裡，例如：在同一資料夾中有檔案 `test.md`、資料夾 `test` 和圖片 `test/img.png`，則在 test.md 中應使用 `![](test/img.png)` 而不是 `![](img.png)`，MkDocs 會自動轉換。
   2. 啟用 Python-Markdown 的 [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) extension 可以給 Markdown 產生的 HTML 元素加上屬性，例如調整大小。
   3. 設定 `height` 的屬性會被主題的 CSS 蓋掉，所以只要調整 `width` 就好，高度會隨比例縮放。
   4. 啟用自己寫的 `custom_extensions.img2figure` 可以把 Markdown 圖片的 title 屬性變為 HTML figure 的 figcaption。
   5. [caption](https://github.com/flywire/caption) 在 HTML table 內無法使用。
5. 程式碼區塊和 syntax highlighting：
   1. 依照 [Code blocks - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/) 啟用和設定 PyMdown Extensions 中的 [Highlight](https://facelessuser.github.io/pymdown-extensions/extensions/highlight/)。
   2. 如果 `use_pygments: true` 的話，必須額外啟用 [SuperFences](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#superfences)，不然不會有顏色。
6. 數學公式（MathJax）：
   1. 依照 [MathJax - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/mathjax/) 啟用和設定 PyMdown Extensions 中的 [Arithmatex](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/)。
   2. 由於 Arithmatex 轉換區塊公式時，只作用在最外層（即無法在 Markdown 清單或 HTML table 中使用區塊公式），所以另外使用自己寫的 `custom_extensions.arithmatex_generic` extension 來補上沒有處理到的部份。
   3. 行內公式放在兩個 `$` 之間，且 `$` 和公式之間**不得有空格或換行**。
   4. 區塊公式放在兩個 `$$` 之間，`$$` 和公式之間可以有空格或換行。
   5. 文章標題、段落標題和圖片標題裡不能用公式。
7. Mermaid：
   1. SuperFences 提供 Custom Fences 的功能，可以把 Mermaid 的相關區塊轉成 HTML div，再讓 Mermaid 的 Javascript 處理。
   2. 依照[這個說明](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#uml-diagram-example)進行設定。其中 `extension_configs` 的部份加到 mkdocs.yml 的 `markdown_extensions`，`pymdownx.superfences.fence_div_format` 要依照 [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation#names-and-modules) 轉成 Python object；Javascript 就加到 mkdocs.yml 的 `extra_javascript`。
   3. Mermaid 語法參考 [Mermaid 官方網站](http://mermaid-js.github.io/mermaid/)。
   4. 可以使用 Mermaid 官方提供的 [Mermaid Live Editor](https://mermaidjs.github.io/mermaid-live-editor/) 編輯完圖像後再貼到文章裡。
   5. Mermaind 和 [Graphviz](https://www.graphviz.org/) 的語法不同。
   6. [mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin) 無法使用，因為它會在 SuperFences 之後才執行，此時該區塊已經被轉換成程式碼區塊了。
8. 在 Markdown 清單中如果要使用多個段落（中間空一行），第二段及之後的段落必須要空 4 格，空行則無所謂。
9. [MkDocs Awesome Pages Plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)：  
   可以精細調整每個資料夾的顯示名稱，和文章的排列方式，在 `docs` 的每一個資料夾和子資料夾中有設定檔 `.pages`。

## TBD

- 太大的數學公式 div 把它縮小(eg: convolution)
- 調整 table css(加 border，內外都要。會變太大)
- 圖片太小，點下去變大？
- 最後輸出的 HTML beautify
- 超連結改成 target="_blank"

## 附錄：從零開始建構網站

```
mkdir jisa0224.github.io
cd jisa0224.github.io
```

複製 `.gitignore` 和 `README.md` 到資料夾底下，並在 GitHub 建立一個新的 repository `jisa0224.github.io`

`master` 分支存放 mkdocs build 完的網頁，`dev` 分支存放網站原始碼

```
git init
git commit --allow-empty -m "an empty commit for branching master and dev"
git checkout -b dev
```

複製 `sitectl.sh` 到資料夾底下

```
chmod +x sitectl.sh
./sitectl.sh init
./sitectl.sh upgrade
./sitectl.sh mkdocs new .
```

## 參考資料

[基于mkdocs-material搭建个人静态博客(含支持的markdown语法)](https://cyent.github.io/markdown-with-mkdocs-material/)
[git - Cloning a repository without making it the origin remote - Stack Overflow](https://stackoverflow.com/questions/2248994/cloning-a-repository-without-making-it-the-origin-remote/2249757#2249757)