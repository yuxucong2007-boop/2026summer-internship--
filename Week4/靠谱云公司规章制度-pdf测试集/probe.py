import json, subprocess, os

TOKEN=open('token.txt').read().strip()
URL='https://59.56.96.36:8080/api/v1/chat/completions'
KID='5e4a239c-2aae-4702-b6d4-2e292943fb81'

def probe(q):
    body={'model':'kpc.glm-5.2','messages':[{'role':'user','content':q}],'files':[{'type':'collection','id':KID}],'stream':True}
    req=json.dumps(body,ensure_ascii=False)
    r=subprocess.run(['curl','-sk','-m','120','--noproxy','*','-H','Authorization: Bearer '+TOKEN,'-H','Content-Type: application/json','-d',req,URL],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode!=0:
        return None, r.stderr
    sources=None
    for line in r.stdout.split('\n'):
        line=line.strip()
        if not line.startswith('data: '): continue
        p=line[6:]
        if p=='[DONE]': continue
        try: obj=json.loads(p)
        except: continue
        if obj.get('sources'): sources=obj['sources']
    return sources, None

for q in ['加班餐补的标准是多少？','轻度违纪行为会受到什么处分？','绩效等级S对应的分数区间是多少？']:
    print('========== 问题:',q)
    src,err=probe(q)
    if err: print('  ERR:',err[:200]); continue
    if not src: print('  !! no sources'); continue
    for s in src:
        docs=s.get('document',[])
        metas=s.get('metadata',[])
        dists=s.get('distances',[])
        print(f"  source: {s['source']}")
        for i,(d,m,ds) in enumerate(zip(docs,metas,dists)):
            print(f"   [{i}] name={m.get('name')} page_label={m.get('page_label')} score={ds:.3f}")
            print(f"       head: {d[:55]!r}")
            print(f"       tail: {d[-55:]!r}")
