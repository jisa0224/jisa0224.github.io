r"""custom Python-Markdown extension: arithmatex_generic

由於 PyMdown Extensions 中的 Arithmatex

1. 不處理在 Markdown 清單或 raw HTML 中的區塊公式（即使已啟用 md_in_html）
2. 即使已啟用 md_in_html，raw HTML 中的行內公式有時會失效

因此另外寫了這個 extension 來補上沒有處理到的部份。

由於我在啟用 Arithmatex 時，指定要用 `generic` 輸出模式，所以此 extension 也必須配合。

- `$f(x)$` 進行**行內公式**轉換後的結果為 `<span class="arithmatex">\(f(x)\)</span>`
- `$$f(x)$$` 進行**區塊公式**轉換後的結果為 `<div class="arithmatex">\[f(x)\]</div>`
"""


from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
import markdown.util as util
from bs4 import BeautifulSoup, NavigableString
import re


class ArithmatexGenericPostprocessor(Postprocessor):
    def unescape(self, text: str) -> str:
        r"""`\\` 會在 postprocessor 之前就被 escape 成 `\`，這裡要 unescape 它，不然數學公式中的換行會失效。
        
        Python-Markdown 會用 markdown.inlinepatterns.EscapeInlineProcessor 進行 escape 然後留下特殊記號，
        然後用 markdown.postprocessors.UnescapePostprocessor(priority = 10) 進行 unescape。

        如果在 UnescapePostprocessor 之後才處理 `\`，無法得知它是 escape 過的還是原本就這樣，
        所以要在它之前執行此函式，即 ArithmatexGenericPostprocessor 的 priority 要大於 10。
        """
        BACKSLASH_PATTERN = "{}{}{}".format(util.STX, ord('\\'), util.ETX)
        return re.sub(BACKSLASH_PATTERN, BACKSLASH_PATTERN * 2, text)

    def process_block(self, text: str) -> list:
        processed_elements = []
        # 在 Python 的 regular expression 裡，`*?` 代表 non-greedy(minimal) match
        # ，`re.DOTALL` 讓 `.` 可以 match 包含換行在內的所有字元。
        splits = re.split(r'\$\$([^\$].*?)\$\$', text, flags=re.DOTALL)
        if len(splits) % 2 == 1:
            # re.split 會回傳 [non-match, match, non-match, match, non-match, ...]，即奇數個子字串，
            # 雖然應該一定成立，但這裡還是加上判斷，如果不符合代表有錯誤，忽略不處理。
            processed_elements.append(NavigableString(splits[0]))
            for i in range(1, len(splits), 2):    # 如果只回傳的 list 中只有一個 str，代表完全沒有 match，for 不執行。
                div = BeautifulSoup("", "html.parser").new_tag("div")
                div["class"] = "arithmatex"
                div.string = r"\[" + self.unescape(splits[i]) + r"\]"
                processed_elements.append(div)
                processed_elements.append(NavigableString(splits[i+1]))
        return processed_elements

    def process_inline(self, text: str) -> list:
        processed_elements = []
        # 在 Python 的 regular expression 裡，`*?` 代表 non-greedy(minimal) match
        # ，`re.DOTALL` 讓 `.` 可以 match 包含換行在內的所有字元。
        splits = re.split(r'\$([^\$].*?)\$', text, flags=re.DOTALL)
        if len(splits) % 2 == 1:
            # re.split 會回傳 [non-match, match, non-match, match, non-match, ...]，即奇數個子字串，
            # 雖然應該一定成立，但這裡還是加上判斷，如果不符合代表有錯誤，忽略不處理。
            processed_elements.append(NavigableString(splits[0]))
            for i in range(1, len(splits), 2):    # 如果只回傳的 list 中只有一個 str，代表完全沒有 match，for 不執行。
                span = BeautifulSoup("", "html.parser").new_tag("span")
                span["class"] = "arithmatex"
                span.string = r"\(" + self.unescape(splits[i]) + r"\)"
                processed_elements.append(span)
                processed_elements.append(NavigableString(splits[i+1]))
        return processed_elements

    def process(self, elem):
        if not hasattr(elem, 'contents'):    # HTML tag 裡的字串
            # 處理 block
            processed_block_only = self.process_block(elem.string)

            # 處理 inline
            processed_block_and_inline = []
            for processed_block_elem in processed_block_only:
                if not hasattr(processed_block_elem, 'contents'):    # HTML tag 裡的字串
                    processed_block_and_inline.extend(self.process_inline(processed_block_elem.string))
                else:                                                # HTML div，因為已經被 process_block 了
                    processed_block_and_inline.append(processed_block_elem)

            # 取代原本的 elem
            for processed_element in processed_block_and_inline:
                elem.insert_before(processed_element)
            elem.replace_with(NavigableString(""))
        else:                                # HTML tag
            if elem.name not in ['pre', 'span', 'code']:
                for child in elem.contents.copy():    # 如果不複製一份的話，會因為 self.process 新增元素而導致無窮迴圈
                    self.process(child)

    def run(self, text):
        html_tree = BeautifulSoup(text, 'html.parser')
        self.process(html_tree)
        return str(html_tree)


class ArithmatexGenericExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(ArithmatexGenericPostprocessor(md), 'arithmatex_generic', priority=15)    # priority 越低越後執行


def makeExtension(**kwargs):
    return ArithmatexGenericExtension(**kwargs)
