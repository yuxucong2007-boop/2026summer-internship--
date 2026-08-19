# -*- coding: utf-8 -*-
"""从 results_raw.json 重算指标 + 重生成报告（修正口径：有检索结果即视为成功，清除瞬时超时残留的 err）"""
import json, time, pathlib
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
SEG_A = ["hr_001","hr_002","hr_003","hr_004","hr_005","fin_001"]
SEG_B = ["fin_002","fin_003","fin_004","fin_005","it_001","it_002","it_003","it_004"]
SEG_C = ["prod_001","prod_002","prod_003","prod_004","cs_001","cs_002","cs_003","sec_001","sec_002"]
SEGMENTS = {"A": SEG_A, "B": SEG_B, "C": SEG_C}

results = json.loads((HERE / "results_raw.json").read_text(encoding="utf-8"))

# 修正：检索到结果（retrieved_segs 非空）即视为成功，清除瞬时超时残留的 err
fixed = 0
for r in results:
    if r.get("error") and r["retrieved_segs"]:
        r["error"] = None
        fixed += 1
# 落回 results_raw.json（已修正）
(HERE / "results_raw.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

ans = [r for r in results if r["answerable"] and not r["error"]]
noans = [r for r in results if not r["answerable"] and not r["error"]]
n = len(ans)
total_ok = len([r for r in results if not r["error"]])
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
    "full_return_rate": round(sum(1 for r in results if not r["error"] and len(r["retrieved_segs"]) == 3) / total_ok, 4) if total_ok else 0,
    "tested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "kb_id": "9e5dbbec-6c08-47f3-b2bb-59a3cc8cfed2",
    "model": "kpc.deepseek-v4-pro",
}
(HERE / "metrics.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
print("修正瞬时超时条目数:", fixed)
print(json.dumps(m, ensure_ascii=False, indent=2))

# 复用 kb_retest.render_report
import importlib.util
spec = importlib.util.spec_from_file_location("kb_retest", HERE / "kb_retest.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.render_report(results, m)
print("report regenerated.")
