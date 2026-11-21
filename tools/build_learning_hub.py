#!/usr/bin/env python3
"""Build static learning pages using only Python's standard library.
Run from any directory. No client-side content fetch or JavaScript dependency.
"""
import html, json, re, sys, math
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
from hub_articles import ARTICLES
BASE='https://minaadelmarkos.github.io/MinaMarkos/'
DATE='2026-11-17'
LINK_UPDATE='2026-11-22'
discovery_links=json.loads((ROOT/'content/discovery-links.json').read_text())
project_names={p['slug']:p['name'] for p in json.loads((ROOT/'content/projects.json').read_text())}
def has_case_link(slug):return any(any(a['slug']==slug for a in articles) for articles in discovery_links.values())
E=html.escape
CATEGORIES=['Apache Kafka','Apache Spark & PySpark','Distributed Systems','Data Engineering','Cloud Architecture','AI Engineering','Engineering Leadership','Engineering Perspectives']
legacy=json.loads((ROOT/'content/existing_articles.json').read_text())
NEW=list(ARTICLES)
for slug,category in [('gcp-data-quality-governance','Cloud Architecture'),('cloudera-hdfs-object-storage-migration-readiness','Data Engineering'),('from-ai-demo-to-production','AI Engineering')]:
 item=legacy[slug]
 NEW.append(dict(slug=slug,title=item['title'],summary=item['summary'],category=category,sections=[],diagram=['Source / use case','Architecture and operating controls','Validated business outcome'],question='What evidence would change this architectural decision?',code=None))
# Tag overlap explicitly without inventing duplicate category pages.
for a in NEW:
 a['tags']=[a['category']]
 if a['slug']=='reliability-business-capability': a['tags'].append('Engineering Leadership')
 if a['slug']=='data-quality-foundation-for-ai': a['tags']+=['AI Engineering','Data Engineering']
 if a['slug']=='ai-dataops-investigation-copilot': a['tags']+=['AI Engineering','Distributed Systems']
 if a['slug']=='spark-cloudera-cloud': a['tags'].append('Apache Spark & PySpark')
 if a['slug'] in ('kafka-architecture','kafka-reliability'): a['tags'].append('Distributed Systems')
 if a['slug'] in ('the-cost-of-untrusted-data','architecture-cost-risk'): a['tags'].append('Engineering Leadership')

def text(s): return html.unescape(re.sub('<[^>]+>',' ',s))
def paragraphs(s): return ''.join('<p>'+E(p.strip())+'</p>' for p in s.strip().split('\n\n'))
def anchor(s): return re.sub('[^a-z0-9]+','-',text(s).lower()).strip('-')
def highlight(s,lang):
 # Tokenize original text once; never run regex over already escaped markup.
 pattern=r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|#[^\n]*|\b(?:public|final|class|static|void|new|try|catch|finally|throw|throws|if|else|for|while|return|import|from|as|def|with|assert|in|not|True|False|None|package|int|long|short|true|false)\b|\b\d+(?:\.\d+)?\b)'
 parts=[];pos=0
 for m in re.finditer(pattern,s):
  parts.append(E(s[pos:m.start()]));t=m.group();kind='comment' if t.startswith(('//','#')) else 'string' if t.startswith(('"',"'")) else 'number' if t[0].isdigit() else 'keyword'
  parts.append(f'<span class="syntax-{kind}">{E(t)}</span>');pos=m.end()
 return ''.join(parts)+E(s[pos:])
def codeblock(s,lang,label):
 return f'<div class="code-sample"><div class="code-toolbar"><span>{E(label)} · {E(lang)}</span><button type="button" class="copy-code" hidden aria-label="Copy {E(label,quote=True)}">Copy code</button></div><pre tabindex="0" aria-label="{E(label,quote=True)}"><code class="language-{lang}">{highlight(s,lang)}</code></pre><p class="copy-status" role="status" aria-live="polite"></p></div>'

def head(title,description,path,article=None):
 from seo_metadata import metadata,IDENTITY
 prefix='../' if article else ''
 actual_title=(title+' | Mina Markos') if article else IDENTITY['blog_title']
 actual_description=description if article else IDENTITY['blog_description']
 return '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+metadata(actual_title,actual_description,path,'BlogPosting' if article else 'Blog',article['category'] if article else None,DATE if article else None,LINK_UPDATE if article and has_case_link(article['slug']) else None)+f'<link rel="icon" href="{prefix}img/fav-icon.jpg"><link rel="stylesheet" href="{prefix}css/learning-hub.css"><link rel="stylesheet" href="{prefix}css/design-system.css"><script defer src="{prefix}js/learning-hub.js"></script><script defer src="{prefix}js/engagement.js"></script>'

def nav(article=False):
 p='../' if article else ''
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="hub-nav"><div class="wide"><a class="brand" href="{p}blog.html">MINA MARKOS <span>/ ENGINEERING</span></a><nav aria-label="Primary"><a href="{p if p else './'}">Portfolio</a><a href="{p}blog.html">Learning hub</a><a href="{p}cv.html" data-engagement="cv">CV</a><a href="{p if p else './'}#portfolio">Projects</a><a href="https://github.com/MINAADELMARKOS">GitHub</a></nav></div></header>'''

def footer(): return '<footer class="hub-footer"><div class="wide"><p>Engineering notes by Mina Adel Markos. Original examples use synthetic data; no confidential infrastructure details.</p><a href="https://github.com/MINAADELMARKOS">GitHub</a> · <a href="https://www.linkedin.com/in/mina-markos-343b8b171/">LinkedIn</a> · <a href="../blog.html">Engineering Blog</a> · <a href="../cv.html" data-engagement="cv">CV</a> · <a href="../#contact" data-engagement="contact">Contact Mina</a></div></footer>'

def diagram(lines):
 return '<figure class="technical-diagram"><ol>'+''.join('<li>'+E(x)+'</li>' for x in lines)+'</ol><figcaption>Conceptual flow — boundaries and responsibilities, not a deployment topology.</figcaption></figure>'

KAFKA_SETUP='''# From a fresh Kafka 4.1.1 binary distribution directory:
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties
bin/kafka-server-start.sh config/server.properties
# Keep that terminal running. From the portfolio checkout in another terminal:
cd examples/kafka
mvn -B package dependency:copy-dependencies
java -cp 'target/classes:target/dependency/*' dev.minamarkos.OrdersLab'''
KAFKA_OUTPUT='''Created orders-lab-<unique-id> with 2 partitions (local RF=1)
Produced order-0 partition=<assigned partition> offset=<offset>
... six produced and six processed records ...
PASS: 6 unique orders, stable key routing, committed next offsets'''
OPS='''# Read-only commands; replace TOPIC and GROUP with your actual identifiers.
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic TOPIC
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group GROUP
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions
bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status
# OS evidence (run on the relevant host, with appropriate access):
df -h
# No output from --under-replicated-partitions is expected for a healthy lab.
# RF=1 cannot demonstrate replica failover or production redundancy.'''
SPARK_SETUP='''# From the portfolio checkout, with Python 3.10–3.12 and JDK 17:
python3 -m venv .venv
.venv/bin/python -m pip install pyspark==3.5.7
SPARK_LOCAL_IP=127.0.0.1 .venv/bin/python examples/spark/orders_lab.py'''

def lab_content(a):
 kind=a.get('code')
 if not kind: return ''
 if kind=='kafka':
  return ('<h2 id="lab">Run the Java lab</h2><p class="validation">Executed locally: Kafka broker/client 4.1.1, JDK 17.0.17, Maven 3.9.11. Assertions cover clean-path delivery, key routing, and committed offsets. No crash, transaction, or production failover test is claimed.</p>'+codeblock(KAFKA_SETUP,'bash','Start and run')+codeblock((ROOT/'examples/kafka/src/main/java/dev/minamarkos/OrdersLab.java').read_text(),'java','Complete Java source')+codeblock(KAFKA_OUTPUT,'text','Expected output shape')+'<p>All six records must be processed before the 45-second deadline. Topic identifiers and partition assignments vary. A failed assertion exits nonzero; inspect the error rather than accepting a partial run.</p>')
 if kind=='kafka-ops':
  return '<h2 id="lab">Read-only diagnostic commands</h2>'+codeblock(OPS,'bash','Kafka 4.1.1 diagnostics')+'<p>Healthy output has a valid topic leader and the expected ISR members. Group lag should converge to zero after the producer stops and processing completes. The controller command should identify a leader and voters. Check the validation record for the commands executed locally; production failure scenarios remain unexecuted.</p>'
 return '<h2 id="lab">Run the PySpark lab</h2><p class="validation">Executed locally: PySpark 3.5.7, Python 3.12, JDK 17.0.17, local[2]. No distributed-cluster or performance benchmark claim.</p>'+codeblock(SPARK_SETUP,'bash','Install and run')+codeblock((ROOT/'examples/spark/orders_lab.py').read_text(),'python','Complete PySpark source')+codeblock('PASS: Finance=200, Networks=120; plan includes pruning, pushdown, broadcast, shuffle','text','Expected result')+'<p>If Java cannot start, check JAVA_HOME and use a full JDK 17. If hostname binding fails locally, keep SPARK_LOCAL_IP=127.0.0.1. If a plan marker changes, confirm the Spark version and inspect the formatted plan before weakening the assertion.</p>'

for a in NEW:
 slug=a['slug'];body=''
 for heading,prose in a['sections']:
  body+=f'<section aria-labelledby="{anchor(heading)}"><h2 id="{anchor(heading)}">{E(heading)}</h2>{paragraphs(prose)}</section>'
 if slug in legacy:
  old=legacy[slug]['body']
  # Keep earlier useful prose on its original URL, with deterministic non-conflicting anchors.
  old=re.sub(r'<h2(?:[^>]*)>(.*?)</h2>',lambda m:f'<h2 id="context-{anchor(m[1])}">{m[1]}</h2>',old,flags=re.S)
  body+='<section class="project-context"><h2 id="earlier-context">Earlier project and operating notes</h2>'+old+'</section>'
 illustration=''
 if slug.startswith('kafka-'):
  illustration='<figure class="system-illustration" tabindex="0" aria-label="System diagram; scroll horizontally on small screens"><img src="../img/engineering/kafka-planes.svg" width="760" height="460" alt="Kafka data replication between partition leader and followers, separate from the KRaft controller quorum"><figcaption>Data and metadata responsibilities are distinct. This RF=3 illustration differs from the single-node lab. On small screens, scroll the diagram horizontally.</figcaption></figure>'
 elif slug.startswith(('spark-','why-spark')):
  illustration='<figure class="system-illustration" tabindex="0" aria-label="System diagram; scroll horizontally on small screens"><img src="../img/engineering/spark-execution.svg" width="760" height="470" alt="Spark driver planning, pruned Parquet scan, broadcast dimension join, and shuffle into final team totals"><figcaption>Follow the lab through its scan, join, exchange, and result boundaries. On small screens, scroll the diagram horizontally.</figcaption></figure>'
 body=illustration+diagram(a['diagram'])+body+lab_content(a)
 repo='Apache-Kafka' if slug.startswith('kafka-') else 'Apache_Spark' if slug.startswith(('spark-','why-spark')) else 'MinaMarkos'
 source=BASE.replace('https://minaadelmarkos.github.io/','https://github.com/MINAADELMARKOS/')+'tree/main/examples/'+('kafka' if repo=='Apache-Kafka' else 'spark') if repo!='MinaMarkos' else 'https://github.com/MINAADELMARKOS/MinaMarkos'
 official='https://kafka.apache.org/41/' if repo=='Apache-Kafka' else 'https://spark.apache.org/docs/3.5.7/' if repo=='Apache_Spark' else 'https://sre.google/sre-book/table-of-contents/'
 body+=f'''<section><h2 id="resources">Source, versions, and further reading</h2><ul><li><a href="{source}">Companion source and run instructions on GitHub</a></li><li><a href="https://github.com/MINAADELMARKOS/{repo}">Original {E(repo)} repository</a></li><li><a href="{official}">Official {'Kafka 4.1' if repo=='Apache-Kafka' else 'Spark 3.5.7' if repo=='Apache_Spark' else 'Site Reliability Engineering'} documentation</a></li><li><a href="https://github.com/MINAADELMARKOS/MinaMarkos/blob/main/examples/VALIDATION.md">What was tested and what remains unexecuted</a></li></ul></section>'''
 if repo=='Apache_Spark': body+='<p><a href="https://github.com/MINAADELMARKOS/Pyspark-_Tutorials">Earlier PySpark notebooks</a> provide additional exercises. The new self-contained lab avoids local dataset-path assumptions in those notebooks.</p>'
 case_links=[(slug,project_names[slug]) for slug,articles in discovery_links.items() if any(item['slug']==a['slug'] for item in articles)]
 if case_links:body+='<section><h2 id="applied-case-studies">Applied engineering case studies</h2><p>Review the implementation, evidence, and documented limitations of these related portfolio projects.</p><ul>'+''.join(f'<li><a href="../projects/{slug}.html">{E(name)}</a></li>' for slug,name in case_links)+'</ul></section>'
 toc='<nav class="toc" aria-label="Table of contents"><h2>On this page</h2><ol>'+''.join(f'<li><a href="#{id}">{title}</a></li>' for id,title in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body))+'</ol></nav>'
 minutes=max(2,math.ceil(len(text(body).split())/200));a['minutes']=minutes
 related=[b for b in NEW if b!=a and (set(b['tags'])&set(a['tags']))][:3]
 if len(related)<2: related+=[b for b in NEW if b!=a and b not in related][:2-len(related)]
 rel='<aside class="related" aria-labelledby="related"><h2 id="related">Continue learning</h2><ul>'+''.join(f'<li><a href="{b["slug"]}.html">{E(b["title"])}</a></li>' for b in related)+'</ul><p><a href="../blog.html">← All articles and learning paths</a></p></aside>'
 page=f'''<!doctype html><html lang="en"><head>{head(a['title'],a['summary'],'insights/'+slug+'.html',a)}</head><body class="portfolio-ui">{nav(True)}<main id="main" class="reading" tabindex="-1"><article><header class="article-heading"><a class="eyebrow" href="../blog.html?category={html.escape(__import__('urllib.parse',fromlist=['quote']).quote(a['category']))}">{E(a['category'])}</a><h1>{E(a['title'])}</h1><p class="standfirst">{E(a['summary'])}</p><p class="byline">By <a rel="author" href="../#about">Mina Adel Markos</a> · Published <time datetime="{DATE}">17 November 2026</time>{' · Updated <time datetime="2026-11-22">22 November 2026</time>' if has_case_link(slug) else ' · Updated 17 November 2026' if slug in legacy else ''} · {minutes} min read</p></header>{toc}{body}<section class="discussion"><h2>Discuss the engineering decision</h2><p>{E(a['question'])}</p></section></article>{rel}</main>{footer()}</body></html>'''
 (ROOT/'insights'/f'{slug}.html').write_text(page+'\n')

# Search is progressive enhancement; every article and category anchor works without JS.
cards=''
for a in NEW:
 tags=' | '.join(a['tags'])
 cards+=f'''<article class="article-card" data-categories="{E(tags,quote=True)}" data-search="{E(a['title']+' '+a['summary']+' '+tags,quote=True)}"><span class="eyebrow">{E(a['category'])}</span><h3><a href="insights/{a['slug']}.html">{E(a['title'])}</a></h3><p>{E(a['summary'])}</p><p class="card-meta">17 Nov 2026 · {a['minutes']} min read</p><a class="read-link" href="insights/{a['slug']}.html">Read article <span aria-hidden="true">↗</span></a></article>'''
categorynav='<nav class="category-nav" aria-label="Article categories">'+''.join(f'<a href="#category-{anchor(c)}">{E(c)}</a>' for c in CATEGORIES)+'</nav>'
categorysections=''.join(f'<section class="category-index" id="category-{anchor(c)}"><h3>{E(c)}</h3><ul>'+''.join(f'<li><a href="insights/{a["slug"]}.html">{E(a["title"])}</a></li>' for a in NEW if c in a['tags'])+'</ul></section>' for c in CATEGORIES)
paths=''
for label,prefix in [('Apache Kafka','kafka-'),('Apache Spark & PySpark','spark-')]:
 items=[a for a in NEW if a['slug'].startswith(prefix) or (prefix=='spark-' and a['slug']=='why-spark-exists')]
 paths+=f'<article class="learning-path"><span class="eyebrow">6-part learning path</span><h3>{E(label)}</h3><ol>'+''.join(f'<li><a href="insights/{a["slug"]}.html">{E(a["title"])}</a></li>' for a in items)+'</ol></article>'
blog=f'''<!doctype html><html lang="en"><head>{head('Engineering Blog & Technical Learning Hub','Kafka and Spark tutorials, runnable Java and PySpark labs, and engineering perspectives on reliable data, AI, architecture, cost, and risk.','blog.html')}</head><body class="portfolio-ui">{nav()}<main id="main" tabindex="-1"><section class="hub-hero"><div class="wide"><p class="eyebrow">FIELD NOTES / TUTORIALS / ENGINEERING DECISIONS</p><h1>Understand the system.<br>Make the trade-off.</h1><p class="standfirst">Kafka, Spark, data platforms, and AI—explained through failure boundaries, executable examples, and the business decisions they support.</p><p class="byline">By <a rel="author" href="./#about">Mina Adel Markos</a> · Data Engineering &amp; AI Architecture</p><a class="hub-button" href="#learning-paths">Choose a learning path ↓</a></div></section><div class="wide hub-content"><section id="learning-paths"><div class="section-heading"><p class="eyebrow">01 / BUILD YOUR MENTAL MODEL</p><h2>Start with a system. Follow it into production.</h2><p>Each series moves from the problem and architecture to a runnable lab, failure reasoning, and operational trade-offs.</p></div><div class="path-grid">{paths}</div></section><section aria-labelledby="library-title" id="library"><div class="section-heading"><p class="eyebrow">02 / THE ENGINEERING LIBRARY</p><h2 id="library-title">Read by the problem you’re solving.</h2></div>{categorynav}<form class="library-controls" role="search" hidden><div><label for="article-search">Search articles</label><input id="article-search" type="search" placeholder="Try: offsets, shuffle, cost…"></div><div><label for="category-filter">Filter category</label><select id="category-filter"><option value="">All categories</option>{''.join(f'<option>{E(c)}</option>' for c in CATEGORIES)}</select></div><button type="reset">Reset</button></form><p id="result-count" role="status" aria-live="polite">{len(NEW)} articles</p><div class="article-grid">{cards}</div><p id="no-results" hidden>No matching articles. Try another term or reset the filters.</p></section><section class="category-directory"><h2>Browse the full topic index</h2>{categorysections}</section><aside class="editorial-note"><h2>How these notes are validated</h2><p>The Java and PySpark labs use synthetic data and executable assertions. Local tests do not establish production throughput, failover, or cloud compatibility. Articles label unexecuted exercises and link to the validation record. Existing project notes remain on their original URLs.</p><a href="https://github.com/MINAADELMARKOS/MinaMarkos/blob/main/examples/VALIDATION.md">Read the validation record</a></aside></div></main>{footer().replace('../blog.html','blog.html').replace('../cv.html','cv.html').replace('../#contact','./#contact')}</body></html>'''
(ROOT/'blog.html').write_text(blog+'\n')
# Preserve every previous sitemap URL and add the library and all articles once.
ns='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',ns)
oldtree=ET.parse(ROOT/'sitemap.xml'); urls={x.text for x in oldtree.findall('.//{'+ns+'}loc')}
urls|={BASE,BASE+'blog.html',BASE+'cv.html'}|{BASE+'insights/'+a['slug']+'.html' for a in NEW}
tree=ET.Element('{'+ns+'}urlset')
for url in sorted(urls):
 node=ET.SubElement(tree,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url
ET.indent(tree);ET.ElementTree(tree).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
(ROOT/'content/article-index.json').write_text(json.dumps([{k:a[k] for k in ('slug','title','summary','category','tags','minutes')} for a in NEW],indent=2,ensure_ascii=False)+'\n')
# Draft distribution materials are files only; no external posting.
for a in NEW:
 if a['category'] not in ('Apache Kafka','Apache Spark & PySpark','Distributed Systems','Cloud Architecture') or a['slug'] in legacy: continue
 source='https://github.com/MINAADELMARKOS/MinaMarkos/tree/main/examples/'+('kafka' if a['slug'].startswith('kafka-') else 'spark')
 heading,prose=a['sections'][0]; last_heading,last=a['sections'][-1]
 lead=prose.split('\n\n')[0]; takeaway=last.split('\n\n')[-1]
 draft=f'''# Distribution draft — {a['title']}

Prepared for manual review. Not posted or sent. No production-experience claims are implied.

## LinkedIn educational post

{a['summary']}

{lead}

A useful review question: {a['question']}

{takeaway}

Full article: {BASE}insights/{a['slug']}.html
Code and validation scope: {source}

## Short video script (approximately 60–90 seconds)

**0–10s / Hook:** {a['question']}

**10–35s / System model:** {lead}

**35–60s / Visual:** Draw these boundaries: {' → '.join(a['diagram'])}. Explain which operation crosses each boundary and which evidence would show it failed.

**60–90s / Decision:** {a['summary']} Read the full article and check the linked validation scope before applying a configuration to production.

On-screen article: {BASE}insights/{a['slug']}.html
On-screen code: {source}

## Discussion questions

1. {a['question']}
2. For “{heading}”, what measurement in your workload would disprove the initial assumption?
3. For “{last_heading}”, which recovery or cost constraint would change your decision?
'''
 (ROOT/'distribution'/f'{a["slug"]}.md').write_text(draft)
print(f'Built {len(NEW)} articles, blog, sitemap, topic index, and 12 tutorial distribution drafts.')
