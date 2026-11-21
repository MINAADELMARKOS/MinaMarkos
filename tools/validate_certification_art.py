#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import re,json
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'docs/certification-art-manifest.json').read_text())
for item in manifest:
 p=R/'img/testimonials'/item['file'];root=ET.parse(p).getroot();assert root.attrib['viewBox']=='0 0 640 640'
 ids={n.attrib['id']for n in root.iter()if 'id'in n.attrib}
 for id in root.attrib['aria-labelledby'].split():assert id in ids
 for tag in ('title','desc'):assert root.find('{http://www.w3.org/2000/svg}'+tag).text
 for n in root.iter():
  assert n.tag.split('}')[-1]not in ('script','image','foreignObject')
  for k,v in n.attrib.items():
   assert not k.lower().startswith('on')
   assert not ('href'in k and not v.startswith('#'))
   for ref in re.findall(r'url\(#([^)]*)\)',v):assert ref in ids
 assert p.stat().st_size<15000
print('PASS: seven archived SVG assets remain valid; current card integration is covered by check_certificate_logos.cjs')
