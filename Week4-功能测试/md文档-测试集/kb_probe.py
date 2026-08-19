# -*- coding: utf-8 -*-
"""探测 https://59.56.96.36:8080 知识库当前状态：
1) 列出所有 collection（知识库）；
2) 用 3 条代表性问题探测 KB 的检索返回结构（分块粒度）。
"""
import json, re, ssl, urllib.request

# 从 kb_test.py 读取 TOKEN / KB / MODEL
src = open(__file__).read() if False else None
def load_consts():
    for fname in ("kb_test.py", "kb_runner.py"):
        try:
            text = open(fname, encoding="utf-8").read()
            t = re.search(r'^TOKEN\s*=\s*"([^"]+)"', text, re.M)
            k = re.search(r'^KB\s*=\s*"([^"]+)"', text, re.M)
            m = re.search(r'^MODEL\s*=\s*"([^"]+)"', text, re.M)
            if t and k:
                return t.group(1), k.group(1), (m.group(1) if m else None)
        except FileNotFoundError:
            continue
    raise SystemExit("cannot find token")

TOKEN, KB, MODEL = load_consts()
BASE = "https://59.56.96.36:8080"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
CHUNK_RE = re.compile(r"\b([a-z]{2,5}_\d{3})\b")

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            return r.status, r.read().decode()
    except Exception as e:
        return None, str(e)

def chat_sources(q, timeout=150):
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

print("KB =", KB, "| MODEL =", MODEL)
print("=" * 70)
# 1) 枚举知识库集合
for ep in ["/api/v1/collections", "/api/v1/collections/list", "/api/collections", "/api/v1/documents/list"]:
    s, body = get(BASE + ep)
    print(f"[{s}] {ep}: {body[:600]}")
    print("-" * 70)

# 2) 探测检索返回结构
for q in ["员工转正后有多少天年假？",
          "API每分钟最多能调用多少次？超限返回什么？",
          "公司明年会不会涨薪？"]:
    try:
        s = chat_sources(q)
    except Exception as e:
        print("ERR query:", q, "->", e)
        continue
    print("\n##### QUERY:", q)
    if not s:
        print("  (no sources)")
        continue
    print("num sources:", len(s))
    for si, src in enumerate(s):
        docs = src.get("document", [])
        if isinstance(docs, str):
            docs = [docs]
        print(f"  -- source[{si}] source={src.get('source')} #docs={len(docs)}")
        for di, d in enumerate(docs):
            txt = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
            ids = CHUNK_RE.findall(txt)
            print(f"     doc[{di}] len={len(txt)} ids={ids}")
            print(f"        head={txt[:60]!r}")
            print(f"        tail={txt[-60:]!r}")
