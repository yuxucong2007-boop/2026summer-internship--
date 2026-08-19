# -*- coding: utf-8 -*-
import json, re, subprocess, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = open('token.txt').read().strip()
URL = 'https://59.56.96.36:8080/api/v1/chat/completions'
KID = '5e4a239c-2aae-4702-b6d4-2e292943fb81'
MODEL = 'kpc.glm-5.2'

DOC_KEY = {'员工手册 v2.2.pdf': '手册', '纪律惩罚规定.pdf': '纪律', '绩效管理办法V1.1.pdf': '绩效', '薪酬福利制度V3.0.pdf': '薪酬'}

# ---------- 文本规范化 ----------
def norm(s):
    if not s:
        return ''
    s = re.sub(r'\s+', '', s)
    table = str.maketrans({'，': ',', '。': '.', '；': ';', '：': ':', '（': '(', '）': ')',
                           '“': '"', '”': '"', '、': ',', '！': '!', '？': '?', '【': '[', '】': ']',
                           '－': '-', '—': '-', '≥': '>=', '≤': '<=', '《': '<', '》': '>'})
    return s.translate(table)

# 每页签名（规范化后前 45 字符）
PDF = json.load(open('pdf_pages.json', encoding='utf-8'))
PAGE_SIG = {}
for fn, d in PDF.items():
    key = DOC_KEY[fn]
    for i, t in enumerate(d['pages'], 1):
        PAGE_SIG.setdefault(key, {})[i] = norm(t)[:45]

def chunk_pages(doc_key, start_page, chunk_text):
    """判定一个检索块覆盖的页码集合"""
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

# ---------- API 调用 ----------
def call_once(q):
    body = {'model': MODEL, 'messages': [{'role': 'user', 'content': q}],
            'files': [{'type': 'collection', 'id': KID}], 'stream': True}
    req = json.dumps(body, ensure_ascii=False)
    r = subprocess.run(['curl', '-sk', '-m', '180', '--noproxy', '*',
                        '-H', 'Authorization: Bearer ' + TOKEN,
                        '-H', 'Content-Type: application/json',
                        '-d', req, URL],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise RuntimeError('curl rc=%d %s' % (r.returncode, r.stderr[:120]))
    sources = None
    answer_parts = []
    chat_id = None
    for line in r.stdout.split('\n'):
        line = line.strip()
        if not line.startswith('data: '):
            continue
        p = line[6:]
        if p == '[DONE]':
            continue
        try:
            obj = json.loads(p)
        except Exception:
            continue
        if obj.get('sources'):
            sources = obj['sources']
        if obj.get('chat_id'):
            chat_id = obj['chat_id']
        for ch in obj.get('choices', []):
            delta = ch.get('delta') or {}
            c = delta.get('content')
            if c:
                answer_parts.append(c)
    return sources, ''.join(answer_parts), chat_id

def run_question(item):
    q = item['question']
    for attempt in range(3):
        try:
            sources, answer, chat_id = call_once(q)
            return {'id': item['id'], 'question': q, 'type': item.get('type'),
                    'document': item.get('document'), 'relevant_pages': item.get('relevant_pages', []),
                    'answer_text': answer, 'chat_id': chat_id, 'sources': sources, 'ok': True}
        except Exception as e:
            if attempt == 2:
                return {'id': item['id'], 'question': q, 'type': item.get('type'),
                        'document': item.get('document'), 'relevant_pages': item.get('relevant_pages', []),
                        'answer_text': '', 'chat_id': None, 'sources': None, 'ok': False, 'error': str(e)}
            time.sleep(2 + attempt * 3)
    return None

def main():
    path = r'C:/Users/Yu/Desktop/靠谱云公司规章制度/靠谱云规章制度-命中率召回率测试集.jsonl'
    items = [json.loads(l) for l in open(path, encoding='utf-8-sig') if l.strip()]
    results = []
    lock = threading.Lock()
    done = 0
    def worker(item):
        nonlocal done
        r = run_question(item)
        with lock:
            done += 1
            print('[%3d/%d] %s %s' % (done, len(items), item['id'], 'OK' if r and r.get('ok') else 'FAIL'), flush=True)
        return r
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = [ex.submit(worker, it) for it in items]
        for f in as_completed(futs):
            r = f.result()
            if r:
                results.append(r)
    results.sort(key=lambda r: r['id'])
    with open('results_raw.jsonl', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('=== 完成，%d 条写入 results_raw.jsonl' % len(results))

if __name__ == '__main__':
    main()
