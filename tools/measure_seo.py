#!/usr/bin/env python3
"""Run repeatable mobile Lighthouse lab checks; keep raw reports outside checkout."""
import argparse,json,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--phase',required=True);p.add_argument('--base-url',default='http://127.0.0.1:8003/');p.add_argument('--lighthouse',required=True);p.add_argument('--chrome',default='/usr/bin/chromium');p.add_argument('--raw-dir',default='/workspace/tooling/seo-results');p.add_argument('--paths',nargs='*',default=['','blog.html','insights/spark-performance.html']);a=p.parse_args()
rawdir=Path(a.raw_dir);rawdir.mkdir(parents=True,exist_ok=True)
reports=[]
for path in a.paths:
    name=(path or 'home').replace('/','-').replace('.html','');raw=rawdir/f'{a.phase}-{name}.json'
    cmd=['node',a.lighthouse,a.base_url+path,'--chrome-path='+a.chrome,'--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage','--only-categories=performance,accessibility,best-practices,seo','--output=json','--output-path='+str(raw),'--quiet','--max-wait-for-load=20000']
    subprocess.run(cmd,check=True)
    r=json.loads(raw.read_text());aud=r['audits']
    assert not r.get('runtimeError'),r.get('runtimeError')
    metrics={k:{'value':aud[k].get('numericValue'),'display':aud[k].get('displayValue'),'unit':aud[k].get('numericUnit')} for k in ['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index','interactive'] if k in aud}
    failed=[{'id':k,'title':v.get('title'),'score':v.get('score'),'description':v.get('description'),'display':v.get('displayValue'),'details':v.get('details')} for k,v in aud.items() if v.get('score') is not None and v['score']<1 and v.get('scoreDisplayMode') not in ('manual','informative','notApplicable')]
    reports.append({'path':path or '/','requestedUrl':r['requestedUrl'],'finalDisplayedUrl':r.get('finalDisplayedUrl'),'fetchTime':r['fetchTime'],'lighthouseVersion':r['lighthouseVersion'],'environment':r.get('environment'),'configSettings':r['configSettings'],'scores':{k:round(v['score']*100) for k,v in r['categories'].items()},'metrics':metrics,'failed_audits':failed,'runWarnings':r.get('runWarnings',[]),'raw_report':str(raw)})
    print(name, reports[-1]['scores'], metrics,flush=True)
output=ROOT/'docs/measurements'/f'lighthouse-{a.phase}.json';output.write_text(json.dumps(reports,indent=2)+'\n')
