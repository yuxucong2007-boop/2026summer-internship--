# -*- coding: utf-8 -*-
import json, sys, re, urllib.request, ssl

BASE = "https://59.56.96.36:8080"
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Imp3dC1zaWduaW5nLXYxIiwidHlwIjoiYXQrand0In0.eyJzdWIiOiIxIiwiZXhwIjoxNzg3MTA0MDY5LCJpYXQiOjE3ODcwMTc2NjksImp0aSI6IjNlYjhhY2IwLTkwMjYtNDM1NS1hYzljLWY0YmJiZDMxOGI1ZCIsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJyb2xlcyI6WyJhZG1pbiIsInN1cGVyYWRtaW4iXSwiY2xpZW50X2lkIjoiYXJnbyJ9.BJWXhpZRLMGRXvZbz3zubrpCd-Q3Jabel5B1GMqT8gBR1zKhjPs4fDyrPpydEwI3dEuoutpg8-nq-rRDI9j6jzg6k1w99NeuLm3BSFoIdSAK4JS9-PVvYSnuP1KfoCu6pOcV6wTQrSay7KJbEFEc08zOjDUq6AeO4grc8t7-Bvx7V8rX9ernkc_cSUCn_C9AUWzrd_MU0rguuqny8irMN_fTlMqSG_XOWOngGOvxyME-PY5fHpTrvx0nP3zfbB2oQO3xwYltMQHwLhZXdaW8YpwWv1qYVhuXRdJ7VaD1xIkeeLuL4DCBcGimeSlZk8zzmopCXgODACn49Cn7BF-R_w"
KB = "9e5dbbec-6c08-47f3-b2bb-59a3cc8cfed2"
MODEL = "kpc.deepseek-v4-pro"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CHUNK_RE = re.compile(r"chunk_id[:：]\s*`?([a-z]+_\d+)`?", re.IGNORECASE)
HEADER_RE = re.compile(r"^##\s*([A-Z]+-\d{3})\s", re.MULTILINE)

def run_query(q, get_answer=False, timeout=120):
    body = {
        "model": MODEL,
        "stream": True,
        "messages": [{"role": "user", "content": q}],
        "files": [{"type": "collection", "id": KB}],
        "metadata": {},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE + "/api/v1/chat/completions",
        data=data, method="POST",
        headers={"Authorization": "Bearer " + TOKEN,
                 "Content-Type": "application/json",
                 "Accept": "text/event-stream"})
    sources = None
    answer = []
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        f = resp
        buf = b""
        got_sources = False
        for raw in f:
            buf += raw
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                if line.startswith(b"data:"):
                    payload = line[5:].strip()
                    if payload == b"[DONE]":
                        continue
                    try:
                        obj = json.loads(payload)
                    except Exception:
                        continue
                    if "sources" in obj and not got_sources:
                        sources = obj["sources"]
                        got_sources = True
                        if not get_answer:
                            # we have what we need; close to save time
                            try: resp.close()
                            except Exception: pass
                            return sources, ""
                    # collect answer content
                    if get_answer:
                        try:
                            for ch in obj.get("choices", []):
                                c = ch.get("delta", {}).get("content")
                                if c: answer.append(c)
                        except Exception:
                            pass
    except Exception as e:
        return sources, ("ERR:" + str(e))
    return sources, "".join(answer)


def parse_chunk_ids_from_sources(sources):
    """Return ordered list of (source_idx, [chunk_ids]) per source, and flat ordered set."""
    per_source = []
    flat_ordered = []
    seen = set()
    if not sources:
        return per_source, flat_ordered
    for si, s in enumerate(sources):
        docs = s.get("document", [])
        if isinstance(docs, str):
            docs = [docs]
        found = []
        for d in docs:
            txt = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
            # find chunk_ids and headers in this text segment
            ids = CHUNK_RE.findall(txt)
            if not ids:
                ids = [h.lower().replace("-", "_") for h in HEADER_RE.findall(txt)]
            for cid in ids:
                if cid and cid not in found:
                    found.append(cid)
                if cid and cid not in seen:
                    seen.add(cid)
                    flat_ordered.append(cid)
        per_source.append({"source_index": si, "source": s.get("source"), "chunk_ids": found})
    return per_source, flat_ordered


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "员工转正后有多少天年假？"
    want_answer = "--answer" in sys.argv
    sources, answer = run_query(q, get_answer=want_answer)
    print("=== QUERY:", q)
    print("=== num sources:", len(sources) if sources else 0)
    per, flat = parse_chunk_ids_from_sources(sources)
    print("=== per-source chunk_ids:")
    for p in per:
        print("  src", p["source_index"], p["source"], "->", p["chunk_ids"])
    print("=== flat ordered retrieved chunk_ids:", flat)
    if answer:
        print("=== answer head:", answer[:300])
