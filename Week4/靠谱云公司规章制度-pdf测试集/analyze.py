# -*- coding: utf-8 -*-
"""分析 results_raw.jsonl，计算 Hit@k / Recall / 干扰题指标，生成报告"""
import json, re

DOC_KEY = {'员工手册 v2.2.pdf': '手册', '纪律惩罚规定.pdf': '纪律', '绩效管理办法V1.1.pdf': '绩效', '薪酬福利制度V3.0.pdf': '薪酬'}
MANUAL_DISCIPLINE_PAGES = set(range(29, 35))  # 手册第7章纪律处罚条例所在页

def norm(s):
    if not s:
        return ''
    s = re.sub(r'\s+', '', s)
    table = str.maketrans({'，': ',', '。': '.', '；': ';', '：': ':', '（': '(', '）': ')',
                           '“': '"', '”': '"', '、': ',', '！': '!', '？': '?', '【': '[', '】': ']',
                           '－': '-', '—': '-', '≥': '>=', '≤': '<=', '《': '<', '》': '>'})
    return s.translate(table)

PDF = json.load(open('pdf_pages.json', encoding='utf-8'))
PAGE_SIG = {}
for fn, d in PDF.items():
    key = DOC_KEY[fn]
    for i, t in enumerate(d['pages'], 1):
        PAGE_SIG.setdefault(key, {})[i] = norm(t)[:45]

def chunk_pages(doc_key, start_page, chunk_text):
    pages = set()
    if start_page:
        pages.add(start_page)
    ntext = norm(chunk_text)
    if doc_key == '手册':
        for m in re.finditer(r'福建靠谱云算力技术有限公司\n(\d+)\n', chunk_text):
            p = int(m.group(1))
            if 1 <= p <= 35:
                pages.add(p)
    elif doc_key == '绩效':
        for m in re.finditer(r'福建靠谱云算力技术有限公司\n(\d+)\s*/\s*6\n', chunk_text):
            p = int(m.group(1))
            if 1 <= p <= 6:
                pages.add(p)
    for p, sig in PAGE_SIG.get(doc_key, {}).items():
        if sig and sig in ntext:
            pages.add(p)
    return pages

def parse_rel(refs):
    out = set()
    for r in refs:
        m = re.match(r'(.+)-P(\d+)', r)
        if m:
            out.add((m.group(1), int(m.group(2))))
    return out

def main():
    results = [json.loads(l) for l in open('results_raw.jsonl', encoding='utf-8') if l.strip()]
    factual = [r for r in results if r.get('type') == 'factual']
    neg = [r for r in results if r.get('type') == 'negative']

    rows = []
    for r in factual:
        rel = parse_rel(r.get('relevant_pages', []))
        chunks = []
        if r.get('sources'):
            for s in r['sources']:
                docs = s.get('document', []) or []
                metas = s.get('metadata', []) or []
                dists = s.get('distances', []) or []
                for i, d in enumerate(docs):
                    m = metas[i] if i < len(metas) else {}
                    name = m.get('name', '')
                    dk = DOC_KEY.get(name)
                    pl = m.get('page_label')
                    try:
                        sp = int(pl) if pl is not None else None
                    except Exception:
                        sp = None
                    pgs = chunk_pages(dk, sp, d) if dk else set()
                    relpages = set((dk, p) for p in pgs) if dk else set()
                    chunks.append({'doc': dk, 'file': name, 'page_label': sp, 'pages': sorted(pgs),
                                   'relpages': relpages,
                                   'score': dists[i] if i < len(dists) else None, 'text': d})
        hit = {}
        rec = {}
        seen = set()
        n = len(chunks)
        for k in range(1, n + 1):
            seen |= chunks[k - 1]['relpages']
            hit[k] = 1 if (seen & rel) else 0
            rec[k] = len(seen & rel) / len(rel) if rel else 0.0
        soft = 0
        if rel and all(dk == '纪律' for dk, _ in rel):
            if any(c['doc'] == '手册' and (set(c['pages']) & MANUAL_DISCIPLINE_PAGES) for c in chunks):
                soft = 1
        rows.append({'id': r['id'], 'question': r['question'], 'document': r.get('document'),
                     'rel': sorted(rel), 'n_chunks': n,
                     'chunks': [{k: c[k] for k in ('doc', 'file', 'page_label', 'pages', 'score')} for c in chunks],
                     'hit': hit, 'rec': rec, 'soft': soft, 'answer': r.get('answer_text', '')})

    K = max((len(r['hit']) for r in rows), default=0)

    def hitval(r, k):
        if k in r['hit']:
            return r['hit'][k]
        if r['hit']:
            return r['hit'][max(r['hit'])]
        return 0

    def recval(r, k):
        if k in r['rec']:
            return r['rec'][k]
        if r['rec']:
            return r['rec'][max(r['rec'])]
        return 0.0

    print('===== 命中率 Hit@k (严格，按测试集相关页) =====')
    for k in range(1, K + 1):
        h = sum(1 for r in rows if hitval(r, k))
        print('Hit@%d = %d/%d = %.2f%%' % (k, h, len(rows), 100 * h / len(rows)))
    print('\n===== 命中率 Hit@k (宽松：纪律题认可手册P29-34) =====')
    for k in range(1, K + 1):
        h = sum(1 for r in rows if (hitval(r, k) or r['soft']))
        print('Hit@%d = %d/%d = %.2f%%' % (k, h, len(rows), 100 * h / len(rows)))
    print('\n===== 召回率 Recall@k (严格) =====')
    for k in range(1, K + 1):
        rk = sum(recval(r, k) for r in rows) / len(rows)
        print('Recall@%d = %.4f' % (k, rk))

    print('\n===== 各文档命中统计 (Hit@1, 严格) =====')
    from collections import Counter
    doccnt = Counter()
    dochit = Counter()
    for r in rows:
        dk = r['document'].replace('.pdf', '')
        doccnt[dk] += 1
        if hitval(r, 1):
            dochit[dk] += 1
    for dk in doccnt:
        print('%s: Hit@1 = %d/%d' % (dk, dochit[dk], doccnt[dk]))

    print('\n===== 干扰题 (5道) =====')
    for r in neg:
        nchunks = 0
        if r.get('sources'):
            for s in r['sources']:
                nchunks += len(s.get('document', []) or [])
        ans = (r.get('answer_text') or '').strip().replace('\n', ' ')
        print('%s | 检索块数=%d | 回答: %s' % (r['id'], nchunks, ans[:90]))
    neg_retr = 0
    for r in neg:
        if r.get('sources'):
            for s in r['sources']:
                if len(s.get('document', []) or []) > 0:
                    neg_retr += 1
                    break
    print('误召回（检索到块）: %d/5' % neg_retr)

    with open('analysis_rows.json', 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print('\n已保存 analysis_rows.json')

if __name__ == '__main__':
    main()
