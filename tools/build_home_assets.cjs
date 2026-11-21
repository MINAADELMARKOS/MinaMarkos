/* npm ci --prefix tools; then node tools/build_home_assets.cjs */
const fs=require('node:fs');const path=require('node:path');const sharp=require('sharp');const CleanCSS=require('clean-css');
const root=path.resolve(__dirname,'..');
(async()=>{
 const cssOnly=process.argv.includes('--css-only');
 const originals=cssOnly?[]:['img/main_official_image.png','img/Picture22.png'];
 fs.mkdirSync(path.join(root,'img/optimized'),{recursive:true});
 for(const input of originals){
  const name=input.includes('main_official')?'mina-adel-markos':'mina-adel-markos-about';
  for(const width of [384,768])await sharp(path.join(root,input)).resize({width,withoutEnlargement:true}).webp({quality:82,effort:6}).toFile(path.join(root,`img/optimized/${name}-${width}.webp`));
 }
 // Keep original stylesheets and legacy templates intact; build a dedicated homepage bundle.
 const files=['css/bootstrap.css','css/font-awesome.min.css','css/style.css','css/home-blog-navigation.css','css/seo-accessibility.css'];
 const styles=files.map(file=>fs.readFileSync(path.join(root,file),'utf8').replace(/@import\s+url\([^;]+\);/g,'')).join('\n');
 const result=new CleanCSS({level:1,rebase:false}).minify(styles);
 if(result.errors.length)throw new Error(result.errors.join('\n'));
 fs.writeFileSync(path.join(root,'css/homepage.min.css'),'/* Built by tools/build_home_assets.cjs; source styles retained. */\n'+result.styles+'\n');
 if(cssOnly){console.log('Rebuilt homepage CSS only.');return;}
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8');const sizes={};
 for(const match of html.matchAll(/<img\b[^>]*src="([^"]+)"[^>]*>/g)){
  const relative=match[1];const m=await sharp(path.join(root,relative)).metadata();sizes[relative]={width:m.width,height:m.height};
 }
 fs.writeFileSync(path.join(root,'content/image-dimensions.json'),JSON.stringify(sizes,null,2)+'\n');
 console.log('Built responsive WebP portraits, minified homepage CSS, and source image dimensions.');
})().catch(e=>{console.error(e);process.exit(1)});
