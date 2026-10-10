import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const source=fs.readFileSync('worker/index.js','utf8');
const load=async()=> (await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64')+'#'+Math.random())).default;
const request=new Request('https://example.test/api/confirm?signature='+'1'.repeat(88));
const original=globalThis.fetch;const providers=[];
try {
 globalThis.fetch=async(url)=>{providers.push(url);return url==='https://configured.test'?new Response('',{status:403}):new Response(JSON.stringify({result:{value:[{err:null,confirmationStatus:'finalized'}]}}));};
 let worker=await load();let result=await(await worker.fetch(request,{SOLANA_RPC_URL:'https://configured.test'})).json();assert.equal(result.confirmed,true);assert.deepEqual(providers,['https://configured.test','https://solana-rpc.publicnode.com']);
 globalThis.fetch=async()=>new Response(JSON.stringify({result:{value:[{err:{InstructionError:[2,{Custom:6045}]},confirmationStatus:'finalized'}]}}));
 result=await(await worker.fetch(request)).json();assert.equal(result.confirmed,false);assert.match(result.message,/shorter URL/);
 globalThis.fetch=async()=>{throw new Error('offline')};assert.equal((await worker.fetch(request)).status,503);
}finally{globalThis.fetch=original;}
const html=fs.readFileSync('src/page.html','utf8'),flow=html.slice(html.indexOf('function pendingLinks('),html.indexOf('\nfunction addRetry('));
const pending={mint:'test-mint',signature:'test-signature',profile:{symbol:'BUG'}};
async function scenario(reply){const values=new Map([['insectpad-pending',pending]]),messages=[],links=[];let attempts=0,retries=0,galleries=0;const context={storage:{get:k=>values.get(k),set:(k,v)=>values.set(k,v)},receipts:[],feedback:t=>messages.push(t),$:()=>({}),appendLink:(parent,text,url)=>links.push(url),renderGallery:()=>galleries++,addRetry:()=>retries++,api:async()=>{attempts++;if(reply instanceof Error)throw reply;return reply},setTimeout:fn=>{fn()}};vm.createContext(context);vm.runInContext(flow,context);await context.pollConfirmation(pending);return {values,messages,links,attempts,retries,galleries,receipts:context.receipts};}
let state=await scenario({confirmed:true});assert.equal(state.receipts.length,1);assert.equal(state.values.get('insectpad-pending'),null);assert.equal(state.galleries,1);
state=await scenario({error:{InstructionError:[2,{Custom:6045}]},message:'Metadata URL was too long. Review a new launch.'});assert.equal(state.values.get('insectpad-pending'),null);assert.equal(state.receipts.length,0);assert.match(state.messages.at(-1),/too long/);assert.ok(state.links.includes('https://solscan.io/tx/test-signature'));
state=await scenario(new Error('Confirmation service unavailable'));assert.equal(state.attempts,3);assert.equal(state.values.get('insectpad-pending'),pending);assert.equal(state.retries,1);assert.match(state.messages.at(-1),/could not verify/);
console.log('Passed: RPC failover, failed launch details, confirmation outage, recovery without duplicate launch.');
