#!/usr/bin/env python3
"""Source crawl of public HTML. No search rankings or HTTP indexing inference."""
import argparse,json,re,hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
BASE='https://minaadelmarkos.github.io/MinaMarkos/'
class Document(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True);self.path=path;self.meta={};self.canonical=[];self.ids=[];self.headings=[];self.links=[];self.images=[];self.scripts=[];self.schemas=[];self.title='';self.capture=None;self.json=False;self.jsontext='';self.errors=[];self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='title':self.capture='title'
        if re.fullmatch('h[1-6]',tag):self.headings.append({'level':int(tag[1]),'text':''});self.capture='heading'
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if tag=='img':self.images.append(a)
        if tag=='script' and a.get('src'):self.scripts.append(a['src'])
        if tag=='script' and a.get('type')=='application/ld+json':self.json=True;self.jsontext=''
    def handle_data(self,data):
        if self.capture=='title':self.title+=data
        if self.capture=='heading':self.headings[-1]['text']+=data
        if self.json:self.jsontext+=data
    def handle_endtag(self,tag):
        if tag=='title' or re.fullmatch('h[1-6]',tag):self.capture=None
        if tag=='script' and self.json:
            try:self.schemas.append(json.loads(self.jsontext))
            except ValueError as e:self.errors.append(str(e))
            self.json=False

def crawl():
    paths=[ROOT/'index.html',ROOT/'blog.html',*sorted((ROOT/'insights').glob('*.html'))]
    paths += [p for p in [ROOT/'cv.html',ROOT/'elements.html',ROOT/'single-blog.html'] if p.exists()]
    docs={p:Document(p) for p in paths};rows=[];broken=[]
    for path,d in docs.items():
        for ref in d.links+[i.get('src','') for i in d.images]:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            if not u.path and not u.fragment:continue
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            if target.is_dir():target/='index.html'
            if not target.is_relative_to(ROOT) or not target.exists():broken.append({'page':str(path.relative_to(ROOT)),'link':ref,'reason':'missing local file'});continue
            if u.fragment and target.suffix=='.html':
                td=docs.get(target) or Document(target)
                if unquote(u.fragment) not in td.ids:broken.append({'page':str(path.relative_to(ROOT)),'link':ref,'reason':'missing fragment'})
        rows.append({'path':str(path.relative_to(ROOT)),'indexable_in_source':'noindex' not in d.meta.get('robots',''),'title':d.title,'description':d.meta.get('description'),'canonical':d.canonical,'h1_count':sum(h['level']==1 for h in d.headings),'headings':d.headings,'image_count':len(d.images),'empty_alt_count':sum(not i.get('alt') for i in d.images),'images_without_dimensions':sum(not(i.get('width')and i.get('height')) for i in d.images),'script_count':len(d.scripts),'schema_types':[n.get('@type') for s in d.schemas for n in s.get('@graph',[s])],'schema_parse_errors':d.errors})
    token=docs[ROOT/'index.html'].meta.get('google-site-verification','')
    return {'scope':'Local source inspection, not Google/Bing index status','base_url':BASE,'pages':rows,'broken_local_references':broken,'verification_token_sha256':hashlib.sha256(token.encode()).hexdigest(),'verification_token_present':bool(token)}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();report=crawl();out=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if args.output:Path(args.output).write_text(out)
    else:print(out)
