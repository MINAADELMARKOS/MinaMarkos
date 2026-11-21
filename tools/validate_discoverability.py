#!/usr/bin/env python3
"""Verify canonical coverage, connected identity, evidence and discovery links locally."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
from audit_seo import crawl,Document,ROOT,BASE
from seo_metadata import IDENTITY,PERSON,WEBSITE
report=crawl();pages=[p for p in report['pages'] if p['indexable_in_source']]
assert len(pages)==35
assert not report['broken_local_references'],report['broken_local_references']
assert report['verification_token_present']
before=json.loads((ROOT/'docs/seo-discoverability/source-before.json').read_text())
assert before['verification_token_sha256']==report['verification_token_sha256']
for key in ['title','description']:
 counts=Counter(p[key] for p in pages)
 assert all(value and count==1 for value,count in counts.items()),(key,counts)
expected=set()
projects={p['slug']:p for p in json.loads((ROOT/'content/projects.json').read_text())}
dimensions=json.loads((ROOT/'content/image-dimensions.json').read_text())
for p in pages:
 path=p['path'];url=BASE+('' if path=='index.html' else path);expected.add(url)
 assert p['canonical']==[url] and p['h1_count']==1,path
 assert not p['schema_parse_errors'] and not p['images_without_dimensions'],path
 d=Document(ROOT/path);nodes=[n for s in d.schemas for n in s.get('@graph',[s])]
 person=next(n for n in nodes if n.get('@id')==PERSON)
 assert person['name']==IDENTITY['name'] and person['sameAs']==IDENTITY['same_as'],path
 assert person['jobTitle']==IDENTITY['job_title'],path
 assert any(n.get('@id')==WEBSITE and n['publisher']=={'@id':PERSON} for n in nodes),path
 assert d.meta['og:url']==url and d.meta['og:title']==p['title'],path
 assert d.meta['twitter:title']==p['title'] and d.meta['twitter:description']==p['description'],path
 image=unquote(urlsplit(d.meta['og:image']).path.removeprefix('/MinaMarkos/'))
 assert (ROOT/image).is_file(),(path,image)
 assert int(d.meta['og:image:width'])==dimensions[image]['width'],path
 assert int(d.meta['og:image:height'])==dimensions[image]['height'],path
 # No skipped heading levels (heading changes are a usability issue, not a ranking promise).
 previous=0
 for heading in p['headings']:
  assert heading['level']<=previous+1,(path,heading)
  previous=heading['level']
 if path.startswith('projects/'):
  project=projects[Path(path).stem]
  work=next(n for n in nodes if n['@type']=='CreativeWork')
  page=next(n for n in nodes if n['@type']=='WebPage')
  assert page['mainEntity']=={'@id':work['@id']}
  assert work['author']=={'@id':PERSON} and work['about']['description']==project['status']
  assert d.meta['og:image']==work['image'] and d.meta['twitter:card']=='summary_large_image'
  if project.get('commit'):assert work['citation']==project['repo_url']+'/tree/'+project['commit']
  else:assert 'citation' not in work
  assert 'rel="author" href="../#about"' in (ROOT/path).read_text()
 if path.startswith('insights/'):
  article=next(n for n in nodes if n['@type']=='BlogPosting')
  assert article['author']=={'@id':PERSON} and article['datePublished']=='2026-11-17'
  assert article['dateModified']>=article['datePublished']
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==len(set(urls)) and set(urls)==expected
mapping=json.loads((ROOT/'content/discovery-links.json').read_text())
for project,articles in mapping.items():
 for article in articles:
  assert f'../insights/{article["slug"]}.html' in Document(ROOT/f'projects/{project}.html').links
  assert f'../projects/{project}.html' in Document(ROOT/f'insights/{article["slug"]}.html').links
print('PASS: 35 unique canonical pages, exact sitemap coverage, identity/schema/evidence, image sizes, heading levels, reciprocal discovery links and preserved verification token')
