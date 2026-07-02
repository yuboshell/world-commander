#!/usr/bin/env python
"""Build a self-contained literature-review web page from the tagged survey CSV + the positioning
figure (world-commander-bench report convention). Frame diagram -> positioning figure -> an
interactive (filter/sort) table of the 73 refs. Publishes to the shared private Pages hub as
literature.html.

    python build_lit_page.py            # writes literature.html
    python build_lit_page.py --publish  # also copies it to ../world-commander-bench/literature.html
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "survey" / "command-crowds.csv"
FIG = ROOT / "fig" / "lit-positioning.png"
OUT = ROOT / "literature.html"
TITLE = "World Commander — Literature Review"

ap = argparse.ArgumentParser()
ap.add_argument("--publish", action="store_true")
publish = ap.parse_args().publish

rows = list(csv.DictReader(open(CSV)))
# fields surfaced in the interactive table (subset of the 23 columns)
COLS = ["Index", "Pillar", "Theme", "Article", "Author", "Venue", "Date",
        "Command_freeform", "Real_time", "Multi_agent", "Budget_aware", "Executor_type",
        "Novelty", "Link",
        # Diao's full record, revealed on row click:
        "Method", "Dataset", "Metric", "Baselines", "Models", "Result",
        "Evaluation Methods", "Others", "Code"]
data = [{c: r.get(c, "") for c in COLS} for r in rows]
data_js = json.dumps(data)

generated = time.strftime("%Y-%m-%d, %I:%M %p %Z")
n = len(rows)


def count(col, val):
    return sum(1 for r in rows if r.get(col) == val)


# Native 2x2 open-quadrant grid (over free-form-command papers), so it matches the page type
# instead of a baked-in PNG. Each cell: total / budget-aware / top executors.
_ff = [r for r in rows if r.get("Command_freeform") == "yes"]


def _cell(ma, rt):
    sub = [r for r in _ff if (r.get("Multi_agent") == "yes") == ma
           and (r.get("Real_time") == "yes") == rt]
    bud = sum(1 for r in sub if r.get("Budget_aware") == "yes")
    ex = {}
    for r in sub:
        e = r.get("Executor_type", "")
        if e and e != "na":
            ex[e] = ex.get(e, 0) + 1
    top = " · ".join(f"{k} {v}" for k, v in sorted(ex.items(), key=lambda kv: -kv[1])[:2])
    return len(sub), bud, top


_maxc = max(_cell(m, t)[0] for m in (False, True) for t in (False, True)) or 1


def _qcell(ma, rt, target=False):
    nn, bud, top = _cell(ma, rt)
    a = 0.08 + 0.5 * nn / _maxc
    bcls = "qb0" if bud == 0 else "qb"
    star = " &#9733;" if target else ""
    gap = ' <span class="qgap">&larr; the gap</span>' if target else ""
    tcls = " qtarget" if target else ""
    return (f'<td class="qc{tcls}" style="background:rgba(31,119,180,{a:.2f})">'
            f'<b>{nn}</b> papers{star}<br><span class="{bcls}">{bud} budget-aware</span>{gap}'
            f'<br><small>{top}</small></td>')


quad = ('<table class="quad"><tr><td></td><th>offline</th><th>real-time</th></tr>'
        '<tr><th class="qrh">single-agent</th>' + _qcell(False, False) + _qcell(False, True) + '</tr>'
        '<tr><th class="qrh">multi-agent / crowd</th>'
        + _qcell(True, False) + _qcell(True, True, True) + '</tr></table>')


axes = [("free-form / abstract command", count("Command_freeform", "yes")),
        ("real-time / streaming", count("Real_time", "yes")),
        ("multi-agent / crowd", count("Multi_agent", "yes")),
        ("budget-aware (measures compute)", count("Budget_aware", "yes"))]
axis_rows = "".join(f"<tr><td>{a}</td><td style='text-align:right'>{c}</td></tr>" for a, c in axes)

# closest three-axis set (free-form x real-time x multi-agent), computed, not hard-coded
_c3 = [r for r in _ff if r.get("Real_time") == "yes" and r.get("Multi_agent") == "yes"]
_c3bud = sum(1 for r in _c3 if r.get("Budget_aware") == "yes")
_c3ex = {}
for r in _c3:
    e = r.get("Executor_type", "")
    if e and e != "na":
        _c3ex[e] = _c3ex.get(e, 0) + 1
c3_break = ", ".join(f"{v} {k}" for k, v in sorted(_c3ex.items(), key=lambda kv: -kv[1]))
c3_bud_txt = "every one budget-blind" if _c3bud == 0 else f"{_c3bud} of them budget-aware"

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<link rel="stylesheet" href="style.css">
<link href="https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic" rel="stylesheet">
<style>
  /* page-specific literature styles (generic base + flowchart colours in style.css) */
  h2 {{ font-size:1.15rem; margin-top:2.2rem; border-bottom:1px solid #eee; padding-bottom:.2rem; }}
  .hint {{ color:#666; font-size:.86rem; }}
  /* open-quadrant 2x2 — native, matches the body type (no baked-in PNG) */
  table.quad {{ border-collapse:separate; border-spacing:7px; margin:14px auto; }}
  table.quad th {{ font-weight:600; color:#555; font-size:.84rem; }}
  table.quad th.qrh {{ text-align:right; white-space:nowrap; padding-right:4px; }}
  table.quad td.qc {{ border-radius:8px; padding:14px; text-align:center; line-height:1.45;
                      min-width:200px; font-size:.86rem; border:1px solid #d6e3f0; }}
  table.quad td.qtarget {{ outline:2.5px solid crimson; border-color:crimson; }}
  .qb {{ color:#161; font-weight:600; }} .qb0 {{ color:#b00; font-weight:600; }}
  .qgap {{ color:#b00; }} table.quad small {{ color:#555; }}
  /* controls + table */
  .controls {{ display:flex; gap:.6rem; flex-wrap:wrap; align-items:center; margin:.8rem 0; }}
  .controls select, .controls input {{ font-size:.9rem; padding:.25rem .4rem; }}
  table.lit {{ border-collapse:collapse; width:100%; font-size:.82rem; }}
  table.lit th, table.lit td {{ border:1px solid #e3e3e3; padding:.3rem .45rem; vertical-align:top; text-align:left; }}
  table.lit th {{ background:#f3f5f7; position:sticky; top:0; cursor:pointer; user-select:none; }}
  table.lit tr:nth-child(even) td {{ background:#fafafa; }}
  .badge {{ display:inline-block; border-radius:4px; padding:0 .35rem; font-size:.75rem; }}
  .y {{ background:#d8f0d8; color:#161; }} .nn {{ background:#eee; color:#777; }}
  .pill {{ font-weight:600; }}
  td.novelty {{ max-width:340px; }}
  table.lit tr.main {{ cursor:pointer; }}
  table.lit tr.detail td {{ background:#fbfbf7; }}
  dl.d {{ display:grid; grid-template-columns:max-content 1fr; gap:2px 14px; margin:.3rem 0; font-size:.82rem; }}
  dl.d dt {{ font-weight:600; color:#555; }} dl.d dd {{ margin:0; }}
</style></head>
<body>
<div class="wrap">

<header class="mast">
  <h1>{TITLE}</h1>
  <p class="subtitle">The paradigm: a human gives free-form natural-language commands; an LLM-based pipeline
executes them as coordinated multi-agent behaviour — RTS units or full-body crowd motion — in real
time, under a compute budget. {n} references, tagged.</p>
  <p class="upd"><b>Updated:</b> {generated} &middot; public</p>
</header>

<p class="topnav">
  <a href="home.html">Home</a> &nbsp;/&nbsp;
  <a href="proposal.html">Proposal</a> &nbsp;/&nbsp;
  <a href="literature.html" class="active">Literature</a> &nbsp;/&nbsp;
  <a href="index.html">Grid Arena (E1)</a> &nbsp;/&nbsp;
  <a href="sc2.html">StarCraft II (E2)</a> &nbsp;/&nbsp;
  <a href="embodiment.html">Embodiment (E3)</a> &nbsp;/&nbsp;
  <a href="motion.html">Crowd Motion (E4)</a> &nbsp;/&nbsp;
  <a href="graph-bpe-motion.html">Motion BPE</a>
</p>

<h2>The paradigm</h2>
<div class="pipe">
  <div class="box shared">Free-form / abstract<br>command</div><span class="arr">&rarr;</span>
  <div class="box shared">Interpreter<br>(LLM)</div><span class="arr">&rarr;</span>
  <div class="box shared">Coordination<br>assignment / MARL</div><span class="arr">&rarr;</span>
  <div class="execs">
    <div class="box edge">Coarse: discrete actions (game API)</div>
    <div class="box edge">Fine: continuous motion (generated)</div>
  </div>
</div>
<p class="hint">Colours follow the hub's tree: the <b>trunk</b> (brown) is the domain-agnostic shared
pipeline (the <b>budget</b> wedge sits on the interpreter; <b>coordination</b> is the multi-agent
layer); the <b>branches</b> (olive) are the domain-specific executors, split by the level of detail
of their output.</p>

<h2>The open quadrant = the contribution</h2>
<table><tr><th>axis</th><th>“yes” / {n}</th></tr>{axis_rows}
<tr><td><b>all four at once</b></td><td style="text-align:right"><b>0</b></td></tr></table>
<p class="hint"><b>No paper in the survey hits all four.</b> The closest (free-form × real-time ×
multi-agent, ignoring budget) is {len(_c3)} papers, {c3_bud_txt} — {c3_break}.
The wedge is the budget-aware corner, open in both executor domains.</p>
{quad}
<p class="hint" style="text-align:center">Free-form-command papers (n={count('Command_freeform','yes')}) by real-time × multi-agent — the target corner (multi-agent × real-time × budget-aware) is empty.</p>

<h2>The survey ({n} refs) — filter &amp; sort</h2>
<p class="hint">Download the full survey as a spreadsheet: <a href="survey/command-crowds.csv" download>command-crowds.csv</a> ({n} references, all columns).</p>
<div class="controls">
  <input id="q" placeholder="search title / author / novelty…" size="26">
  <label>pillar <select id="f_Pillar"></select></label>
  <label>real-time <select id="f_Real_time"></select></label>
  <label>multi-agent <select id="f_Multi_agent"></select></label>
  <label>budget-aware <select id="f_Budget_aware"></select></label>
  <label>executor <select id="f_Executor_type"></select></label>
  <span class="hint" id="shown"></span>
</div>
<table class="lit" id="tbl"><thead><tr>
  <th data-k="Pillar">Pillar</th><th data-k="Theme">Theme</th><th data-k="Article">Article</th>
  <th data-k="Author">Author</th><th data-k="Venue">Venue</th><th data-k="Date">Date</th>
  <th data-k="Command_freeform">free-form</th><th data-k="Real_time">real-time</th>
  <th data-k="Multi_agent">multi</th><th data-k="Budget_aware">budget</th>
  <th data-k="Executor_type">executor</th><th data-k="Novelty">novelty</th>
</tr></thead><tbody></tbody></table>

<script>
const DATA = {data_js};
const FILT = ["Pillar","Real_time","Multi_agent","Budget_aware","Executor_type"];
const tbody = document.querySelector("#tbl tbody");
let sortK = "Pillar", sortDir = 1;
function uniq(k) {{ return [...new Set(DATA.map(r=>r[k]).filter(x=>x!=""))].sort(); }}
FILT.forEach(k => {{
  const s = document.getElementById("f_"+k);
  s.innerHTML = '<option value="">all</option>' + uniq(k).map(v=>`<option>${{v}}</option>`).join("");
  s.onchange = render;
}});
document.getElementById("q").oninput = render;
document.querySelectorAll("#tbl th").forEach(th => th.onclick = () => {{
  const k = th.dataset.k; if(!k) return;
  sortDir = (sortK===k) ? -sortDir : 1; sortK = k; render();
}});
function badge(v) {{ return v=="yes" ? '<span class="badge y">yes</span>'
  : (v=="no" ? '<span class="badge nn">no</span>' : '<span class="badge nn">'+ (v||'–') +'</span>'); }}
function render() {{
  const q = document.getElementById("q").value.toLowerCase();
  let rows = DATA.filter(r => {{
    for (const k of FILT) {{ const v=document.getElementById("f_"+k).value; if(v && r[k]!=v) return false; }}
    if (q && !(r.Article+" "+r.Author+" "+r.Novelty).toLowerCase().includes(q)) return false;
    return true;
  }});
  rows.sort((a,b)=> (a[sortK]>b[sortK]?1:a[sortK]<b[sortK]?-1:0)*sortDir);
  tbody.innerHTML = rows.map(r => `<tr class="main" onclick="this.nextElementSibling.hidden=!this.nextElementSibling.hidden">
    <td class="pill">${{r.Pillar}}</td><td>${{r.Theme}}</td>
    <td>${{r.Link? `<a href="${{r.Link}}" target="_blank" onclick="event.stopPropagation()">${{r.Article}}</a>` : r.Article}}</td>
    <td>${{r.Author}}</td><td>${{r.Venue}}</td><td>${{r.Date}}</td>
    <td>${{badge(r.Command_freeform)}}</td><td>${{badge(r.Real_time)}}</td>
    <td>${{badge(r.Multi_agent)}}</td><td>${{badge(r.Budget_aware)}}</td>
    <td>${{r.Executor_type}}</td><td class="novelty">${{r.Novelty}}</td></tr>
    <tr class="detail" hidden><td colspan="12"><dl class="d">
      <dt>Method</dt><dd>${{r.Method||'–'}}</dd>
      <dt>Dataset</dt><dd>${{r.Dataset||'–'}}</dd>
      <dt>Metric</dt><dd>${{r.Metric||'–'}}</dd>
      <dt>Baselines</dt><dd>${{r.Baselines||'–'}}</dd>
      <dt>Models</dt><dd>${{r.Models||'–'}}</dd>
      <dt>Result</dt><dd>${{r.Result||'–'}}</dd>
      <dt>Evaluation</dt><dd>${{r['Evaluation Methods']||'–'}}</dd>
      ${{r.Others? `<dt>Other</dt><dd>${{r.Others}}</dd>` : ''}}
      ${{r.Code? `<dt>Code</dt><dd><a href="${{r.Code}}" target="_blank" onclick="event.stopPropagation()">${{r.Code}}</a></dd>` : ''}}
    </dl></td></tr>`).join("");
  document.getElementById("shown").textContent = rows.length + " / " + DATA.length + " shown";
}}
render();
</script>
<footer style="margin-top:3rem;color:#777;font-size:.82rem;border-top:1px solid #eee;padding-top:.6rem">
World Commander — literature review. Source of record: <code>survey/command-crowds.csv</code> +
<code>LITERATURE.md</code>; regenerate with <code>python build_lit_page.py --publish</code>.
Public.
</footer>
<p class="attribution">Design from <a href="https://jonbarron.info" target="_blank" rel="noopener">Jon Barron's website</a>, via <a href="https://github.com/leonidk/leonidk.github.io" target="_blank" rel="noopener">Leonid Keselman's Jekyll fork</a>.</p>

</div>
</body></html>"""

OUT.write_text(HTML)
print(f"wrote {OUT.name}  ({len(HTML)/1e6:.2f} MB, {n} refs)")
if publish:
    dest = ROOT.parent / "world-commander-bench" / "literature.html"
    if dest.parent.exists():
        dest.write_bytes(OUT.read_bytes())
        print(f"published -> {dest}\n  next: commit + push the bench repo (gitlab remote) to deploy")
    else:
        print(f"--publish: bench repo not found at {dest.parent}")
