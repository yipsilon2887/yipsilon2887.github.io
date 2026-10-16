"""Check all generated page links, anchors and multilingual output."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parent
DIST = ROOT

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.lang = None
        self.h1 = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        self.links.extend(attrs[k] for k in ('href', 'src') if k in attrs)

pages = {}
for path in DIST.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    assert '\ufffd' not in text, f'Invalid text: {path}'
    pages[path.resolve()] = Page(text)

checked = 0
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target = target / 'index.html'
        assert target.exists(), f'Broken link: {path.name} -> {link}'
        if url.fragment:
            assert url.fragment in pages[target].ids, f'Broken anchor: {link}'
        checked += 1
    if path != (DIST/'index.html').resolve():
        assert page.h1 == 1
        assert page.lang in ('ja', 'zh-CN', 'en')

data = json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
resume = json.loads((ROOT/'resume.json').read_text(encoding='utf-8'))
for language in ('ja', 'zh', 'en'):
    assert len(resume[language]['entries']) == 4
    assert len(resume[language]['skillRows']) == 5
    page_text = (DIST/language/'cv'/'index.html').read_text(encoding='utf-8')
    for excluded in ['B.Econ', 'Bachelor', 'Yitao_Ye_Resume', '\u5b66\u58eb', '\u672c\u79d1', '\u6e0b\u8c37', '\u6da9\u8c37']:
        assert excluded not in page_text, f'Privacy exclusion found: {excluded}'
assert not list(DIST.rglob('*.pdf')), 'Application PDFs must remain local'
assert all(len(d['projects']) == 3 and len(d['jobs']) == 2 for d in data.values())
assert all(d['name'].strip() for d in data.values())
assert data['ja']['name'] == data['zh']['name'] == '\u53f6\u6bc5\u9676'
assert data['en']['name'] == 'Yitao Ye'
assert all(d['nickname'].strip() for d in data.values())
print(f'PASS: {len(pages)} pages, {checked} local links/anchors, 3 languages, configured display names and valid UTF-8.')
