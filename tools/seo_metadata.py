"""Canonical identity and connected Schema.org metadata shared by all site builders."""
import html,json
from pathlib import Path
IDENTITY=json.loads((Path(__file__).resolve().parents[1]/'content/site_identity.json').read_text())
BASE=IDENTITY['base_url'];PERSON=BASE+'#mina-markos';WEBSITE=BASE+'#website';BLOG=BASE+'blog.html#blog'
def graph(title,description,path,kind,category=None,published=None,modified=None):
    url=BASE+path
    nodes=[{'@type':'Person','@id':PERSON,'name':IDENTITY['name'],'alternateName':IDENTITY['alternate_names'],'jobTitle':IDENTITY['job_title'],'description':IDENTITY['description'],'url':BASE,'image':BASE+IDENTITY['image'],'sameAs':IDENTITY['same_as'],'knowsAbout':IDENTITY['topics']},
           {'@type':'WebSite','@id':WEBSITE,'url':BASE,'name':'Mina Adel Markos — Data Engineering & AI Architecture','publisher':{'@id':PERSON},'inLanguage':'en'}]
    node={'@type':kind,'@id':url+('#article' if kind=='BlogPosting' else '#profile-page' if kind=='ProfilePage' else '#blog' if kind=='Blog' else '#page'),'url':url,'name':title,'description':description,'inLanguage':'en','isPartOf':{'@id':BLOG if kind=='BlogPosting' else WEBSITE}}
    if kind=='ProfilePage':node['mainEntity']={'@id':PERSON}
    if kind=='Blog':node['author']={'@id':PERSON}
    if kind=='BlogPosting':
        node.update(headline=title,author={'@id':PERSON},publisher={'@id':PERSON},mainEntityOfPage=url,image=BASE+IDENTITY['image'],articleSection=category,datePublished=published,dateModified=modified or published)
        nodes.append({'@type':'Blog','@id':BLOG,'url':BASE+'blog.html','name':IDENTITY['blog_title'],'author':{'@id':PERSON},'isPartOf':{'@id':WEBSITE}})
    nodes.append(node)
    if path:
        crumbs=[('Portfolio',BASE)]
        if kind=='BlogPosting':crumbs.append(('Engineering Blog',BASE+'blog.html'))
        crumbs.append(('Engineering Blog' if kind=='Blog' else 'CV' if path=='cv.html' else title,url))
        nodes.append({'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':link}for i,(name,link)in enumerate(crumbs)]})
    return {'@context':'https://schema.org','@graph':nodes}

def metadata(title,description,path,kind='WebPage',category=None,published=None,modified=None):
    e=html.escape;url=BASE+path;image=BASE+IDENTITY['image']
    result=f'''<title>{e(title)}</title>
<meta name="description" content="{e(description,quote=True)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'article' if kind=='BlogPosting' else 'profile' if kind=='ProfilePage' else 'website'}">
<meta property="og:site_name" content="Mina Adel Markos">
<meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{image}"><meta property="og:image:alt" content="Mina Adel Markos, Senior Data Engineer">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title,quote=True)}"><meta name="twitter:description" content="{e(description,quote=True)}"><meta name="twitter:image" content="{image}"><meta name="twitter:image:alt" content="Mina Adel Markos, Senior Data Engineer">
'''
    if kind=='BlogPosting':result+=f'<meta property="article:published_time" content="{published}"><meta property="article:modified_time" content="{modified or published}">\n'
    return result+'<script type="application/ld+json">'+json.dumps(graph(title,description,path,kind,category,published,modified),ensure_ascii=False).replace('</','<\\/')+'</script>\n'
