import http from 'node:http';
import fs from 'node:fs';
const root=process.cwd();
const files=new Map(),BUCKET={async put(key,value){files.set(key,value)},async get(key){return files.has(key)?{body:files.get(key)}:null},async head(key){return files.has(key)?{}:null}};
http.createServer(async(req,res)=>{try{const source=fs.readFileSync(root+'/worker/index.js','utf8');const worker=(await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'))).default;const data=[];for await(const c of req)data.push(c);const request=new Request('http://'+req.headers.host+req.url,{method:req.method,headers:req.headers,...(data.length?{body:Buffer.concat(data),duplex:'half'}:{})});const response=await worker.fetch(request,{BUCKET});res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()));}catch(e){res.writeHead(500);res.end(e.message)}}).listen(4173,'127.0.0.1',()=>console.log('Local: http://127.0.0.1:4173'));
