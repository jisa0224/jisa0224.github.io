r"""custom Python-Markdown extension: img2figure

複製一份"原本的 img"，再將"原本的 img"清空作為 figure，最後把"複製的 img"放進去。

之所以用這種迂迴的方式，而不是先找到 img 的 parent 元素，建立 figure 元素後把 img 移進去，
是因為若配合 Python-Markdown 的 md_in_html extension 使用會產生問題。

md_in_html 處理巢狀 HTML 時，只處理最外層的 HTML tag，所以

``` python
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree

class DebugTreeProcessor(Treeprocessor):
    def printElement(self, elem):
        print(elem)
        print('    tag:', elem.tag)
        print('    attrib:', elem.attrib)
        print('    text:', repr(elem.text))
        print('    tail:', repr(elem.tail))
        print('    subelements:', list(iter(elem)))
    def run(self, root):
        for elem in root.iter():
            self.printElement(elem)
        print()

class DebugExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(DebugTreeProcessor(), 'debug', 5)

print(markdown.markdown('<table markdown="1"><tr><td>![alt](img.png "title")</td></tr></table>', 
                        extensions=['md_in_html', DebugExtension()]))
```

輸出為

```
<Element 'div' at 0x7f56794582c0>
    tag: div
    attrib: {}
    text: '\n'
    tail: '\n'
    subelements: [<Element 'table' at 0x7f567901a5e0>]
<Element 'table' at 0x7f567901a5e0>
    tag: table
    attrib: {}
    text: '\n'
    tail: '\n'
    subelements: [<Element 'p' at 0x7f567901a630>]
<Element 'p' at 0x7f567901a630>
    tag: p
    attrib: {}
    text: '\x02wzxhzdk:0\x03\x02wzxhzdk:1\x03'
    tail: '\n'
    subelements: [<Element 'img' at 0x7f567901a770>]
<Element 'img' at 0x7f567901a770>
    tag: img
    attrib: {'src': 'img.png', 'title': 'title', 'alt': 'alt'}
    text: None
    tail: '\x02wzxhzdk:2\x03\x02wzxhzdk:3\x03'
    subelements: []

<table>
<p><tr><td><img alt="alt" src="img.png" title="title" /></td></tr></p>
</table>
```

可以發現 `<tr>` 和 `<td>` 並不是 `<table>` 的子元素，所以 `<p>` 才會加在它們之前，
且 `<tr><td>` 是 `<p>` 的 text，`</tr></td>` 是 `<img>` 的 tail。

如果用前面提到的方式，就會轉換成：

```
<table>
<p><tr><td><figure><img alt="alt" src="img.png" title="title" /></td></tr><figcaption>title</figcaption></figure></p>
</table>
```

而導致錯誤。

參考資料：
<https://python-markdown.github.io/extensions/api/>
<https://effbot.org/zone/element-index.htm>
<https://github.com/flywire/caption>
"""

from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
from copy import deepcopy


class Img2FigureTreeprocessor(Treeprocessor):
    def run(self, root):
        # selects all "img" elements in the tree that has a "title" attribute.
        for elem in root.findall(".//img[@title]"):
            # 複製一份 img
            img = deepcopy(elem)
            img.tail = None   # 在 etree.dump 得到的字串中，tail 會位在整個元素後面，所以原本 elem 的 tail 還是留在 elem

            # 把原本的 img 清空，但留下 tail
            elem.tag = ""
            elem.attrib.clear()
            elem.text = ""
            for child in elem:
                elem.remove(child)

            # 建立 HTML figure 及 figcaption 元素，然後把複製的 img 放進去
            figure = elem    # 新的 figure 元素就是原本的 img 元素（已被清空）
            figure.tag = "figure"
            figcaption = etree.Element("figcaption")
            figcaption.text = img.get("title")
            figure.append(img)
            figure.append(figcaption)


class Img2FigureExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(Img2FigureTreeprocessor(), 'img2figure', priority=0)    # priority 越低越後執行


def makeExtension(**kwargs):
    return Img2FigureExtension(**kwargs)
