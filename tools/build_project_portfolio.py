#!/usr/bin/env python3
"""Generate source-backed cards, case studies, inventory and ranking. No remote writes."""
from pathlib import Path
import sys,json,re,html,subprocess
from urllib.parse import quote
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'content'))
from project_cases import PROJECTS
from seo_metadata import metadata,BASE
E=html.escape
image_dimensions=json.loads((R/'content/image-dimensions.json').read_text())
def size_attrs(source):
 d=image_dimensions[source];return f'width="{d["width"]}" height="{d["height"]}"'
original=json.loads((R/'content/project-original-links.json').read_text())
revisions=json.loads((R/'content/project-review-revisions.json').read_text())
weights=[2,1,2,1,1,2,1];criteria=['Enterprise relevance','Architecture complexity','Data engineering depth','AI integration','Business value relevance','Implementation evidence','Documentation quality']
projects=sorted(PROJECTS,key=lambda p:-sum(s*w for s,w in zip(p['scores'],weights)))
(R/'projects').mkdir(exist_ok=True);(R/'docs/project-review').mkdir(parents=True,exist_ok=True)
for rank,p in enumerate(projects,1):
 p['demo_label']='Data portal preview (samples/fixtures)' if p['slug']=='verdatrace' else 'UI preview (synthetic)'
 p['rank']=rank;p['weighted_score']=sum(s*w for s,w in zip(p['scores'],weights));p['original_links']=[]
 for old in original:
  if old['image']==p['image']:p['original_links']=old['links']
 p['commit']=revisions[p['repo']] if p['repo'] else None
 p['repo_url']='https://github.com/MINAADELMARKOS/'+p['repo'] if p['repo'] else None
 if p['slug']=='databricks-sales':
  p['image']='img/portfolio/Databricks_Customer_Sales.png'
  if not (R/p['image']).exists(): (R/p['image']).write_bytes(Path('/workspace/project-review/DataBricks_Customer_Sales_Analysis/Customer_Sales_Dashboard.png').read_bytes())
 def unique_links(links):
  seen=set();return [(u,l) for u,l in links if not(u in seen or seen.add(u))]
 def repo_link(file):return p['repo_url']+'/blob/'+p['commit']+'/'+quote(file,safe='/')
 sections=[('Executive Summary',p['problem']+' '+p['solution']),('Business Context',p['context']),('Engineering Challenges',p['challenges']),('Architecture Decisions',p['decisions']),('Implementation',p['implementation']),('Reliability and Security',p['security']),('Business Value',p['value']),('Future Improvements',p['future'])]
 content=''
 for title,prose in sections:
  id=title.lower().replace(' ','-');content+=f'<section><h2 id="{id}">{title}</h2><p>{E(prose)}</p></section>'
 diagram='<section><h2 id="technical-architecture">Technical Architecture</h2><figure class="project-architecture"><ol>'+''.join('<li>'+E(stage)+'</li>' for stage in p['flow'])+'</ol><figcaption>Source-reviewed flow at the revision below. Optional, simulated and unverified boundaries are labeled; this is not evidence of a production deployment.</figcaption></figure></section>'
 content=content.replace('<section><h2 id="engineering-challenges">',diagram+'<section><h2 id="engineering-challenges">')
 evidence=f'<section><h2 id="evidence">Evidence and validation boundary</h2><p>Status: <strong>{E(p["status"])}</strong>. Reviewed 22 November 2026.</p>'
 if p['repo']:
  evidence+=f'<p>Reviewed repository revision: <a href="{p["repo_url"]}/tree/{p["commit"]}">{p["commit"][:12]}</a>. Code presence is distinct from executed runtime behavior.</p><ul>'+''.join(f'<li><a href="{repo_link(f)}">{E(f)}</a></li>'for f in p['evidence'])+'</ul>'
 else:evidence+='<p>No implementation repository was established from the accessible source. The card does not invent one.</p>'
 evidence+='<p><a href="../docs/project-review/VALIDATION.md">Current local test outcomes and unexecuted checks</a>. CI and test evidence is separated from production readiness; the validation record includes retrieved checks at the reviewed revision.</p>'
 ci_file=R/'docs/project-review/remote-ci.json'
 if ci_file.exists():
  ci=json.loads(ci_file.read_text()).get(p['slug'])
  if isinstance(ci,list):
   evidence+='<p>Remote check runs returned for this revision: '+('none; no CI success is inferred.' if not ci else '')+'</p>'
   if ci:evidence+='<ul>'+''.join(f'<li><a href="{c["html_url"]}">{E(c["name"])}</a>: {E(c["status"])} / {E(c["conclusion"] or "unknown")}</li>' for c in ci)+'</ul>'
 if p['image']:evidence+=f'<figure><img class="case-screenshot" {size_attrs(p["image"])} src="../{E(p["image"],quote=True)}" alt="{E(p["name"],quote=True)} — existing project screenshot" loading="lazy"><figcaption>Existing project artifact; this screenshot is not a new live-execution result.</figcaption></figure>'
 content=content.replace('<section><h2 id="future-improvements">',evidence+'</section><section><h2 id="future-improvements">')
 links=[]
 if p['repo_url']:links.append((p['repo_url'],'GitHub repository'))
 if p['demo']:links.append((p['demo'],p['demo_label']))
 if p['slug']=='investinator':links.append(('https://minaadelmarkos.github.io/Enterprise-DataOps-Incident-Resolution-Copilot/','CV-listed alternate preview (availability unverified)'))
 for link in p['original_links']:
  links.append(('../'+link if not link.startswith('http') else link,'Related explanation' if not link.startswith('http') else 'Original supporting link'))
 linkhtml='<ul>'+''.join(f'<li><a href="{E(url,quote=True)}">{label}</a></li>'for url,label in unique_links(links))+'</ul>'
 toc='<nav class="toc" aria-label="Case study contents"><h2>On this page</h2><ol>'+''.join(f'<li><a href="#{id}">{title}</a></li>'for id,title in re.findall('<h2 id="([^"]+)">(.*?)</h2>',content))+'</ol></nav>'
 page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{metadata(p['name']+' | Engineering Case Study | Mina Markos',p['problem'],'projects/'+p['slug']+'.html','WebPage')}<link rel="stylesheet" href="../css/learning-hub.css"><link rel="stylesheet" href="../css/project-portfolio.css"><link rel="stylesheet" href="../css/design-system.css"><link rel="icon" href="../img/fav-icon.jpg"></head><body class="portfolio-ui"><a class="skip-link" href="#main">Skip to case study</a><header class="hub-nav"><div class="wide"><a class="brand" href="../">MINA ADEL MARKOS <span>/ ENGINEERING PORTFOLIO</span></a><nav aria-label="Primary"><a href="../#portfolio">All projects</a><a href="../blog.html">Engineering Blog</a><a href="../cv.html">CV</a><a href="../#contact">Contact</a></nav></div></header><main class="reading" id="main" tabindex="-1"><article><header class="article-heading"><p class="eyebrow">{E(p['category'])}</p><h1>{E(p['name'])}</h1><p class="standfirst">{E(p['solution'])}</p><p class="project-status">{E(p['status'])}</p><p class="byline">Mina Adel Markos · Source review: 22 November 2026</p><p>{E(p['stack'])}</p>{linkhtml}</header>{toc}{content}</article><aside class="related"><h2>Continue the review</h2><a href="../#portfolio">Explore other engineering projects</a> · <a href="../cv.html">Read the latest CV</a></aside></main><footer class="hub-footer"><div class="wide">Mina Adel Markos · <a href="../#contact">Discuss a data engineering opportunity</a></div></footer></body></html>'''
 (R/'projects'/f'{p["slug"]}.html').write_text(page+'\n')
# Card links preserve every original URL in addition to case studies.
categories=['Enterprise Data Platforms','AI & Intelligent Systems','Cloud Architecture','Data Engineering','Business Intelligence']
filters='<div hidden class="filters portfolio-filter"><ul><li class="active"><button class="project-filter" type="button" data-filter="*" aria-pressed="true">All projects</button></li>'+''.join(f'<li><button class="project-filter" type="button" data-filter=".category-{i}" aria-pressed="false">{E(c)}</button></li>'for i,c in enumerate(categories))+'</ul></div>'
cards=''
for p in projects:
 tags=[categories.index(p['category'])]
 if p['slug']=='verdatrace':tags+=[categories.index('Cloud Architecture')]
 links=[]
 if p['repo_url']:links.append((p['repo_url'],'GitHub'))
 if p['demo']:links.append((p['demo'],p['demo_label']))
 for url in p['original_links']:links.append((url,'Technical explanation' if not url.startswith('http') else 'Original source'))
 links=unique_links(links)
 cards+=f'''<div class="all {' '.join('category-'+str(i)for i in tags)}"><article class="engineering-project"><img {size_attrs(p['image'])} src="{E(p['image'],quote=True)}" alt="{E(p['name'],quote=True)} project preview" loading="lazy" decoding="async"><div class="project-body"><p class="project-category">{E(p['category'])}</p><h3>{E(p['name'])}</h3><p class="project-status">{E(p['status'])}</p><p class="project-problem">{E(p['problem'])}</p><p>{E(p['solution'])}</p><p class="project-stack">{E(p['stack'])}</p><div class="engineering-project-actions"><a class="case-button" href="projects/{p['slug']}.html" data-engagement="project">View Case Study<span class="sr-only">: {E(p['name'])}</span></a><div class="project-evidence-links">{''.join(f'<a href="{E(url,quote=True)}"'+(' target="_blank" rel="noopener noreferrer"'if url.startswith('http') else '')+f'>{label}</a>'for url,label in links)}</div></div></div></article></div>'''
section=f'''<section class="portfolio_area engineering-portfolio" id="portfolio" aria-labelledby="portfolio-heading"><div class="container"><div class="main_title text-left"><p class="executive-eyebrow">PROBLEMS / ARCHITECTURE / EVIDENCE</p><h2 id="portfolio-heading">Engineering projects, explained.</h2><p>Explore the problem, implementation choices, and evidence behind each project. Local demos, reference platforms, and presentation artifacts are labeled explicitly.</p></div><p class="project-contact"><a href="cv.html" data-engagement="cv">Read my latest CV</a> · <a href="#contact" data-engagement="contact">Discuss a data platform challenge</a></p>{filters}<p id="project-filter-status" role="status" aria-live="polite">{len(projects)} projects</p><div class="portfolio-grid engineering-project-grid">{cards}</div></div></section>'''
p=R/'index.html';s=p.read_text();s=re.sub(r'<section class="portfolio_area".*?</section>',lambda m:section,s,count=1,flags=re.S);p.write_text(s)
(R/'content/projects.json').write_text(json.dumps(projects,indent=2,ensure_ascii=False)+'\n')
# Preserve the library and CV sitemap; add each case once.
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
t=ET.parse(R/'sitemap.xml');urls={n.text for n in t.findall('.//{*}loc')}|{BASE+'projects/'+p['slug']+'.html'for p in projects};node=ET.Element('{'+ns+'}urlset')
for url in sorted(urls):ET.SubElement(ET.SubElement(node,'{'+ns+'}url'),'{'+ns+'}loc').text=url
ET.indent(node);ET.ElementTree(node).write(R/'sitemap.xml',encoding='utf-8',xml_declaration=True)
rows=['# Project inventory and prioritization','', 'Source-reviewed public repositories and original portfolio artifacts. Numeric scores are editorial judgments (0–5), not business KPIs or runtime measurements. Weights: enterprise relevance 2, architecture 1, data depth 2, AI 1, business relevance 1, implementation evidence 2, documentation 1. Equal totals retain the reviewed ordering; InvestiNator and VerdaTrace are co-leading by score.','', '| Rank | Project | Weighted score / 50 | '+ ' | '.join(criteria)+' | Status |','|---|---|---|'+'---|'*8]
for p in projects:rows.append('| '+str(p['rank'])+' | '+p['name']+' | '+str(p['weighted_score'])+' | '+' | '.join(map(str,p['scores']))+' | '+p['status']+' |')
rows+=['','All ten existing projects are retained; Databricks SQL analysis is added from the supplied CV and an accessible repository. The CV’s banking-data-platform URL was not accessible; its embedded PDF hyperlink actually points to Banking-Fraud-Detection, so no second banking project was invented. The CV-listed alternate InvestiNator preview URL is preserved on its case study, while the repository-documented preview is used on the card.','']
for p in projects:
 rows+=[f'## {p["name"]}',f'- Business problem: {p["problem"]}',f'- Technical objective: {p["solution"]}',f'- Category / stack: {p["category"]} / {p["stack"]}',f'- Status: {p["status"]}',f'- Repository: {p["repo_url"] or "Not established"}',f'- Revision: {p["commit"] or "Not available"}',f'- Preview: {p["demo"] or "No independently established live application"}',f'- Screenshot: {p["image"]}',f'- Documentation / source: {", ".join(p["evidence"]) or "Original linked document and supplied CV only"}',f'- Architecture: {" → ".join(p["flow"])}','']
(R/'docs/project-review/INVENTORY_AND_RANKING.md').write_text('\n'.join(rows))
print('Built 11 project cards and 11 source-backed case-study pages.')
