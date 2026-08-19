# -*- coding: utf-8 -*-
import json, pathlib

results = json.loads(pathlib.Path("results_raw.json").read_text(encoding="utf-8"))
metrics = json.loads(pathlib.Path("metrics.json").read_text(encoding="utf-8"))

# 类别级 hit@1
from collections import defaultdict
cat_total=defaultdict(int); cat_hit=defaultdict(int)
for r in results:
    if r["answerable"] and not r["error"]:
        cat_total[r["category"]]+=1
        if r["hit1"]: cat_hit[r["category"]]+=1
cat_data=[(c,cat_hit[c],cat_total[c]) for c in cat_total]

rows=[]
for r in results:
    if r["answerable"]:
        if r["hit1"]: tag='<span class="tag hit">命中</span>'
        else: tag=f'<span class="tag miss">未命中Top1(rank{r["first_correct_rank"]})</span>'
    else:
        tag='<span class="tag fa">误召回</span>' if r["retrieved_segs"] else '<span class="tag na">无召回</span>'
    order=" → ".join(r["retrieved_segs"]) if r["retrieved_segs"] else "—"
    exp=",".join(r["expected_segs"]) or "无"
    cls="missrow" if (r["answerable"] and not r["hit1"]) else ("farow" if not r["answerable"] else "")
    rows.append(f'<tr class="{cls}"><td>{r["query_id"]}</td><td class="q">{r["query"]}</td><td>{r["category"]}</td><td>{exp}</td><td class="mono">{order}</td><td>{tag}</td></tr>')

cat_rows=""
for c,h,t in sorted(cat_data,key=lambda x:x[0]):
    pct=round(h/t*100)
    cat_rows+=f'<tr><td>{c}</td><td>{h}/{t}</td><td>{pct}%</td><td><div class="bar"><div class="barfill" style="width:{pct}%"></div></div></td></tr>'

m=metrics
html=f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>知识库命中率测试报告 · 星河科技 test-命中率</title>
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
<h1>知识库命中率测试报告</h1>
<div class="sub">目标：<code>https://59.56.96.36:8080</code> · 知识库「test-命中率」· 模型 deepseek-v4-pro · 测试集 35 条（test_queries.jsonl） · 生成时间 2026-08-18</div>

<div class="grid">
  <div class="card"><div class="lab">段落级 Hit Rate@1</div><div class="val" style="color:var(--brand)">{m['Hit@1_segment']*100:.1f}%</div><div class="hint">正确段落排第1 / 32条可答</div></div>
  <div class="card"><div class="lab">段落级 Hit Rate@2</div><div class="val" style="color:var(--green)">{m['Hit@2_segment']*100:.0f}%</div><div class="hint">前2名含正确段落</div></div>
  <div class="card"><div class="lab">MRR（段落）</div><div class="val">{m['MRR_segment']:.3f}</div><div class="hint">平均倒数排名</div></div>
  <div class="card"><div class="lab">无答案误召回率</div><div class="val" style="color:var(--red)">{m['noanswer_false_recall_rate']*100:.0f}%</div><div class="hint">3/3 条无答案问题仍返回文档</div></div>
</div>

<div class="section">
  <h2>关键发现</h2>
  <div class="find"><div class="ico">📏</div><div class="txt"><b>切分粒度过粗：</b>系统把 23 个 chunk 的 <code>test_knowledge_base.md</code> 实际切成了仅 <b>3 个大段</b>（每段约 1000–1200 字），并不是按 chunk_id 边界切分。每段打包了 6–9 个原本独立的 chunk：
    <b>段A</b>=HR+差旅住宿(hr_001~fin_001)｜<b>段B</b>=报销+IT(fin_002~it_004)｜<b>段C</b>=产品+客服+安全(prod_001~sec_002)。</div></div>
  <div class="find"><div class="ico">🔁</div><div class="txt"><b>全量返回、按相关性排序：</b>35 条问题全部返回了全部 3 段（A/B/C 各出现 35 次），只是顺序随问题变化。因此 Hit@2/Hit@3 ≡ 100% 不具区分度；<b>真正有区分度的是 Hit@1（正确段是否排第1）</b>，实测 93.75%。</div></div>
  <div class="find"><div class="ico">🎯</div><div class="txt"><b>2 条 Top-1 未命中：</b>q010「一线城市酒店报销」(期望段A含fin_001，实际段B报销类排第1)；q019「密码锁定」(期望段B含it_003，实际段C安全类排第1)。两条均为 rank2 命中，属语义相近导致的段间混淆。</div></div>
  <div class="find"><div class="ico">⚠️</div><div class="txt"><b>无答案问题无拒答能力：</b>q031~q033（涨薪/股票代码/餐厅晚餐）本应不召回，但系统 100% 仍返回全部段落，误召回率 100%——当前配置没有相关性阈值或拒答机制。</div></div>
</div>

<div class="charts">
  <div class="chartbox"><canvas id="c1"></canvas></div>
  <div class="chartbox"><canvas id="c2"></canvas></div>
</div>

<div class="section">
  <h2>建议</h2>
  <p>1. <b>调细分块</b>：按 <code>## chunk_id</code> 标题/段落切分为 23 块，让 chunk_id 级命中率真正可度量、召回更精准。</p>
  <p>2. <b>调小 Top-K</b>：当前 Top-K≥段总数导致全量返回；设为 3–5 并配合分块，Recall 才有区分度。</p>
  <p>3. <b>引入相关性阈值 / 拒答机制</b>：低于阈值的段落不返回，以降低无答案问题的误召回（当前 100%）。</p>
  <p>4. <b>可选 Reranker</b>：针对 q010/q019 这类段间混淆，加 rerank 可提升 Hit@1。</p>
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

<div class="foot">数据来源：results_raw.json · metrics.json · 由 WorkBuddy 自动测试生成</div>
</div>
<script>
const COLOR='#2563eb',GREEN='#16a34a',RED='#dc2626',AMBER='#d97706';
new Chart(document.getElementById('c1'),{{type:'bar',data:{{labels:['Hit@1','Hit@2','Hit@3','Recall@3'],datasets:[{{data:[{m['Hit@1_segment']*100},{m['Hit@2_segment']*100},{m['Hit@3_segment']*100},{m['Recall@3_segment']*100}],backgroundColor:[COLOR,GREEN,GREEN,GREEN],borderRadius:6}}]}},options:{{plugins:{{title:{{display:true,text:'段落级命中率指标 (%)',font:{{size:14}}}},legend:{{display:false}}}},scales:{{y:{{beginAtZero:true,max:105,ticks:{{callback:v=>v+'%'}}}}}}}}}});
new Chart(document.getElementById('c2'),{{type:'doughnut',data:{{labels:['Top1命中','Top1未命中(rank2+)'],datasets:[{{data:[30,2],backgroundColor:[GREEN,RED],borderWidth:0}}]}},options:{{plugins:{{title:{{display:true,text:'32条可答问题 Top-1 分布',font:{{size:14}}}},legend:{{position:'bottom'}}}},cutout:'62%'}}}});
</script>
</body></html>"""

pathlib.Path("知识库命中率测试报告.html").write_text(html,encoding="utf-8")
print("written 知识库命中率测试报告.html", len(html),"bytes")
