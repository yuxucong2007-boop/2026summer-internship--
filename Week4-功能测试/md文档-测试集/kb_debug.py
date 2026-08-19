# -*- coding: utf-8 -*-
import json, urllib.request, ssl, re

BASE = "https://59.56.96.36:8080"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3dC1zaWduaW5nLXYxIiwidHlwIjoiYXQrand0In0.eyJzdWIiOiIxIiwiZXhwIjoxNzg3MTA0MDY5LCJpYXQiOjE3ODcwMTc2NjksImp0aSI6IjNlYjhhY2IwLTkwMjYtNDM1NS1hYzljLWY0YmJiZDMxOGI1ZCIsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJyb2xlcyI6WyJhZG1pbiIsInN1cGVyYWRtaW4iXSwiY2xpZW50X2lkIjoiYXJnbyJ9.BJWXhpZRLMGRXvZbz3zubrpCd-Q3Jabel5B1GMqT8gBR1zKhjPs4fDyrPpydEwI3dEuoutpg8-nq-rRDI9j6jzg6k1w99NeuLm3BSFoIdSAK4JS9-PVvYSnuP1KfoCu6pOcV6wTQrSay7KJbEFEc08zOjDUq6AeO4grc8t7-Bvx7V8rX9ernkc_cSUCn_C9AUWzrd_MU0rguuqny8irMN_fTlMqSG_XOWOngGOvxyME-PY5fHpTrvx0nP3zfbB2oQO3xwYltMQHwLhZXdaW8YpwWv1qYVhuXRdJ7VaD1xIkeeLuL4DCBcGimeSlZk8zzmopCXgODACn49Cn7BF-R_w"
KB = "9e5dbbec-6c08-47f3-b2bb-59a3cc8cfed2"
MODEL = "kpc.deepseek-v4-pro"
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
CHUNK_RE = re.compile(r"\b([a-z]{2,5}_\d{3})\b")

def get_sources(q, timeout=120):
    body = json.dumps({"model":MODEL,"stream":True,"messages":[{"role":"user","content":q}],
        "files":[{"type":"collection","id":KB}],"metadata":{}}).encode("utf-8")
    req = urllib.request.Request(BASE+"/api/v1/chat/completions", data=body, method="POST",
        headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json","Accept":"text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    sources=None
    buf=b""
    for raw in resp:
        buf+=raw
        while b"\n" in buf:
            line,buf=buf.split(b"\n",1); line=line.strip()
            if not line.startswith(b"data:"): continue
            payload=line[5:].strip()
            if payload==b"[DONE]": continue
            try: obj=json.loads(payload)
            except: continue
            if "sources" in obj:
                sources=obj["sources"]
                try: resp.close()
                except: pass
                return sources
    return sources

for q in ["员工转正后有多少天年假？", "API每分钟最多能调用多少次？"]:
    s = get_sources(q)
    print("\n##### QUERY:", q)
    print("num sources:", len(s) if s else 0)
    if not s: continue
    for si,src in enumerate(s):
        docs = src.get("document",[])
        if isinstance(docs,str): docs=[docs]
        print(f"  -- source {si}: source={src.get('source')} #docs={len(docs)}")
        for di,d in enumerate(docs):
            txt = d if isinstance(d,str) else json.dumps(d,ensure_ascii=False)
            ids = CHUNK_RE.findall(txt)
            print(f"     doc[{di}] len={len(txt)} chunk_ids={ids} head={txt[:70]!r} tail={txt[-70:]!r}")
