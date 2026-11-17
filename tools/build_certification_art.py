#!/usr/bin/env python3
"""Original, fully vector portfolio artwork; never official issuer badges."""
from pathlib import Path
from html import escape as e
import json,re
R=Path(__file__).resolve().parents[1]
DATA=[
('generative-ai-leader-illustration.svg','Google Cloud',['Generative AI','Leader'],'AI & STRATEGY','#3158C7','#7452BA',['AI fundamentals','Cloud AI','Output quality','Responsible AI'],'Understand AI. Lead with Value.','ai'),
('google-cloud-associate-cloud-engineer-custom-evidence.svg','Google Cloud',['Associate Cloud','Engineer'],'CLOUD ENGINEERING','#3158C7','#5368A8',['Cloud setup','Deployment','Operations','Access & security'],'Build. Deploy. Operate. Secure.','cloud'),
('google-business-intelligence-certificate.svg','Google',['Business','Intelligence'],'BUSINESS INTELLIGENCE','#2563A6','#187759',['Data modeling','Analysis','Dashboards','Storytelling'],'From Data to Decisions.','bi'),
('cloudera-certified-data-engineer.svg','Cloudera',['Data Engineer','Professional'],'DATA ENGINEERING','#087F83','#244978',['Distributed data','Pipelines','Transformation','Reliability'],'Engineering Data at Scale.','pipeline'),
('si-architect-certification.svg','Issuer unconfirmed',['SI Architect','Certification'],'ENTERPRISE ARCHITECTURE','#4D49A4','#7650AC',['System design','Integration','Scalability','Trade-offs'],'Design Systems for Business Growth.','architecture'),
('vodafone-data-analytics.svg','Vodafone Business',['Data Analytics','Professional'],'BUSINESS ANALYTICS','#B72D3A','#36465C',['Business analysis','KPI monitoring','Reporting','Decision support'],'Analytics for Business Outcomes.','telecom'),
('cloudera-data-analyst.svg','Cloudera',['Data Analyst','Professional'],'ENTERPRISE ANALYTICS','#087C9D','#127D73',['SQL analytics','Exploration','Aggregation','Insights'],'Enterprise Data. Actionable Insights.','sql')]
def box(x,y,w,h,label='',fill='white'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="currentColor" stroke-width="4"/>'+ (f'<text x="{x+w/2}" y="{y+h/2+10}" text-anchor="middle" font-size="28" font-weight="700" fill="#16253D" stroke="none">{e(label)}</text>' if label else '')
def line(d):return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
def diagram(kind):
 if kind=='ai':
  return line('M100 285L165 255L192 320L125 370L100 285M165 255L125 370M100 285L192 320')+''.join(f'<circle cx="{x}" cy="{y}" r="12" fill="currentColor"/>'for x,y in [(100,285),(165,255),(192,320),(125,370)])+line('M218 315H258M380 315H422')+line('M320 255L366 275V322Q364 350 320 375Q276 350 274 322V275Z')+line('M298 313L315 330L344 293')+box(444,263,110,112)+line('M462 350V327M494 350V305M526 350V283')+''.join(f'<text x="{x}" y="411" text-anchor="middle" font-size="25" fill="#16253D" stroke="none">{label}</text>'for x,label in [(146,'AI'),(320,'TRUST'),(499,'VALUE')])
 if kind=='cloud':
  return line('M244 290H397Q439 286 425 252Q414 231 389 238Q367 203 332 224Q297 203 278 238Q233 231 230 263Q229 281 244 290Z')+line('M320 292V315M155 315H485M155 315V342M320 315V342M485 315V342')+box(90,344,130,65,'Compute')+box(255,344,130,65,'K8s')+box(420,344,130,65,'Storage')
 if kind=='bi':
  return box(108,237,424,180)+box(128,258,105,54,'KPI')+line('M263 365L314 335L361 348L405 301L499 277')+line('M263 383H503M263 383V270')+box(128,330,105,65,'Goal')
 if kind=='pipeline':
  out=line('M109 320H528')
  for x,label in [(65,'IN'),(172,'ETL'),(279,'SQL'),(386,'DB'),(493,'BI')]:out+=box(x,278,82,88,label)
  return out+line('M320 367V390L342 406L375 377')
 if kind=='architecture':
  return ''.join(box(110,y,365,44,label)for y,label in [(231,'Business services'),(286,'Integration'),(341,'Data platform'),(396,'Infrastructure')])+line('M510 267L551 285V352L510 382L486 362M509 303V344')
 if kind=='telecom':
  return line('M138 279V387M108 387L138 340L168 387M115 270Q138 248 161 270M96 252Q138 208 180 252')+'<circle cx="138" cy="282" r="9" fill="currentColor"/>'+line('M187 314H230')+box(246,245,300,163)+line('M272 378H519M275 354L317 322L358 340L406 299L449 309L510 279')+box(268,260,80,40,'KPI')
 return '<ellipse cx="125" cy="267" rx="49" ry="18" fill="white" stroke="currentColor" stroke-width="4"/>'+line('M76 267V356C76 385 174 385 174 356V267M76 313C76 337 174 337 174 313M190 320H229M423 320H460')+box(241,262,170,115,'SQL')+line('M478 369V342M510 369V310M542 369V280')
for filename,issuer,title,category,accent,secondary,themes,message,kind in DATA:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="640" height="640" role="img" aria-labelledby="title desc">
<title id="title">{e(issuer+' — '+' '.join(title))}</title><desc id="desc">Original portfolio illustration of {e(kind)}. Illustrative learning themes: {e(', '.join(themes))}. Not an official badge; examination objectives have not been independently verified.</desc>
<defs><linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{accent}" stop-opacity=".09"/><stop offset="1" stop-color="{secondary}" stop-opacity=".03"/></linearGradient></defs>
<rect x="2" y="2" width="636" height="636" rx="30" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="3"/><rect x="24" y="221" width="592" height="218" rx="20" fill="url(#wash)"/>
<g font-family="Arial, Helvetica, sans-serif"><text x="40" y="51" font-size="22" font-weight="700" letter-spacing="1" fill="{accent}">{e(category)}</text><text x="40" y="93" font-size="29" fill="#526176">{e(issuer)}</text><g fill="#16253D" font-size="45" font-weight="700"><text x="40" y="151">{e(title[0])}</text><text x="40" y="202">{e(title[1])}</text></g><g color="{accent}">{diagram(kind)}</g>
'''
 for i,theme in enumerate(themes):
  x=42+(i%2)*292;y=472+(i//2)*40
  svg+=f'<circle cx="{x}" cy="{y-8}" r="4" fill="{accent}"/><text x="{x+14}" y="{y}" font-size="25" fill="#16253D">{e(theme)}</text>'
 svg+=f'<text x="320" y="554" text-anchor="middle" font-size="24" font-weight="700" fill="{accent}">{e(message)}</text><path d="M40 576H600" stroke="#E2E8F0" stroke-width="2"/><text x="40" y="607" font-size="21" fill="#526176">{e(issuer)}</text><text x="600" y="607" text-anchor="end" font-size="18" fill="#526176">CUSTOM ILLUSTRATION</text></g></svg>\n'
 (R/'img/testimonials'/filename).write_text(svg)
(R/'docs/certification-art-manifest.json').write_text(json.dumps([dict(file=x[0],issuer=x[1],title=' '.join(x[2]),themes=x[6],evidence='Supplied brief and portfolio description; official verification blocked')for x in DATA],indent=2)+'\n')
print('Built seven original 640 × 640 vector illustrations.')
