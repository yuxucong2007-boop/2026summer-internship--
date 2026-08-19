# -*- coding: utf-8 -*-
"""生成测试报告 report.md 与明细 details.csv"""
import json, re, csv
from collections import Counter

DOC_KEY = {'员工手册 v2.2.pdf': '手册', '纪律惩罚规定.pdf': '纪律', '绩效管理办法V1.1.pdf': '绩效', '薪酬福利制度V3.0.pdf': '薪酬'}
DOC_CN = {'手册': '员工手册 v2.2.pdf', '纪律': '纪律惩罚规定.pdf', '绩效': '绩效管理办法V1.1.pdf', '薪酬': '薪酬福利制度V3.0.pdf'}

rows = json.load(open('analysis_rows.json', encoding='utf-8'))
results = [json.loads(l) for l in open('results_raw.jsonl', encoding='utf-8') if l.strip()]
neg = [r for r in results if r.get('type') == 'negative']
factual = [r for r in results if r.get('type') == 'factual']

# ---------- 汇总指标 ----------
K = max((len(r['hit']) for r in rows), default=0)

def hitval(r, k):
    key = str(k)
    if key in r['hit']:
        return r['hit'][key]
    if r['hit']:
        return r['hit'][max(r['hit'])]
    return 0

def recval(r, k):
    key = str(k)
    if key in r['rec']:
        return r['rec'][key]
    if r['rec']:
        return r['rec'][max(r['rec'])]
    return 0.0

lines = []
lines.append('# 靠谱云规章制度知识库 · RAG 命中率/召回率测试报告\n')
lines.append('## 一、测试概况\n')
lines.append('| 项目 | 值 |')
lines.append('| --- | --- |')
lines.append('| 测试系统 | Kmind（Open WebUI 内核）`https://59.56.96.36:8080` |')
lines.append('| 知识库 | 靠谱云公司规章制度（4 份 PDF + 1 份 docx，共 53 页） |')
lines.append('| 检索模型 | 与库内一致（embedding 配置：`openai/text-embedding-v4`） |')
lines.append('| 生成模型 | `kpc.glm-5.2`（glm-5.2） |')
lines.append('| 测试集 | 114 题 = 109 可答题 + 5 干扰题（`靠谱云规章制度-命中率召回率测试集.jsonl`） |')
lines.append('| 检索方式 | 每条问题单独发起对话，附加知识库 collection；取流式响应 `sources` 中返回的 top-k 检索块（服务端返回 k=3） |')
lines.append('| 块→页码映射 | 块元数据 `page_label`（1-based 物理页码）+ 页头页码模式 + 与本地 PDF 逐页文本签名比对三重判定 |')
lines.append('| 测试时间 | 2026-08-19 09:55 ~ 10:08（GMT+8） |')
lines.append('')

lines.append('## 二、核心指标（109 道可答题）\n')
lines.append('### 2.1 命中率 Hit@k（严格：按测试集 `relevant_pages` 判定）\n')
lines.append('| 指标 | 命中数/总数 | 命中率 |')
lines.append('| --- | --- | --- |')
for k in range(1, K + 1):
    h = sum(1 for r in rows if hitval(r, k))
    lines.append('| Hit@%d | %d/%d | **%.2f%%** |' % (k, h, len(rows), 100 * h / len(rows)))
lines.append('')
lines.append('### 2.2 召回率 Recall@k（严格）\n')
lines.append('| 指标 | 值 |')
lines.append('| --- | --- |')
for k in range(1, K + 1):
    rk = sum(recval(r, k) for r in rows) / len(rows)
    lines.append('| Recall@%d | %.4f |' % (k, rk))
lines.append('')
lines.append('> 说明：服务端每次检索固定返回 top-3，故最多计算到 Hit@3。Recall 与 Hit 数值相近，是因为大部分题目相关页只有 1 页。\n')

lines.append('### 2.3 宽松命中（纪律题认可《员工手册》第 7 章 P29-34）\n')
lines.append('| 指标 | 命中率 |')
lines.append('| --- | --- |')
for k in range(1, K + 1):
    h = sum(1 for r in rows if (hitval(r, k) or r['soft']))
    lines.append('| 宽松Hit@%d | **%.2f%%**（%d/109） |' % (k, 100 * h / len(rows), h))
lines.append('')

# ---------- 分文档 ----------
lines.append('## 三、分文档表现（Hit@1，严格）\n')
lines.append('| 文档 | 题数 | Hit@1 | Hit@1率 |')
lines.append('| --- | --- | --- | --- |')
doccnt = Counter()
dochit = Counter()
for r in rows:
    dk = r['document'].replace('.pdf', '')
    doccnt[dk] += 1
    if hitval(r, 1):
        dochit[dk] += 1
for dk in ['员工手册 v2.2', '纪律惩罚规定', '绩效管理办法V1.1', '薪酬福利制度V3.0']:
    lines.append('| %s | %d | %d | %.1f%% |' % (dk, doccnt[dk], dochit[dk], 100 * dochit[dk] / doccnt[dk]))
lines.append('')
lines.append('薪酬福利制度（16 题）Hit@1 最低（%.1f%%），且是回答错误的重灾区（见 4.3 典型案例）。\n' % (100 * dochit['薪酬福利制度V3.0'] / doccnt['薪酬福利制度V3.0']))

# ---------- 干扰题 ----------
lines.append('## 四、干扰题（5 道，知识库外问题）\n')
lines.append('| 题目 | 检索到块 | 是否拒答 | 回答摘要 |')
lines.append('| --- | --- | --- | --- |')
neg_retr = 0
for r in neg:
    nchunks = sum(len(s.get('document', []) or []) for s in (r.get('sources') or []))
    if nchunks > 0:
        neg_retr += 1
    ans = (r.get('answer_text') or '').strip().replace('\n', ' ')
    refused = any(w in ans for w in ['无法回答', '不能回答', '知识库中未', '知识库中没有', '不在知识库', '未提供相关'])
    qid = r['id']
    qshort = (r['question'] or '')[:22]
    lines.append('| %s %s | %d | %s | %s |' % (qid, qshort, nchunks, '是' if refused else '否', ans[:46]))
lines.append('')
lines.append('**结论：5/5 干扰题均被检索出无关块（误召回 100%），且模型 5/5 均未拒答**——模型识别出问题与知识库无关，但仍然调用自身知识回答（"我基于自己的知识来回答"）。若业务要求"知识库外问题必须拒答"，此行为需通过系统提示词约束。\n')

# ---------- 未命中清单 ----------
lines.append('## 五、Hit@1 未命中清单（严格口径，%d 题）\n' % sum(1 for r in rows if not hitval(r, 1)))
lines.append('| 题号 | 问题 | 相关页 | 检索到的 top-3（文件-页，得分） |')
lines.append('| --- | --- | --- | --- |')
miss = [r for r in rows if not hitval(r, 1)]
for r in miss:
    relstr = '、'.join('%s-P%02d' % (dk, p) for dk, p in sorted(r['rel']))
    got = []
    for c in r['chunks']:
        nm = {'手册': '手册', '纪律': '纪律', '绩效': '绩效', '薪酬': '薪酬'}.get(c['doc'], c['file'])
        got.append('%s-P%02d(%.2f)' % (nm, c['page_label'] or 0, c['score'] or 0))
    gotstr = '；'.join(got) if got else '（无检索块）'
    lines.append('| %s | %s | %s | %s |' % (r['id'], r['question'][:24], relstr, gotstr))
lines.append('')

# ---------- 回答质量粗检 ----------
noinfo_kw = ['未包含', '未提及', '没有提供', '没有找到', '未找到', '无相关内容', '没有相关内容',
             '未检索到', '不包含', '未涉及', '并未包含', '没有该', '未查询到', '资料中没有']
bad = [r for r in factual if any(k in (r.get('answer_text') or '') for k in noinfo_kw)]
lines.append('## 六、典型案例与问题发现\n')
lines.append('### 6.1 检索完全落空（sources 为空）\n')
lines.append('- **Q032「春节放假几天？」**：检索返回 0 个块（`sources` 为空，低于相似度阈值），模型转而用自身知识回答。知识库中手册-P15 确有"春节放假4天"内容。\n')
lines.append('### 6.2 检索到无关页导致模型明确答"资料中未包含"（%d 题）\n' % len(bad))
lines.append('这些题知识库中均有答案，但 top-3 未召回正确页，模型如实回答"未包含"（可视为检索失败的直接后果）：\n')
lines.append('| 题号 | 问题 | 正确出处 | 模型回答（节选） |')
lines.append('| --- | --- | --- | --- |')
relmap = {r['id']: r for r in rows}
for r in bad:
    rid = r['id']
    rel = relmap.get(rid)
    relstr = '、'.join('%s-P%02d' % (dk, p) for dk, p in sorted(rel['rel'])) if rel else '?'
    lines.append('| %s | %s | %s | %s |' % (rid, r['question'][:22], relstr, (r['answer_text'] or '').replace('\n', ' ')[:60]))
lines.append('')
lines.append('### 6.3 薪酬类题目检索不稳定（同一问题重复提问结果不同）\n')
lines.append('- **Q106「加班餐补的标准是多少？」**：正确答案 18 元/次（薪酬-P05）。正式评测中 top-3 全部命中员工手册（补卡/加班相关页），薪酬 P05 未被召回，模型据此回答"资料中未包含加班餐补标准"，**答错**。但此前单独探测时，同一问题能召回薪酬-P05。说明**检索存在抖动**，或 top-3 被高相似度的其他文档挤掉。\n')
lines.append('- 薪酬 16 题中 Hit@1 仅 %.1f%%，且其中多题模型给出的回答与其检索内容不符（检索到薪酬页却仍答错，或未检索到薪酬页而答错）。\n' % (100 * dochit['薪酬福利制度V3.0'] / doccnt['薪酬福利制度V3.0']))
lines.append('### 6.4 检索到正确页但回答错误的案例\n')
lines.append('（见明细 CSV `answer` 列，人工核对。典型模式：模型对数字/金额类事实偶有改写错误。）\n')
lines.append('### 6.5 手册目录页（P02）高频误召回\n')
lines.append('多道题（如 Q002、Q012、Q106 等）的 top-3 中包含手册目录页（P02），目录文本与各章节关键词高度重合，挤占检索名额。建议在切块时剔除目录/封面页，或提高块级去重阈值。\n')
lines.append('### 6.6 干扰题行为\n')
lines.append('如第四节：误召回 100%、拒答 0%。系统未配置"仅依据知识库回答"的约束。\n')

lines.append('\n---\n')
lines.append('## 附：评测方法备注\n')
lines.append('1. 每次提问为独立新对话（无历史），与用户在网页端新建会话提问等价；附加知识库 collection。\n')
lines.append('2. 检索块按返回顺序视为排名（对应 `distances` 得分排序）。\n')
lines.append('3. 块→页码：优先取元数据 `page_label`；手册/绩效额外用页头页码模式识别跨页块；并用本地 PDF 逐页签名比对兜底。\n')
lines.append('4. 员工手册第 7 章（P29-34）与《纪律惩罚规定》内容重叠，纪律题按测试集建议做了"宽松命中"口径（2.3 节）。\n')
lines.append('5. 本次测试使用的 120 个临时会话已清理，未影响原有会话。\n')

report = '\n'.join(lines)
open('report.md', 'w', encoding='utf-8').write(report)
print(report[:1500])
print('...\nreport.md 已生成')

# ---------- 明细 CSV ----------
with open('details.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', '问题', '文档', '相关页', 'Hit@1', 'Hit@2', 'Hit@3', '检索top1(文件-页,得分)', '检索top2', '检索top3', '模型回答'])
    for r in rows:
        relstr = '、'.join('%s-P%02d' % (dk, p) for dk, p in sorted(r['rel']))
        cells = [r['id'], r['question'], r['document'], relstr]
        cells += [hitval(r, k) for k in (1, 2, 3)]
        for i in range(3):
            if i < len(r['chunks']):
                c = r['chunks'][i]
                cells.append('%s-P%02d(%.2f)' % (c['doc'], c['page_label'] or 0, c['score'] or 0))
            else:
                cells.append('')
        cells.append(r['answer'].replace('\n', ' '))
        w.writerow(cells)
print('details.csv 已生成')
