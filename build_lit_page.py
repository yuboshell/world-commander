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

fig_uri = "data:image/png;base64," + base64.b64encode(FIG.read_bytes()).decode()
generated = time.strftime("%Y-%m-%d, %I:%M %p %Z")
n = len(rows)


def count(col, val):
    return sum(1 for r in rows if r.get(col) == val)


axes = [("free-form / abstract command", count("Command_freeform", "yes")),
        ("real-time / streaming", count("Real_time", "yes")),
        ("multi-agent / crowd", count("Multi_agent", "yes")),
        ("budget-aware (measures compute)", count("Budget_aware", "yes"))]
axis_rows = "".join(f"<tr><td>{a}</td><td style='text-align:right'>{c}</td></tr>" for a, c in axes)

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 1080px; color:#1a1a1a;
         line-height:1.55; padding:0 1rem; }}
  h1 {{ font-size:1.5rem; margin-bottom:.2rem; }}
  h2 {{ font-size:1.15rem; margin-top:2.2rem; border-bottom:1px solid #eee; padding-bottom:.2rem; }}
  .hint {{ color:#666; font-size:.86rem; }}
  img.fig {{ max-width:100%; border:1px solid #e2e2e2; border-radius:6px; display:block; margin:12px auto; }}
  /* pipeline diagram (self-contained, no JS) */
  .pipe {{ display:flex; align-items:center; flex-wrap:wrap; gap:8px; margin:16px 0; }}
  .box {{ border-radius:8px; padding:10px 12px; font-size:.9rem; text-align:center; border:2px solid; }}
  .shared {{ background:#e8eefc; border-color:#5577bb; }}
  .edge {{ background:#fdeeee; border-color:#bb5555; }}
  .arr {{ color:#999; font-size:1.3rem; }}
  .execs {{ display:flex; flex-direction:column; gap:6px; }}
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
<div style="font-size:.9rem;color:#666;border-bottom:1px solid #eee;padding-bottom:.6rem;margin-bottom:1rem">
Reports: <a href="index.html">Grid Arena (E1)</a> &middot; <a href="sc2.html">StarCraft II (E2)</a>
&middot; <a href="embodiment.html">Embodiment (E3)</a> &middot; <a href="motion.html">Crowd Motion (E4)</a>
&middot; <b>Literature</b></div>
<h1>{TITLE}</h1>
<p class="hint">The paradigm: a human gives free-form natural-language commands; an LLM-based pipeline
executes them as coordinated multi-agent behaviour — RTS units or full-body crowd motion — in real
time, under a compute budget. {n} references, tagged.</p>
<p class="hint"><b>Updated:</b> {generated} &middot; members-only</p>

<h2>The paradigm</h2>
<div class="pipe">
  <div class="box shared">free-form / abstract<br>command</div><span class="arr">&rarr;</span>
  <div class="box shared">interpreter<br>(LLM)</div><span class="arr">&rarr;</span>
  <div class="box shared">coordination<br>assignment / MARL</div><span class="arr">&rarr;</span>
  <div class="execs">
    <div class="box edge">RTS: game-unit commands</div>
    <div class="box edge">crowd: full-body motion</div>
  </div>
</div>
<p class="hint">Blue = the domain-agnostic shared middle (the <b>budget</b> wedge sits on the
interpreter; <b>coordination</b> is the multi-agent layer). Red = the domain-specific
<b>executor</b> edge.</p>

<h2>The open quadrant = the contribution</h2>
<table><tr><th>axis</th><th>“yes” / {n}</th></tr>{axis_rows}
<tr><td><b>all four at once</b></td><td style="text-align:right"><b>0</b></td></tr></table>
<p class="hint"><b>No paper in the survey hits all four.</b> The closest (free-form × real-time ×
multi-agent, ignoring budget) is 5 papers, every one budget-blind — 4 RTS units, 1 full-body motion.
The wedge is the budget-aware corner, open in both executor domains.</p>
<img class="fig" src="{fig_uri}" alt="open-quadrant positioning">

<h2>The survey ({n} refs) — filter &amp; sort</h2>
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
Members-only; not for public hosting.
</footer>
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
