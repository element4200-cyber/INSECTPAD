import fs from 'node:fs';
const page=fs.readFileSync('src/page.html','utf8');
const backend=fs.readFileSync('src/backend.js','utf8');
const tutorial=fs.readFileSync('assets/insect-tutorial.mp4').toString('base64');
const poster=fs.readFileSync('assets/tutorial-poster.png').toString('base64');
const library=fs.readFileSync('vendor/solana-web3-1.98.4.iife.min.js','utf8');
fs.mkdirSync('worker',{recursive:true});
fs.writeFileSync('worker/index.js','const PAGE = '+JSON.stringify(page)+';\nconst SOLANA_LIBRARY = '+JSON.stringify(library)+';\nconst TUTORIAL_VIDEO = '+JSON.stringify(tutorial)+';\nconst TUTORIAL_POSTER = '+JSON.stringify(poster)+';\n'+backend);
