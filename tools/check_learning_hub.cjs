const { chromium }=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',args:['--no-sandbox']});
 const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});
 const page=await context.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://**/*',r=>r.abort());
 const base=process.env.HUB_BASE_URL || 'http://127.0.0.1:8002/';
 for(const width of [375,768,1024,1440]){
  await page.setViewportSize({width,height:1000});
  await page.goto(base+'blog.html',{waitUntil:'networkidle'});
  assert.equal(await page.locator('.article-card').count(),21);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('#category-filter').selectOption('Apache Kafka');
  assert.equal(await page.locator('.article-card:visible').count(),6);
  await page.locator('#article-search').fill('offset');
  assert((await page.locator('.article-card:visible').count())>0);
  await page.locator('#article-search').fill('zzznomatchzz');
  assert(await page.locator('#no-results').isVisible());
  await page.locator('button[type=reset]').click();
  await page.waitForFunction(()=>!document.querySelectorAll('.article-card[hidden]').length);
  await page.screenshot({path:`/tmp/hub-${width}.png`,fullPage:false});
  for(const slug of ['kafka-java-producer-consumer','spark-performance','data-quality-foundation-for-ai']){
   await page.goto(base+'insights/'+slug+'.html',{waitUntil:'networkidle'});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${slug} overflows at ${width}`);
   assert.equal(await page.locator('h1').count(),1);
   for(const link of await page.locator('.toc a').all()){
    const hash=await link.getAttribute('href');assert.equal(await page.locator(hash).count(),1);
   }
   if(slug==='spark-performance'){
    await page.locator('.copy-code').first().click();
    await page.waitForFunction(()=>document.querySelector('.copy-code').textContent==='Copied');
    assert((await page.evaluate(()=>navigator.clipboard.readText())).includes('python3 -m venv'));
   }
  }
  await page.goto(base,{waitUntil:'networkidle'});
  const nav=page.locator('.menu_nav a[href="blog.html"]');
  if(width>=992){
    const bounds=await page.locator('.menu_nav > li').evaluateAll(items=>items.map(item=>{const r=item.getBoundingClientRect();return {y:r.y,right:r.right};}));
    assert(bounds.every(r=>Math.abs(r.y-bounds[0].y)<1&&r.right<=width),'Desktop navigation must fit one row');
  }
  if(width<992)await page.locator('.navbar-toggler').click();
  await nav.waitFor({state:'visible'});
  await nav.click();await page.waitForURL('**/blog.html');
  console.log(`${width}px: homepage navigation, filters/reset/empty state, reading layout, TOC and clipboard passed`);
 }
 // All generated pages must load without missing local dependencies.
 for(const a of JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'../content/article-index.json'),'utf8'))){
  const response=await page.goto(base+'insights/'+a.slug+'.html');assert.equal(response.status(),200);
 }
 assert.deepEqual(errors,[]);
 const nojs=await browser.newContext({javaScriptEnabled:false});const plain=await nojs.newPage();
 await plain.goto(base+'blog.html');assert.equal(await plain.locator('.article-card:visible').count(),21);
 await plain.getByRole('link',{name:'Apache Kafka',exact:true}).click();
 assert(plain.url().endsWith('#category-apache-kafka'));
 await nojs.close();await browser.close();
 console.log('PASS: all 21 articles served; no page errors; no-JavaScript library and category navigation work');
})().catch(e=>{console.error(e);process.exit(1)});
