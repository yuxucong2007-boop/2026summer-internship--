# -*- coding: utf-8 -*-
"""知识库命中率复测（2026-08-18 第二轮）
对象：https://59.56.96.36:8080 知识库「test-命中率」(9e5dbbec-6c08-47f3-b2bb-59a3cc8cfed2)
测试集：test_queries.jsonl（35 条，与第一轮完全相同，保证可比）
步骤：跑 35 条 -> 写 results_raw.json / metrics.json -> 动态生成 知识库命中率测试报告.html
"""
import json, re, ssl, time, urllib.request, pathlib
from collections import defaultdict

BASE = "https://59.56.96.36:8080"
HERE = pathlib.Path(__file__).parent

# ---- 读取凭据 ----
text = open(HERE / "kb_test.py", encoding="utf-8").read()
TOKEN = re.search(r'^TOKEN\s*=\s*"([^"]+)"', text, re.M).group(1)
KB = re.search(r'^KB\s*=\s*"([^"]+)"', text, re.M).group(1)
MODEL = re.search(r'^MODEL\s*=\s*"([^"]+)"', text, re.M).group(1)

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
CHUNK_RE = re.compile(r"\b([a-z]{2,5}_\d{3})\b")

# ---- 系统实际 3 大段 -> chunk 映射（探测确认）----
SEG_A = ["hr_001","hr_002","hr_003","hr_004","hr_005","fin_001"]
SEG_B = ["fin_002","fin_003","fin_004","fin_005","it_001","it_002","it_003","it_004"]
SEG_C = ["prod_001","prod_002","prod_003","prod_004","cs_001","cs_002","cs_003","sec_001","sec_002"]
SEGMENTS = {"A": SEG_A, "B": SEG_B, "C": SEG_C}
SEG_OF = {}
for name, ids in SEGMENTS.items():
    for cid in ids:
        SEG_OF[cid] = name

def get_ranked_segments(q, timeout=180):
    """返回检索到的段落（按相关性排序），元素 {'seg','chunk_ids','len','head'}。"""
    body = json.dumps({"model": MODEL, "stream": True,
                       "messages": [{"role": "user", "content": q}],
                       "files": [{"type": "collection", "id": KB}],
                       "metadata": {}}).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/v1/chat/completions", data=body, method="POST",
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
                 "Accept": "text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    sources = None; buf = b""
    for raw in resp:
        buf += raw
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1); line = line.strip()
            if not line.startswith(b"data:"):
                continue
            payload = line[5:].strip()
            if payload == b"[DONE]":
                continue
            try:
                obj = json.loads(payload)
            except Exception:
                continue
            if "sources" in obj:
                sources = obj["sources"]
                try: resp.close()
                except Exception: pass
                return sources
    return sources

def parse_ranked(sources):
    ranked = []
    if not sources:
        return ranked
    for src in sources:
        docs = src.get("document", [])
        if isinstance(docs, str):
            docs = [docs]
        for d in docs:
            txt = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
            ids = CHUNK_RE.findall(txt)
            segs = set(SEG_OF.get(i) for i in ids if i in SEG_OF)
            seg = next(iter(segs)) if len(segs) == 1 else ("?" if not segs else "/".join(sorted(segs)))
            ranked.append({"seg": seg, "chunk_ids": ids, "len": len(txt), "head": txt[:50]})
    return ranked

def main():
    queries = [json.loads(l) for l in (HERE / "test_queries.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    results = []
    for i, q in enumerate(queries, 1):
        ranked = []; err = None
        for attempt in range(3):
            try:
                ranked = parse_ranked(get_ranked_segments(q["query"]))
                if ranked:
                    break
            except Exception as e:
                err = str(e); time.sleep(2)
        rec_segs = [r["seg"] for r in ranked]
        exp_doc_ids = q["relevant_doc_ids"]
        exp_segs = sorted(set(SEG_OF[c] for c in exp_doc_ids if c in SEG_OF))
        hit1 = any(s in exp_segs for s in rec_segs[:1]) if rec_segs else False
        hit2 = any(s in exp_segs for s in rec_segs[:2]) if rec_segs else False
        hit3 = any(s in exp_segs for s in rec_segs[:3]) if rec_segs else False
        first_correct_rank = None
        for idx, s in enumerate(rec_segs, 1):
            if s in exp_segs:
                first_correct_rank = idx; break
        mrr = (1.0 / first_correct_rank) if first_correct_rank else 0.0
        rec_chunk_ids = []
        for r in ranked:
            for c in r["chunk_ids"]:
                if c not in rec_chunk_ids:
                    rec_chunk_ids.append(c)
        # chunk 软命中：期望 chunk 是否出现在返回集合中（含其在返回序列中的首个位置）
        first_chunk_rank = None
        for idx, c in enumerate(rec_chunk_ids, 1):
            if c in exp_doc_ids:
                first_chunk_rank = idx; break
        soft_hit = first_chunk_rank is not None
        results.append({
            "query_id": q["query_id"], "query": q["query"], "category": q.get("category", ""),
            "answerable": q["answerable"], "expected_doc_ids": exp_doc_ids, "expected_segs": exp_segs,
            "retrieved_segs": rec_segs,
            "retrieved_ranked": [{"seg": r["seg"], "chunk_ids": r["chunk_ids"], "len": r["len"]} for r in ranked],
            "hit1": hit1, "hit2": hit2, "hit3": hit3,
            "first_correct_rank": first_correct_rank, "mrr": mrr,
            "soft_hit_chunk": soft_hit, "first_chunk_rank": first_chunk_rank,
            "error": err,
        })
        flag = ""
        if err:
            flag = "ERR"
        elif q["answerable"]:
            flag = "HIT" if hit1 else "MISS(top1)"
        else:
            flag = "误召回" if rec_segs else "无召回"
        print(f"[{i:02d}/{len(queries)}] {q['query_id']} {flag} order={rec_segs} exp={exp_segs}")
        time.sleep(0.4)

    (HERE / "results_raw.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ans = [r for r in results if r["answerable"] and not r["error"]]
    noans = [r for r in results if not r["answerable"] and not r["error"]]
    n = len(ans)
    m = {
        "total_queries": len(results),
        "answerable_evaluated": n,
        "noanswer_evaluated": len(noans),
        "Hit@1_segment": round(sum(r["hit1"] for r in ans) / n, 4) if n else 0,
        "Hit@2_segment": round(sum(r["hit2"] for r in ans) / n, 4) if n else 0,
        "Hit@3_segment": round(sum(r["hit3"] for r in ans) / n, 4) if n else 0,
        "Recall@1_segment": round(sum(r["hit1"] for r in ans) / n, 4) if n else 0,
        "Recall@3_segment": round(sum(r["hit3"] for r in ans) / n, 4) if n else 0,
        "MRR_segment": round(sum(r["mrr"] for r in ans) / n, 4) if n else 0,
        "soft_hit_chunk_anypos": round(sum(r["soft_hit_chunk"] for r in ans) / n, 4) if n else 0,
        "noanswer_false_recall_rate": round(sum(1 for r in noans if r["retrieved_segs"]) / len(noans), 4) if noans else 0,
        "full_return_rate": round(sum(1 for r in results if not r["error"] and len(r["retrieved_segs"]) == 3) / len(results), 4) if results else 0,
        "tested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "kb_id": KB, "model": MODEL,
    }
    (HERE / "metrics.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== METRICS ===")
    print(json.dumps(m, ensure_ascii=False, indent=2))
    return results, m

def render_report(results, m):
    # 类别级 Hit@1
    cat_total = defaultdict(int); cat_hit = defaultdict(int)
    for r in results:
        if r["answerable"] and not r["error"]:
            cat_total[r["category"]] += 1
            if r["hit1"]:
                cat_hit[r["category"]] += 1
    cat_data = sorted(((c, cat_hit[c], cat_total[c]) for c in cat_total), key=lambda x: x[0])

    rows = []
    for r in results:
        if r["answerable"] and not r["error"]:
            if r["hit1"]:
                tag = '<span class="tag hit">命中</span>'
            else:
                tag = f'<span class="tag miss">未命中Top1(rank{r["first_correct_rank"]})</span>'
        elif not r["answerable"] and not r["error"]:
            tag = '<span class="tag fa">误召回</span>' if r["retrieved_segs"] else '<span class="tag na">无召回</span>'
        else:
            tag = '<span class="tag na">ERR</span>'
        order = " → ".join(r["retrieved_segs"]) if r["retrieved_segs"] else "—"
        exp = ",".join(r["expected_segs"]) or "无"
        cls = "missrow" if (r["answerable"] and not r["error"] and not r["hit1"]) else ("farow" if (not r["answerable"] and not r["error"]) else "")
        rows.append(f'<tr class="{cls}"><td>{r["query_id"]}</td><td class="q">{r["query"]}</td><td>{r["category"]}</td><td>{exp}</td><td class="mono">{order}</td><td>{tag}</td></tr>')
    cat_rows = ""
    for c, h, t in cat_data:
        pct = round(h / t * 100)
        cat_rows += f'<tr><td>{c}</td><td>{h}/{t}</td><td>{pct}%</td><td><div class="bar"><div class="barfill" style="width:{pct}%"></div></div></td></tr>'

    # 关键发现（动态）
    n_docs = 3
    seg_desc = "｜".join(f'段{name}({len(ids)}块:{ids[0]}~{ids[-1]})' for name, ids in SEGMENTS.items())
    top1_misses = [r for r in results if r["answerable"] and not r["error"] and not r["hit1"]]
    miss_list = "、".join(f'<b>{r["query_id"]}</b>「{r["query"]}」(期望段{",".join(r["expected_segs"])}→实际第{r["first_correct_rank"]}名)' for r in top1_misses) or "无"
    noans = [r for r in results if not r["answerable"] and not r["error"]]
    noans_desc = "、".join(r["query_id"] for r in noans) or "无"

    h1 = m["Hit@1_segment"] * 100; h2 = m["Hit@2_segment"] * 100; h3 = m["Hit@3_segment"] * 100
    r3 = m["Recall@3_segment"] * 100; fr = m["noanswer_false_recall_rate"] * 100
    n_ok = m["answerable_evaluated"]; miss_n = len(top1_misses); hit_n = n_ok - miss_n

    html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>知识库命中率测试报告 · 星河科技 test-命中率（复测）</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#f6f7f9;--card:#fff;--line:#e5e7eb;--t1:#111827;--t2:#4b5563;--t3:#9ca3af;
--brand:#2563eb;--brandbg:#eff6ff;--green:#16a34a;--red:#dc2626;--amber:#d97706;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--t1);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}}
.wrap{{max-width:1100px;margin:0 auto;padding:28px 20px 60px}}
h1{{font-size:24px;margin:0 0 4px}}.sub{{color:var(--t2);font-size:14px;margin-bottom:22px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 16px}}
.card .lab{{font-size:12px;color:var(--t3);letter-spacing:.5px}}.card .val{{font-size:30px;font-weight:700;margin-top:4px}}
.card .hint{{font-size:12px;color:var(--t2);margin-top:2px}}
.section{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:18px 0}}
.section h2{{font-size:17px;margin:0 0 6px}}.section p{{color:var(--t2);font-size:14px;margin:6px 0}}
.find{{display:flex;gap:12px;align-items:flex-start;margin:12px 0;padding:12px 14px;border-radius:10px;background:var(--brandbg);border:1px solid #dbeafe}}
.find .ico{{font-size:20px}}.find .txt{{font-size:14px;color:var(--t1)}}
.find .txt b{{color:var(--brand)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}}
th{{background:#f9fafb;color:var(--t2);font-weight:600;font-size:12px;position:sticky;top:0}}
td.q{{max-width:320px}}td.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--t2)}}
.tag{{display:inline-block;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:600}}
.hit{{background:#dcfce7;color:#166534}}.miss{{background:#fee2e2;color:#991b1b}}.fa{{background:#fef3c7;color:#92400e}}.na{{background:#f3f4f6;color:#6b7280}}
tr.missrow td{{background:#fff7f7}}tr.farow td{{background:#fffbeb}}
.bar{{background:#eef2f7;border-radius:5px;height:14px;min-width:60px}}.barfill{{background:var(--brand);height:100%;border-radius:5px}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}}
.chartbox{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;height:300px}}
.scroll{{max-height:560px;overflow:auto;border:1px solid var(--line);border-radius:12px}}
.legend{{font-size:12px;color:var(--t3);margin-top:8px}}
.foot{{color:var(--t3);font-size:12px;text-align:center;margin-top:30px}}
code{{background:#f3f4f6;padding:1px 5px;border-radius:4px;font-size:12px}}
</style></head><body><div class="wrap">
<h1>知识库命中率测试报告（复测）</h1>
<div class="sub">目标：<code>https://59.56.96.36:8080</code> · 知识库「test-命中率」<code>{m['kb_id'][:8]}…</code> · 模型 <code>{m['model']}</code> · 测试集 35 条（与第一轮相同） · 测试时间 {m['tested_at']}</div>

<div class="grid">
  <div class="card"><div class="lab">段落级 Hit Rate@1</div><div class="val" style="color:var(--brand)">{h1:.1f}%</div><div class="hint">正确段排第1 / {n_ok} 条可答</div></div>
  <div class="card"><div class="lab">段落级 Hit Rate@2</div><div class="val" style="color:var(--green)">{h2:.0f}%</div><div class="hint">前2名含正确段</div></div>
  <div class="card"><div class="lab">MRR（段落）</div><div class="val">{m['MRR_segment']:.3f}</div><div class="hint">平均倒数排名</div></div>
  <div class="card"><div class="lab">无答案误召回率</div><div class="val" style="color:var(--red)">{fr:.0f}%</div><div class="hint">{m['noanswer_evaluated']} 条无答案问题仍返回文档</div></div>
</div>

<div class="section">
  <h2>关键发现（复测 vs 第一轮）</h2>
  <div class="find"><div class="ico">📏</div><div class="txt"><b>分块仍为 3 大段：</b>重新导入后系统依然按固定字数把 23 个 chunk 切成 <b>{n_docs} 段</b>（未按 <code>## chunk_id</code> 边界切分）：{seg_desc}。因此检索单元仍是"段落"，chunk 级命中率依旧无法按设计口径计算。</div></div>
  <div class="find"><div class="ico">🔁</div><div class="txt"><b>全量返回：</b>全量返回率 {m['full_return_rate']*100:.0f}%（{len(results)} 条中 {round(m['full_return_rate']*len(results))} 条返回了全部 3 段），Hit@2/Hit@3 无区分度；有区分度的只有 <b>Hit@1 = {h1:.1f}%</b>、MRR = {m['MRR_segment']:.3f}。</div></div>
  <div class="find"><div class="ico">🎯</div><div class="txt"><b>Top-1 未命中 {miss_n} 条：</b>{miss_list if miss_list else '本轮全部命中，无 rank2+ 情况。'}</div></div>
  <div class="find"><div class="ico">⚠️</div><div class="txt"><b>无答案误召回：</b>{noans_desc}（{len(noans)} 条）本应拒答，实际误召回率 {fr:.0f}%——仍无相关性阈值 / 拒答机制。</div></div>
</div>

<div class="charts">
  <div class="chartbox"><canvas id="c1"></canvas></div>
  <div class="chartbox"><canvas id="c2"></canvas></div>
</div>

<div class="section">
  <h2>建议</h2>
  <p>1. <b>修复分块</b>：把平台的分块策略改为"按 <code>##</code> 标题切分"，或把 <code>test_knowledge_base.md</code> 拆成 23 个独立文件导入——这是 chunk 级命中率可测、召回更精准的前提。</p>
  <p>2. <b>调小 Top-K</b>：当前 Top-K ≥ 段总数导致全量返回；分块修复后把返回条数设为 3–5。</p>
  <p>3. <b>相关性阈值 / 拒答</b>：降低无答案问题误召回（当前 {fr:.0f}%），避免模型基于无关段落硬编答案。</p>
  <p>4. <b>可选 Reranker</b>：针对段间语义混淆进一步拉高 Hit@1。</p>
</div>

<div class="section">
  <h2>各类别 Hit@1</h2>
  <table><thead><tr><th>类别</th><th>命中/总数</th><th>Hit@1</th><th>分布</th></tr></thead><tbody>
  {cat_rows}
  </tbody></table>
</div>

<div class="section">
  <h2>逐条明细（35条）</h2>
  <div class="legend">检索顺序为段落相关性排名（A/B/C）；"期望段"为含标准答案 chunk 的段。</div>
  <div class="scroll"><table>
  <thead><tr><th>ID</th><th>问题</th><th>类别</th><th>期望段</th><th>检索顺序</th><th>结果</th></tr></thead><tbody>
  {''.join(rows)}
  </tbody></table></div>
</div>

<div class="foot">数据来源：results_raw.json · metrics.json · 由 WorkBuddy 自动测试生成（复测 2026-08-18）</div>
</div>
<script>
const COLOR='#2563eb',GREEN='#16a34a',RED='#dc2626',AMBER='#d97706';
new Chart(document.getElementById('c1'),{{type:'bar',data:{{labels:['Hit@1','Hit@2','Hit@3','Recall@3'],datasets:[{{data:[{h1},{h2},{h3},{r3}],backgroundColor:[COLOR,GREEN,GREEN,GREEN],borderRadius:6}}]}},options:{{plugins:{{title:{{display:true,text:'段落级命中率指标 (%)',font:{{size:14}}}},legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,max:105,ticks:{{callback:v=>v+'%'}}}}}}}}}});
new Chart(document.getElementById('c2'),{{type:'doughnut',data:{{labels:['Top1命中','Top1未命中(rank2+)'],datasets:[{{data:[{hit_n},{miss_n}],backgroundColor:[GREEN,RED],borderWidth:0}}]}},options:{{plugins:{{title:{{display:true,text:'{n_ok}条可答问题 Top-1 分布',font:{{size:14}}}},legend:{{position:'bottom'}}}},cutout:'62%'}}}});
</script>
</body></html>"""
    (HERE / "知识库命中率测试报告.html").write_text(html, encoding="utf-8")
    print("written 知识库命中率测试报告.html", len(html), "bytes")

if __name__ == "__main__":
    results, m = main()
    render_report(results, m)
