#!/usr/bin/env python3
"""TLS-verified public HTTP crawl. --compare also requires exact deployed bytes."""
import argparse,hashlib,json,re,subprocess,tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote,urljoin,urlsplit,unquote
from audit_seo import crawl,ROOT,BASE,Document
p=argparse.ArgumentParser();p.add_argument('--compare',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
files=set()
for page in crawl()['pages']:
 if not page['indexable_in_source']:continue
 files.add(page['path']);d=Document(ROOT/page['path']);text=(ROOT/page['path']).read_text()
 refs=[i['src'] for i in d.images]+d.scripts+[d.meta['og:image']]
 refs+=re.findall(r'<link\b[^>]*href="([^"]+)"[^>]*>',text)
 for ref in refs:
  url=urljoin(BASE+('' if page['path']=='index.html' else page['path']),ref)
  if url.startswith(BASE):
   path=unquote(urlsplit(url).path.removeprefix('/MinaMarkos/'))
   if path and (ROOT/path).is_file():files.add(path)
files|={'sitemap.xml','robots.txt','assets/cv/Mina_Adel_Markos_Senior_Data_Engineer.pdf','elements.html','single-blog.html'}
def fetch(item):
 path,url=item
 with tempfile.TemporaryDirectory() as tmp:
  body=Path(tmp)/'body';headers=Path(tmp)/'headers'
  r=subprocess.run(['curl','--silent','--show-error','--location','--max-time','40','--retry','1','--dump-header',str(headers),'--output',str(body),'--write-out','%{http_code}\n%{url_effective}\n%{content_type}',url],capture_output=True,text=True)
  bits=r.stdout.splitlines();data=body.read_bytes() if body.exists() else b''
  row={'path':path,'url':url,'status':int(bits[0]) if bits and bits[0].isdigit() else None,'effective_url':bits[1] if len(bits)>1 else None,'content_type':bits[2] if len(bits)>2 else None,'sha256':hashlib.sha256(data).hexdigest(),'curl_exit':r.returncode}
  if r.stderr:row['error']=r.stderr.strip()
  row['x_robots_tag']=re.findall(r'^x-robots-tag:\s*(.*)',headers.read_text(errors='replace'),flags=re.M|re.I) if headers.exists() else []
  if path and (ROOT/path).is_file():
   row['matches_source']=data==(ROOT/path).read_bytes()
   if path.endswith('.html') and row['status']==200:
    saved=Path(tmp)/'page.html';saved.write_bytes(data);d=Document(saved)
    row.update(canonical=d.canonical,robots=d.meta.get('robots'),title=d.title)
  return row
items=[(f,BASE+('' if f=='index.html' else quote(f,safe='/'))) for f in sorted(files)]
items.append(('index.html',BASE+'index.html')) # Explicit index alias must consolidate to the root canonical.
items.append((None,'https://minaadelmarkos.github.io/robots.txt'))
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,items))
fail=[r for r in rows if r['path'] and (r['status']!=200 or r['curl_exit'] or (a.compare and not r.get('matches_source')))]
result={'scope':'Public HTTPS responses; not search index or ranking data','exact_source_comparison_required':a.compare,'resource_count':len(rows)-1,'failures':len(fail),'responses':rows}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
print(f"Fetched {len(rows)-1} site resources; {len(fail)} failures; origin robots HTTP {rows[-1]['status']}")
if fail:print(json.dumps(fail,indent=2));raise SystemExit(1)
