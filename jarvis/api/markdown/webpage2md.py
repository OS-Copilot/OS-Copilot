import re
import requests
import html2text as ht
from urllib.parse import urljoin
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError(
        'Webpage requires extra dependencies. Install with `pip install --upgrade "embedchain[dataloaders]"`'
    ) from None

class WebPage2MDTool:
    _session = requests.Session()
    def get_web_md(self, url):
        """Load data from a web page using a shared requests session."""
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        try:
            response = self._session.get(url,headers=headers, timeout=30)
            response.raise_for_status()
            data = response.content
            content = self._get_clean_content(data, url)
            text_maker = ht.HTML2Text()
            md_text = text_maker.handle(content)
        except Exception:
            md_text = "error loading markdown of current webpage"
        return md_text
    def _get_clean_content(self, html, url) -> str:
        soup = BeautifulSoup(html, "html.parser")
        original_size = len(str(soup.get_text()))

        tags_to_exclude = [
            "nav",
            "aside",
            "form",
            "header",
            "noscript",
            "svg",
            "canvas",
            "footer",
            "script",
            "style",
        ]
        for tag in soup(tags_to_exclude):
            tag.decompose()

        ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
        for id in ids_to_exclude:
            tags = soup.find_all(id=id)
            for tag in tags:
                tag.decompose()

        classes_to_exclude = [
            "elementor-location-header",
            "navbar-header",
            "nav",
            "header-sidebar-wrapper",
            "blog-sidebar-wrapper",
            "related-posts",
        ]
        for class_name in classes_to_exclude:
            tags = soup.find_all(class_=class_name)
            for tag in tags:
                tag.decompose()
        # 将相对路径转绝对路径
        # 查找所有带有href属性的<a>标签
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            link['href'] = absolute_url

        # 查找所有带有src属性的<img>标签
        for img in soup.find_all('img', src=True):
            absolute_url = urljoin(url, img['src'])
            img['src'] = absolute_url
        content = str(soup)
        
        return content

    @classmethod
    def close_session(cls):
        cls._session.close()
