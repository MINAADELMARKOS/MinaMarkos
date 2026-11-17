#!/usr/bin/env python3
"""Validate generated article metadata, internal links/fragments, and preserved prose."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET
import json, re, sys, html
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.metas={};self.canon=[];self.h1=0;self.title='';self.intitle=False;self.ld=[];self.inld=False;self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.intitle=True
        if tag=='meta':self.metas[a.get('name',a.get('property',''))]=a.get('content')
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
        if tag in ('link','script','img'):
            ref=a.get('src') or (a.get('href') if a.get('rel') in ('stylesheet','icon') else None)
            if ref:self.links.append(ref)
        if tag=='script' and a.get('type')=='application/ld+json':self.inld=True
    def handle_endtag(self,tag):
        if tag=='title':self.intitle=False
        if tag=='script':self.inld=False
    def handle_data(self,data):
        if self.intitle:self.title+=data
        if self.inld:self.ld.append(json.loads(data))
paths=[ROOT/'blog.html',*sorted((ROOT/'insights').glob('*.html'))]
parsed={p:Page(p) for p in paths}; titles=[]; base='https://minaadelmarkos.github.io/MinaMarkos/'
for path,page in parsed.items():
    assert page.h1==1,(path,'H1 count',page.h1)
    assert len(page.ids)==len(set(page.ids)),(path,'duplicate IDs')
    assert page.canon==[base+str(path.relative_to(ROOT))],(path,'canonical')
    assert page.metas.get('robots')=='index,follow'
    for key in ('description','og:title','og:description','og:url','og:image','twitter:card','twitter:description'):
        assert page.metas.get(key),(path,key)
    assert page.title not in titles,('duplicate title',path);titles.append(page.title)
    assert any(x.get('@type') in ('Blog','BlogPosting') for x in page.ld),(path,'structured data')
    for ref in page.links:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target/= 'index.html'
        assert target.is_relative_to(ROOT),(path,'escaped root',ref)
        assert target.exists(),(path,'broken internal link',ref)
        if u.fragment and target.suffix=='.html':
            other=parsed.get(target) or Page(target)
            assert unquote(u.fragment) in other.ids,(path,'missing fragment',ref)
legacy=json.loads((ROOT/'content/existing_articles.json').read_text())
def norm(s):return ' '.join(html.unescape(re.sub('<[^>]*>',' ',s)).split())
for slug,old in legacy.items():
    current=norm((ROOT/'insights'/f'{slug}.html').read_text())
    for prose in re.findall(r'<p[^>]*>(.*?)</p>',old['body'],re.S):
        assert norm(prose) in current,(slug,'lost existing paragraph',norm(prose)[:70])
urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==len(set(urls))
for p in paths:assert base+str(p.relative_to(ROOT)) in urls,('missing sitemap',p)
assert len(list((ROOT/'distribution').glob('*.md')))==12
print(f'PASS: {len(paths)} pages; metadata, schema, H1, unique IDs/titles, internal links/fragments, sitemap, preserved prose, 12 distribution drafts')
