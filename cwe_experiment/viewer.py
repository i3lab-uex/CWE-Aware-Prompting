"""Loopback-only PyArrow result API and dependency-free viewer."""

from __future__ import annotations

from collections import defaultdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


INDEX_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CWE Prompting Results</title><link rel="stylesheet" href="/app.css"></head>
<body><header><div><p class="eyebrow">CWE abstraction experiment</p><h1>Generation results</h1></div><p id="status" role="status">Loading…</p></header>
<main>
  <section id="cards" class="cards" aria-label="Summary"></section>
  <section class="panel"><h2>Comparison by prompt level</h2><div id="levels"></div></section>
  <section class="panel"><h2>Explore generations</h2>
    <form id="filters" class="filters">
      <label>Task<input name="task" placeholder="Task ID"></label>
      <label>Target CWE<select name="cwe"><option value="">All</option></select></label>
      <label>Prompt level<select name="level"><option value="">All</option></select></label>
      <label>Model<select name="model"><option value="">All</option></select></label>
      <label>Functional<select name="functional"><option value="">All</option><option value="pass">All tests pass</option><option value="fail">Tests fail</option><option value="not-run">Not run</option></select></label>
      <label>Analyzer<select name="analyzer"><option value="">All</option><option value="findings">Has findings</option><option value="none">No findings</option><option value="error">Analyzer error</option></select></label>
      <button type="submit">Apply</button>
    </form>
    <div class="table-wrap"><table><thead><tr><th>Task</th><th>Target</th><th>Level</th><th>Prompt CWE</th><th>Syntax</th><th>Tests</th><th>Analysis</th><th></th></tr></thead><tbody id="rows"></tbody></table></div>
    <nav class="pagination" aria-label="Results pages"><button id="previous">Previous</button><span id="page"></span><button id="next">Next</button></nav>
  </section>
</main>
<aside id="detail" aria-label="Generation detail" aria-hidden="true"><button id="close" aria-label="Close detail">×</button><div id="detail-content"></div></aside><div id="scrim"></div>
<script src="/app.js"></script></body></html>"""


APP_CSS = """:root{color-scheme:light;--ink:#17211c;--muted:#66726b;--paper:#f4f5ef;--card:#fff;--line:#dce2dc;--green:#19734b;--amber:#a25b08;--red:#a33333;--blue:#315c89}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,sans-serif}header,main{max-width:1280px;margin:auto}header{padding:2.5rem 1.5rem 1rem;display:flex;justify-content:space-between;align-items:end}h1{font-size:clamp(2rem,5vw,4rem);line-height:1;margin:.15rem 0}.eyebrow{margin:0;text-transform:uppercase;letter-spacing:.12em;color:var(--green);font-weight:700}main{padding:1rem 1.5rem 4rem}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}.card,.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 5px 20px #26382b0a}.card{padding:1.2rem}.card strong{display:block;font-size:2rem}.card span{color:var(--muted)}.panel{padding:1.25rem;margin-top:1rem}.level-row{display:grid;grid-template-columns:110px 1fr 110px;gap:1rem;align-items:center;margin:.65rem 0}.bar{height:12px;background:#e7ebe7;border-radius:99px;overflow:hidden}.bar i{display:block;height:100%;background:var(--green);border-radius:inherit}.filters{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr)) auto;gap:.75rem;align-items:end;margin-bottom:1.2rem}.filters label{font-size:.8rem;color:var(--muted)}input,select,button{width:100%;padding:.65rem;border:1px solid #bdc8c0;border-radius:8px;background:#fff;color:var(--ink)}button{cursor:pointer;font-weight:650}button:hover{border-color:var(--green)}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;min-width:800px}th,td{text-align:left;padding:.75rem;border-bottom:1px solid var(--line)}th{font-size:.76rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.badge{display:inline-block;border-radius:99px;padding:.16rem .48rem;font-size:.76rem;background:#edf0ed}.ok{color:var(--green);background:#e0f3e9}.warn{color:var(--amber);background:#fff0d9}.error{color:var(--red);background:#fbe4e4}.info{color:var(--blue);background:#e6eef7}.pagination{display:flex;justify-content:center;align-items:center;gap:1rem;margin-top:1rem}.pagination button{width:auto}aside{position:fixed;z-index:3;right:0;top:0;height:100%;width:min(760px,94vw);background:#fff;padding:1.5rem;overflow:auto;transform:translateX(105%);transition:transform .2s;box-shadow:-20px 0 50px #0002}aside.open{transform:none}#close{position:sticky;top:0;float:right;width:44px;font-size:1.5rem}#scrim{display:none;position:fixed;inset:0;background:#13201888;z-index:2}#scrim.open{display:block}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#17211c;color:#eef5f0;padding:1rem;border-radius:9px;max-height:480px;overflow:auto}.finding{border-left:4px solid var(--amber);padding:.6rem .8rem;background:#fff8ec;margin:.5rem 0}.empty{color:var(--muted);font-style:italic}@media(max-width:900px){.cards{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(2,1fr)}header{align-items:start;flex-direction:column}.level-row{grid-template-columns:80px 1fr 80px}}@media(max-width:520px){.cards,.filters{grid-template-columns:1fr}.card strong{font-size:1.6rem}main,header{padding-left:.8rem;padding-right:.8rem}}"""


APP_JS = r"""let page=1,lastPage=1;const $=s=>document.querySelector(s);const esc=v=>String(v??'');
function badge(text,kind=''){const s=document.createElement('span');s.className='badge '+kind;s.textContent=text;return s}
async function json(url){const r=await fetch(url);if(!r.ok)throw new Error(await r.text());return r.json()}
function option(select,value){const o=document.createElement('option');o.value=value;o.textContent=value;select.append(o)}
async function loadMeta(){const m=await json('/api/meta');$('#cards').replaceChildren(...[
 ['Generations',m.total],['Valid Python',m.syntax_rate+'%'],['All tests pass',m.pass_rate+'%'],['With CWE findings',m.finding_rate+'%']
].map(([label,value])=>{const d=document.createElement('div');d.className='card';const strong=document.createElement('strong');strong.textContent=value;const span=document.createElement('span');span.textContent=label;d.append(strong,span);return d}));
 const levels=$('#levels');levels.replaceChildren(...m.by_level.map(x=>{const d=document.createElement('div');d.className='level-row';const name=document.createElement('strong');name.textContent=x.level;const bar=document.createElement('div');bar.className='bar';const fill=document.createElement('i');fill.style.width=x.pass_rate+'%';bar.append(fill);const rate=document.createElement('span');rate.textContent=x.pass_rate+'% pass';d.append(name,bar,rate);return d}));
 m.filters.cwes.forEach(v=>option(document.querySelector('[name=cwe]'),v));m.filters.levels.forEach(v=>option(document.querySelector('[name=level]'),v));m.filters.models.forEach(v=>option(document.querySelector('[name=model]'),v));}
function params(){const p=new URLSearchParams(new FormData($('#filters')));p.set('page',page);p.set('page_size',25);return p}
async function loadRows(){const d=await json('/api/results?'+params());lastPage=d.pages||1;$('#page').textContent=`Page ${d.page} of ${lastPage} · ${d.total} rows`;$('#previous').disabled=d.page<=1;$('#next').disabled=d.page>=lastPage;const body=$('#rows');body.replaceChildren();for(const r of d.items){const tr=document.createElement('tr');for(const val of [r.task_id,'CWE-'+r.target_cwe,r.cwe_level,r.prompt_cwe?'CWE-'+r.prompt_cwe:'—']){const td=document.createElement('td');td.textContent=val;tr.append(td)}let td=document.createElement('td');td.append(badge(r.syntax_valid?'valid':'invalid',r.syntax_valid?'ok':'error'));tr.append(td);td=document.createElement('td');td.append(badge(r.all_tests_pass?'pass':`${r.test_passed}/${r.test_total}`,r.all_tests_pass?'ok':'warn'));tr.append(td);td=document.createElement('td');const count=r.bandit_count+r.codeql_count;td.append(badge(count?count+' findings':(r.analyzer_error?'error':'no findings'),r.analyzer_error?'error':count?'warn':'info'));tr.append(td);td=document.createElement('td');const b=document.createElement('button');b.textContent='Details';b.onclick=()=>showDetail(r.row_id);td.append(b);tr.append(td);body.append(tr)}$('#status').textContent='Results loaded'}
function section(title,text){const h=document.createElement('h3');h.textContent=title;const pre=document.createElement('pre');pre.textContent=text||'—';return [h,pre]}
async function showDetail(id){const r=await json('/api/results/'+id);const c=$('#detail-content');c.replaceChildren();const h=document.createElement('h2');h.textContent=`${r.task_id} · ${r.cwe_level} · generation ${r.generation_index}`;c.append(h,...section('Prompt',r.prompt),...section('Native reasoning',r.reasoning_native),...section('Extracted reasoning',r.reasoning_extracted),...section('Code',r.code));const th=document.createElement('h3');th.textContent='Tests';c.append(th);if(!r.test_results?.length){const p=document.createElement('p');p.className='empty';p.textContent='Tests were not run.';c.append(p)}else for(const t of r.test_results){const p=document.createElement('p');p.append(badge(`${t.category} ${t.test_index}: ${t.status}`,t.passed?'ok':'error'));if(t.error)p.append(' '+t.error);c.append(p)}const fh=document.createElement('h3');fh.textContent='Analyzer findings';c.append(fh);const fs=[...(r.bandit_findings||[]),...(r.codeql_findings||[])];if(!fs.length){const p=document.createElement('p');p.className='empty';p.textContent=(r.bandit_status==='complete'||r.codeql_status==='complete')?'No findings (this is not proof of security).':'Analyzer did not complete.';c.append(p)}else for(const f of fs){const d=document.createElement('div');d.className='finding';d.textContent=`${f.source}/${f.suite} · ${f.cwe?'CWE-'+f.cwe:'no CWE'} · ${f.rule}: ${f.message}`;c.append(d)}$('#detail').classList.add('open');$('#detail').setAttribute('aria-hidden','false');$('#scrim').classList.add('open')}
function close(){ $('#detail').classList.remove('open');$('#detail').setAttribute('aria-hidden','true');$('#scrim').classList.remove('open') }
$('#filters').onsubmit=e=>{e.preventDefault();page=1;loadRows()};$('#previous').onclick=()=>{if(page>1){page--;loadRows()}};$('#next').onclick=()=>{if(page<lastPage){page++;loadRows()}};$('#close').onclick=close;$('#scrim').onclick=close;
Promise.all([loadMeta(),loadRows()]).catch(e=>{$('#status').textContent='Error: '+e.message});"""


def _rate(numerator: int, denominator: int) -> float:
    return round(100 * numerator / denominator, 1) if denominator else 0.0


class ResultRepository:
    def __init__(self, path: str | Path) -> None:
        import pyarrow.parquet as pq

        self.path = Path(path)
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        self.rows = pq.read_table(self.path).to_pylist()

    def meta(self) -> dict[str, Any]:
        total = len(self.rows)
        levels: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in self.rows:
            levels[str(row.get("cwe_level"))].append(row)
        return {
            "total": total,
            "syntax_rate": _rate(sum(row.get("syntax_valid") is True for row in self.rows), total),
            "pass_rate": _rate(sum(row.get("all_tests_pass") is True for row in self.rows), total),
            "finding_rate": _rate(sum(row.get("any_cwe_detected") is True for row in self.rows), total),
            "by_level": [
                {
                    "level": level,
                    "total": len(rows),
                    "pass_rate": _rate(sum(row.get("all_tests_pass") is True for row in rows), len(rows)),
                    "finding_rate": _rate(sum(row.get("any_cwe_detected") is True for row in rows), len(rows)),
                }
                for level, rows in sorted(levels.items())
            ],
            "filters": {
                "cwes": sorted({row.get("target_cwe") for row in self.rows if row.get("target_cwe") is not None}),
                "levels": sorted({str(row.get("cwe_level")) for row in self.rows}),
                "models": sorted({str(row.get("model")) for row in self.rows}),
            },
        }

    def query(self, query: dict[str, list[str]]) -> dict[str, Any]:
        def first(name: str) -> str:
            return (query.get(name) or [""])[0]

        indexed = list(enumerate(self.rows))
        task, cwe, level, model = first("task"), first("cwe"), first("level"), first("model")
        functional, analyzer = first("functional"), first("analyzer")
        if task:
            indexed = [(i, r) for i, r in indexed if task.lower() in str(r.get("task_id", "")).lower()]
        if cwe:
            indexed = [(i, r) for i, r in indexed if str(r.get("target_cwe")) == cwe]
        if level:
            indexed = [(i, r) for i, r in indexed if r.get("cwe_level") == level]
        if model:
            indexed = [(i, r) for i, r in indexed if r.get("model") == model]
        if functional == "pass":
            indexed = [(i, r) for i, r in indexed if r.get("all_tests_pass") is True]
        elif functional == "fail":
            indexed = [(i, r) for i, r in indexed if r.get("test_total", 0) and not r.get("all_tests_pass")]
        elif functional == "not-run":
            indexed = [(i, r) for i, r in indexed if not r.get("test_total", 0)]
        if analyzer == "findings":
            indexed = [(i, r) for i, r in indexed if r.get("bandit_findings") or r.get("codeql_findings")]
        elif analyzer == "none":
            indexed = [
                (i, r)
                for i, r in indexed
                if not r.get("bandit_findings")
                and not r.get("codeql_findings")
                and (r.get("bandit_status") == "complete" or r.get("codeql_status") == "complete")
            ]
        elif analyzer == "error":
            indexed = [(i, r) for i, r in indexed if r.get("bandit_status") in {"error", "partial", "unavailable"} or r.get("codeql_status") in {"error", "partial", "unavailable"}]
        try:
            page = max(1, int(first("page") or 1))
            page_size = min(100, max(1, int(first("page_size") or 25)))
        except ValueError:
            page, page_size = 1, 25
        total = len(indexed)
        pages = max(1, (total + page_size - 1) // page_size)
        page = min(page, pages)
        items = []
        for row_id, row in indexed[(page - 1) * page_size : page * page_size]:
            items.append(
                {
                    "row_id": row_id,
                    "task_id": row.get("task_id"),
                    "target_cwe": row.get("target_cwe"),
                    "cwe_level": row.get("cwe_level"),
                    "prompt_cwe": row.get("prompt_cwe"),
                    "syntax_valid": row.get("syntax_valid"),
                    "test_passed": row.get("test_passed", 0),
                    "test_total": row.get("test_total", 0),
                    "all_tests_pass": row.get("all_tests_pass"),
                    "bandit_count": len(row.get("bandit_findings") or []),
                    "codeql_count": len(row.get("codeql_findings") or []),
                    "analyzer_error": row.get("bandit_status") in {"error", "partial", "unavailable"} or row.get("codeql_status") in {"error", "partial", "unavailable"},
                }
            )
        return {"page": page, "page_size": page_size, "pages": pages, "total": total, "items": items}

    def detail(self, row_id: int) -> dict[str, Any]:
        if row_id < 0 or row_id >= len(self.rows):
            raise IndexError(row_id)
        return self.rows[row_id]


class ViewerHandler(BaseHTTPRequestHandler):
    server: "ViewerServer"

    def _send(self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, value: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._send(json.dumps(value, ensure_ascii=False).encode(), "application/json; charset=utf-8", status)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self._send(INDEX_HTML.encode(), "text/html; charset=utf-8")
        if parsed.path == "/app.css":
            return self._send(APP_CSS.encode(), "text/css; charset=utf-8")
        if parsed.path == "/app.js":
            return self._send(APP_JS.encode(), "text/javascript; charset=utf-8")
        if parsed.path == "/api/meta":
            return self._json(self.server.repository.meta())
        if parsed.path == "/api/results":
            return self._json(self.server.repository.query(parse_qs(parsed.query)))
        if parsed.path.startswith("/api/results/"):
            try:
                return self._json(self.server.repository.detail(int(parsed.path.rsplit("/", 1)[1])))
            except (ValueError, IndexError):
                return self._json({"error": "result not found"}, HTTPStatus.NOT_FOUND)
        return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Any) -> None:
        return


class ViewerServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], repository: ResultRepository) -> None:
        self.repository = repository
        super().__init__(address, ViewerHandler)


def create_server(results: str | Path, host: str = "127.0.0.1", port: int = 8000) -> ViewerServer:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("El viewer sólo puede escuchar en loopback")
    return ViewerServer((host, port), ResultRepository(results))


def serve(results: str | Path, host: str = "127.0.0.1", port: int = 8000) -> None:
    server = create_server(results, host, port)
    print(f"Viewer disponible en http://{host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
