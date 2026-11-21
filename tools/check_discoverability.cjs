const {chromium}=require('playwright');
const Axe=require('@axe-core/playwright').default;
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');const base=process.env.HUB_BASE_URL||'http://127.0.0.1:8014/';
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();const errors=[];const results=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push(r.url());});
 const report=JSON.parse(fs.readFileSync(path.join(root,'docs/seo-discoverability/source-after.json')));
 for(const width of [375,768,1024,1440]){
  await page.setViewportSize({width,height:1000});
  for(const record of report.pages.filter(p=>p.indexable_in_source)){
   const suffix=record.path==='index.html'?'':record.path;
   await page.goto(base+suffix,{waitUntil:'load'});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),suffix+' overflow');
   assert.equal(await page.locator('h1').count(),1);
   const schemas=await page.locator('script[type="application/ld+json"]').allTextContents();schemas.forEach(s=>JSON.parse(s));
   assert(await page.locator('main').isVisible());
  }
  results.push({width,pages:35,noJavaScript:true,noHorizontalOverflow:true,semanticContentVisible:true});
  console.log(width+'px: all 35 pages readable without JavaScript; no horizontal overflow');
 }
 await context.close();
 const active=await browser.newContext();const live=await active.newPage();
 for(const suffix of['','blog.html','projects/investinator.html','insights/kafka-troubleshooting.html']){
  await live.setViewportSize({width:375,height:1000});await live.goto(base+suffix,{waitUntil:'networkidle'});
  const axe=await new Axe({page:live}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
  assert.deepEqual(axe.violations.map(v=>v.id),[],suffix);
  results.push({page:suffix||'/',automatedAccessibilityViolations:axe.violations,passedRules:axe.passes.length});
 }
 // Hold the deferred controller: first paint must already reserve the closed-menu layout.
 const early=await active.newPage();await early.setViewportSize({width:375,height:1000});let release;const gate=new Promise(resolve=>release=resolve);
 await early.route('**/js/homepage.*.js',async route=>{await gate;await route.continue();});
 await early.goto(base,{waitUntil:'commit'});await early.waitForSelector('.navbar-toggler',{state:'visible'});
 assert.equal(await early.locator('#navbarSupportedContent').isVisible(),false);
 const initialTop=await early.locator('#home').evaluate(e=>e.getBoundingClientRect().top);
 release();await early.waitForLoadState('networkidle');
 const readyTop=await early.locator('#home').evaluate(e=>e.getBoundingClientRect().top);
 assert.equal(initialTop,readyTop,'Navigation must not shift the hero when controller loads');
 await early.close();
 await live.goto(base+'insights/kafka-troubleshooting.html');const link=live.locator('a[href="../projects/investinator.html"]');await link.focus();assert(await link.evaluate(e=>document.activeElement===e));await live.keyboard.press('Enter');await live.waitForURL('**/projects/investinator.html');
 await live.locator('a[rel="author"]').focus();await live.keyboard.press('Enter');await live.waitForURL('**/#about');
 assert.deepEqual(errors,[]);await browser.close();
 fs.writeFileSync(path.join(root,'docs/seo-discoverability/browser-checks.json'),JSON.stringify({results,errors,keyboardCaseAndAuthorLinks:true,stableNavigationBeforeController:true},null,2)+'\n');console.log('PASS: sampled Axe checks, keyboard links and zero local script/missing-resource errors');
})().catch(e=>{console.error(e);process.exit(1)});
