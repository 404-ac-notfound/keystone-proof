import json
import pathlib
import subprocess
import yaml

root = pathlib.Path(__file__).parent
path = root / 'codex-review.yml.disabled'
w = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
assert w['on']['pull_request']['types'] == ['opened', 'synchronize', 'ready_for_review']
assert set(w['jobs']) == {'codex', 'post_feedback'}
assert w['permissions'] == {}
assert w['jobs']['codex']['if'] == '${{ false }}'
assert w['jobs']['post_feedback']['if'] == '${{ false }}'
read = w['jobs']['codex']
post = w['jobs']['post_feedback']
assert set(read['permissions'].values()) == {'read'}
assert post['permissions'] == {'pull-requests': 'write'}
assert not any('checkout' in s.get('uses', '') or 'openai' in str(s) for s in post['steps'])
assert read['steps'][-1]['with']['permission-profile'] == ':read-only'
assert read['steps'][-1]['with']['safety-strategy'] == 'drop-sudo'
assert read['steps'][-1]['with']['allow-users'] == '*'
assert 'pull_request_target' not in w['on']
assert path.name.endswith('.yml.disabled')
assert not str(path.relative_to(root.parents[2])).startswith('.github/workflows/')
scripts = {
    'guard': read['steps'][0]['with']['script'],
    'post': post['steps'][0]['with']['script'],
}
harness = r'''
const fs = require('fs');
const scripts = JSON.parse(fs.readFileSync(0, 'utf8'));
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const assert = require('assert/strict');
const guard = new AsyncFunction('github', 'context', 'core', scripts.guard);
const post = new AsyncFunction('github', 'context', 'core', scripts.post);
const head = 'a'.repeat(40), base = 'b'.repeat(40);
const p = {number: 7, head: {sha:head, ref:'job/7', repo:{full_name:'404-ac-notfound/keystone-proof'}}, base:{sha:base}};
const context = {repo:{owner:'404-ac-notfound', repo:'keystone-proof'}, runId:100,
  serverUrl:'https://github.com', payload:{pull_request:p, repository:{full_name:'404-ac-notfound/keystone-proof'}}};
let count = 0;
async function exercise(fn, spec={}, error='') {
  process.env.HAS_OPENAI_API_KEY='true';
  process.env.EXPIRES_AT='2026-10-23T00:00:00Z';
  process.env.PILOT_PR='7';
  process.env.CASH_CHECKED_AT=new Date().toISOString();
  process.env.INCLUDED_MINUTES='125';
  process.env.REVIEWED_HEAD=head;
  process.env.REVIEWED_BASE=base;
  process.env.REVIEW_TEXT='No defects. @codex review';
  Object.assign(process.env, spec.env || {});
  let output={}, posts=[];
  const current={...structuredClone(p), state:'open', ...spec.current};
  const comments = spec.comments || [];
  let pages=0;
  const github={paginate:async(fn)=>fn===github.rest.pulls.listFiles ? (spec.files || [{additions:1,deletions:1,patch:'diff'}]) : comments,
    request:async()=>({data:spec.diff || 'diff'}), rest:{
    pulls:{listFiles:()=>{},get:async()=>({data:current})},
    issues:{listComments:()=>{}, createComment:async x=>posts.push(x)},
    actions:{getWorkflowRun:async()=>({data:{workflow_id:4}}),
      listWorkflowRuns:async()=>({data:{workflow_runs: spec.many ? Array.from({length:100},()=>({id:101})) : spec.runs || []}})}
  }};
  const core={setOutput:(k,v)=>output[k]=v, info:()=>{}};
  const ctx=structuredClone(context);
  if(spec.fork) ctx.payload.pull_request.head.repo.full_name='someone/fork';
  try {
    await fn(github,ctx,core);
    assert.equal(error, '', 'expected failure: '+error);
  } catch(e) {
    if(!error) throw e;
    assert.ok(e.message.includes(error), e.message+' expected '+error);
  }
  count++;
  return {output,posts};
}
(async()=>{
  assert.equal((await exercise(guard)).output.head,head);
  await exercise(guard,{env:{HAS_OPENAI_API_KEY:'false'}},'missing');
  await exercise(guard,{env:{CASH_CHECKED_AT:''}},'attestation');
  await exercise(guard,{env:{CASH_CHECKED_AT:new Date(Date.now()-3601000).toISOString()}},'attestation');
  await exercise(guard,{env:{CASH_CHECKED_AT:new Date(Date.now()+60000).toISOString()}},'attestation');
  await exercise(guard,{env:{INCLUDED_MINUTES:'124'}},'125');
  await exercise(guard,{env:{INCLUDED_MINUTES:''}},'125');
  await exercise(guard,{env:{INCLUDED_MINUTES:'Infinity'}},'125');
  await exercise(guard,{fork:true},'fork');
  await exercise(guard,{current:{head:{...p.head,sha:'c'.repeat(40)}}},'stale');
  await exercise(guard,{current:{base:{sha:'c'.repeat(40)}}},'stale');
  await exercise(guard,{current:{state:'closed'}},'closed');
  const marker=`<!-- keystone-codex-action:${head} -->`;
  await exercise(guard,{comments:[{user:{login:'github-actions[bot]'},body:marker}]},'already reviewed');
  await exercise(guard,{comments:[{user:{login:'404-ac-notfound'},body:marker}]});
  await exercise(guard,{runs:[{id:99,status:'failure'},{id:100}]});
  await exercise(guard,{runs:[{id:98,status:'failure'},{id:99,status:'cancelled'},{id:100}]},'ceiling');
  await exercise(guard,{many:true},'too large');
  const ok=await exercise(post);
  assert.equal(ok.posts.length,1);
  assert.ok(ok.posts[0].body.startsWith(marker));
  assert.ok(ok.posts[0].body.includes(head) && ok.posts[0].body.includes(base));
  assert.ok(!ok.posts[0].body.includes('@codex'));
  await exercise(post,{current:{state:'closed'}},'closed');
  await exercise(post,{current:{head:{...p.head,sha:'c'.repeat(40)}}},'stale');
  await exercise(post,{current:{base:{sha:'c'.repeat(40)}}},'stale');
  await exercise(post,{current:{head:{...p.head,repo:{full_name:'someone/fork'}}}},'forked');
  assert.equal((await exercise(post,{comments:[{user:{login:'github-actions[bot]'},body:marker}]})).posts.length,0);
  assert.equal((await exercise(post,{comments:[{user:{login:'404-ac-notfound'},body:marker}]})).posts.length,1);
  await exercise(post,{env:{REVIEW_TEXT:'   '}},'empty');
  await exercise(post,{env:{REVIEW_TEXT:'x'.repeat(12001)}},'oversized');
  await exercise(guard,{env:{PILOT_PR:'8'}},'named');
  await exercise(guard,{env:{EXPIRES_AT:''}},'expired');
  await exercise(guard,{files:Array.from({length:51},()=>({additions:0,deletions:0,patch:'diff'}))},'size');
  await exercise(guard,{files:[{additions:1001,deletions:0,patch:'diff'}]},'size');
  await exercise(guard,{files:[{additions:1,deletions:0}]},'binary');
  await exercise(guard,{diff:'x'.repeat(131073)},'byte');
  const RealDate=Date;
  global.Date=class extends RealDate { static now(){return RealDate.parse('2026-10-23T00:00:00Z');} };
  await exercise(guard,{},'expired');
  console.log(`PASS: YAML/two-job/static permission checks; ${count} offline guard/posting scenarios`);
})().catch(e=>{console.error(e);process.exit(1)});
'''
result = subprocess.run(['node', '-e', harness], input=json.dumps(scripts), text=True,
                        capture_output=True)
print(result.stdout, end='')
print(result.stderr, end='')
if result.returncode:
    raise SystemExit(result.returncode)

fetch = next(s['run'] for s in read['steps'] if 'run' in s)
subprocess.run(['bash', '-n'], input=fetch, text=True, check=True)
print('PASS: fetch script bash syntax; no workflow installed')
