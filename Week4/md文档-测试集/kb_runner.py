# -*- coding: utf-8 -*-
"""知识库命中率测试：针对 https://59.56.96.36:8080 的 'test-命中率' 知识库。
系统把 test_knowledge_base.md 切成 3 个大段，每次检索返回 3 段但顺序随问题变化。
因此在【段落级别】衡量检索质量，并保留 chunk_id 级软命中以供参考。
"""
import json, ssl, re, time, urllib.request, pathlib, sys

BASE = "https://59.56.96.36:8080"
TOKEN = pathlib.Path("token.txt").read_text(encoding="utf-8").strip() if pathlib.Path("token.txt").exists() else \
  "eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3dC1zaWduaW5nLXYxIiwidHlwIjoiYXQrand0In0.eyJzdWIiOiIxIiwiZXhwIjoxNzg3MTA0MDY5LCJpYXQiOjE3ODcwMTc2NjksImp0aSI6IjNlYjhhY2IwLTkwMjYtNDM1NS1hYzljLWY0YmJiZDMxOGI1ZCIsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJyb2xlcyI6WyJhZG1pbiIsInN1cGVyYWRtaW4iXSwiY2xpZW50X2lkIjoiYXJnbyJ9.BJWXhpZRLMGRXvZbz3zubrpCd-Q3Jabel5B1GMqT8gBR1zKhjPs4fDyrPpydEwI3dEuoutpg8-nq-rRDI9j6jzg6k1w99NeuLm3BSFoIdSAK4JS9-PVvYSnuP1KfoCu6pOcV6wTQrSay7KJbEFEc08zOjDUq6AeO4grc8t7-Bvx7V8rX9ernkc_cSUCn_C9AUWzrd_MU0rguuqny8irMN_fTlMqSG_XOWOngGOvxyME-PY5fHpTrvx0nP3zfbB2oQO3xwYltMQHwLhZXdaW8YpwWv1qYVhuXRdJ7VaD1xIkeeLuL4DCBcGimeSlZk8zzmopCXgODACn49Cn7BF-R_w"
KB = "9e5dbbec-6c08-47f3-b2bb-59a3cc8cfed2"
MODEL = "kpc.deepseek-v4-pro"
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
CHUNK_RE = re.compile(r"\b([a-z]{2,5}_\d{3})\b")

# 系统实际切分后的 3 个段落 -> chunk_id 映射（经实测确认）
SEG_A = ["hr_001","hr_002","hr_003","hr_004","hr_005","fin_001"]            # 段A: HR + 差旅住宿
SEG_B = ["fin_002","fin_003","fin_004","fin_005","it_001","it_002","it_003","it_004"]  # 段B: 报销/IT
SEG_C = ["prod_001","prod_002","prod_003","prod_004","cs_001","cs_002","cs_003","sec_001","sec_002"]  # 段C: 产品/客服/安全
SEG_OF = {}
for name, ids in [("A",SEG_A),("B",SEG_B),("C",SEG_C)]:
    for cid in ids: SEG_OF[cid] = name

def get_ranked_segments(q, timeout=150):
    """返回检索到的段落顺序（按相关性排名），元素为 {'seg','chunk_ids','len','head'}。"""
    body = json.dumps({"model":MODEL,"stream":True,"messages":[{"role":"user","content":q}],
        "files":[{"type":"collection","id":KB}],"metadata":{}}).encode("utf-8")
    req = urllib.request.Request(BASE+"/api/v1/chat/completions", data=body, method="POST",
        headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json","Accept":"text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    sources=None; buf=b""
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
                break
        if sources: break
    if not sources: return []
    ranked=[]
    for src in sources:
        docs=src.get("document",[])
        if isinstance(docs,str): docs=[docs]
        for d in docs:
            txt = d if isinstance(d,str) else json.dumps(d,ensure_ascii=False)
            ids=CHUNK_RE.findall(txt)
            # 用出现的 chunk_id 集合判定属于哪一段
            segs=set(SEG_OF.get(i) for i in ids if i in SEG_OF)
            seg = next(iter(segs)) if len(segs)==1 else ("?" if not segs else "/".join(sorted(segs)))
            ranked.append({"seg":seg,"chunk_ids":ids,"len":len(txt),"head":txt[:40]})
    return ranked

def mrr_of_rank(rank):  # rank 1-based; None if not found
    return 1.0/rank if rank else 0.0

def main():
    queries=[json.loads(l) for l in pathlib.Path("test_queries.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    results=[]
    for i,q in enumerate(queries,1):
        ranked=[]
        err=None
        for attempt in range(3):
            try:
                ranked=get_ranked_segments(q["query"])
                break
            except Exception as e:
                err=str(e); time.sleep(2)
        rec_segs=[r["seg"] for r in ranked]
        exp_doc_ids=q["relevant_doc_ids"]
        exp_segs=sorted(set(SEG_OF[c] for c in exp_doc_ids if c in SEG_OF))
        # 段位排名指标
        hit1 = any(s in exp_segs for s in rec_segs[:1]) if rec_segs else False
        hit2 = any(s in exp_segs for s in rec_segs[:2]) if rec_segs else False
        hit3 = any(s in exp_segs for s in rec_segs[:3]) if rec_segs else False
        first_correct_rank=None
        for idx,s in enumerate(rec_segs,1):
            if s in exp_segs: first_correct_rank=idx; break
        mrr=mrr_of_rank(first_correct_rank)
        # chunk_id 软命中（无论排名，相关 chunk 是否出现在返回集合里）
        rec_chunk_ids=set()
        for r in ranked: rec_chunk_ids.update(r["chunk_ids"])
        soft_hit = any(c in rec_chunk_ids for c in exp_doc_ids) if exp_doc_ids else False
        results.append({
            "query_id":q["query_id"],"query":q["query"],"category":q.get("category",""),
            "answerable":q["answerable"],"expected_doc_ids":exp_doc_ids,"expected_segs":exp_segs,
            "retrieved_segs":rec_segs,"retrieved_ranked":[{"seg":r["seg"],"chunk_ids":r["chunk_ids"]} for r in ranked],
            "hit1":hit1,"hit2":hit2,"hit3":hit3,"first_correct_rank":first_correct_rank,"mrr":mrr,
            "soft_hit_chunk":soft_hit,"error":err,
        })
        status = "OK" if not err else "ERR"
        flag = ""
        if q["answerable"]:
            flag = "HIT" if hit1 else "MISS(top1)"
        else:
            flag = "误召回" if rec_segs else "无召回"
        print(f"[{i:02d}/{len(queries)}] {q['query_id']} {status} order={rec_segs} exp={exp_segs} {flag}")
        time.sleep(0.4)
    pathlib.Path("results_raw.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    # 指标
    ans=[r for r in results if r["answerable"] and not r["error"]]
    noans=[r for r in results if not r["answerable"] and not r["error"]]
    n=len(ans)
    m={"total_queries":len(results),
       "answerable_evaluated":n,
       "noanswer_evaluated":len(noans),
       "Hit@1_segment": round(sum(r["hit1"] for r in ans)/n,4) if n else 0,
       "Hit@2_segment": round(sum(r["hit2"] for r in ans)/n,4) if n else 0,
       "Hit@3_segment": round(sum(r["hit3"] for r in ans)/n,4) if n else 0,
       "Recall@1_segment": round(sum(r["hit1"] for r in ans)/n,4) if n else 0,
       "Recall@3_segment": round(sum(r["hit3"] for r in ans)/n,4) if n else 0,
       "MRR_segment": round(sum(r["mrr"] for r in ans)/n,4) if n else 0,
       "soft_hit_chunk_anypos": round(sum(r["soft_hit_chunk"] for r in ans)/n,4) if n else 0,
       "noanswer_false_recall_rate": round(sum(1 for r in noans if r["retrieved_segs"])/len(noans),4) if noans else 0,
    }
    pathlib.Path("metrics.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
    print("\n=== METRICS ===")
    print(json.dumps(m,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
