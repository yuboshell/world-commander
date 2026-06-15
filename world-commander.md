---
marp: true
html: true
paginate: true
size: 16:9
title: "World Commander"
---

<style>
/* ── Keynote-White theme ─────────────────────────────────────────────────── */
section {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #1a1a1a;
  background: #ffffff;
  font-size: 27px;
  line-height: 1.34;
  padding: 34px 50px 36px 50px;
  justify-content: flex-start !important;   /* top-align all slides, beat default theme */
}
h1 {                                   /* slide title: white bg, thin rule */
  font-size: 35px;
  font-weight: 600;
  color: #000;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1.5px solid #c9c9c9;
}
h1 .sec { color: #1a1a1a; font-weight: 600; margin-right: 0.45em; }   /* paper-style section number */
a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
strong { font-weight: 600; }
ul, ol { margin: 0.3em 0; padding-left: 1.1em; }
li { margin: 0.42em 0; }
li > ul { margin-top: 0.3em; }
p { margin: 0.5em 0; }
blockquote { border-left: 3px solid #333; padding-left: 16px; margin: 0.7em 0 0 0; font-weight: 600; color: #1a1a1a; }
code { font-size: 0.92em; background: #f0f0f0; padding: 0 4px; border-radius: 3px; }

/* booktabs-style rules: reset default-theme borders/zebra first, then add rules */
table { border-collapse: collapse; }
table, tr, th, td { border: none !important; background: transparent !important; }
th, td { padding: 3px 10px; text-align: left; vertical-align: top; }
table { border-top: 1.5px solid #333 !important; border-bottom: 1.5px solid #333 !important; }
thead th { border-bottom: 1px solid #333 !important; font-weight: 600; }

/* two-column scaffold; ratios set inline per slide */
.columns { display: grid; gap: 26px; align-items: start; }
.col-img { text-align: center; }
.col-img img { max-width: 100%; }
.caption { font-size: 0.72em; color: #1a1a1a; line-height: 1.28; margin-top: 6px; text-align: left; }
.credit  { font-size: 0.6em; color: #1a1a1a; margin-top: 2px; }

/* page number bottom-right as "current / total" */
section::after {
  content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
  font-size: 14px; color: #1a1a1a;
}

/* dense slides */
section.tight { font-size: 23px; line-height: 1.3; }
section.tight h1 { font-size: 32px; }
section.tight li { margin: 0.36em 0; }

/* title slide: title + scope + two captioned figures, then author */
section.title { justify-content: flex-start !important; }
section.title h1 { border-bottom: none; font-size: 42px; margin: 0 0 6px 0; padding: 0; }
section.title .sub { font-size: 24px; color: #1a1a1a; margin: 0 0 12px 0; padding-bottom: 12px; border-bottom: 1.5px solid #c9c9c9; }
section.title .figs { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: end; margin: 6px 0 0 0; }
section.title .figs .col-img img { max-width: 100%; }
section.title .figs .caption { text-align: center; }
section.title .by { font-size: 23px; color: #1a1a1a; margin: 16px 0 0 0; text-align: center; }
section.title .date { font-size: 17px; color: #1a1a1a; margin-top: 4px; text-align: center; }
section.title::after { content: "" !important; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->

# World Commander

<p class="sub">Natural-language command of agent crowds in strategy games, under real-time compute budgets</p>

<p class="by">This proposal grew from Yubo Huang's interest and insight, under the guidance of Dr. Enmao Diao.</p>

<div class="figs">
<div class="col-img">

<img src="fig/hero.svg" style="max-height: 280px;">

<div class="caption">What we build: real-time, language-commanded agent crowds (here, two players commanding their own).</div>

</div>
<div class="col-img">

<img src="fig/command-station.png" style="max-height: 280px;">

<div class="caption">The long-term goal: the next revolutionary video game, played by voice from the commander's chair.</div>

</div>
</div>

<p class="date">June 2026</p>

---

<!-- _class: tight -->
# <span class="sec">1</span> Related Work: Efficiency, Untested at Game Speed

- The interface shipped once ([Tom Clancy's EndWar (2008)](https://en.wikipedia.org/wiki/Tom_Clancy's_EndWar)), but on a 70-word grammar. Language models lifted that limit; they still **cannot act at game pace**.
- LLMs already play StarCraft II, by text ([TextStarCraft II (NeurIPS 2024)](https://arxiv.org/abs/2312.11865)) or screenshots ([AVA (2026)](https://arxiv.org/abs/2503.05383)), but only by **pausing or slowing the clock**.
- Real-time is only now being measured ([VideoGameBench (2025)](https://arxiv.org/abs/2505.18134): models collapse once the clock keeps running), and only for single agents, **not the efficiency methods**.
- Eviction, quantization, and distillation are tuned on perplexity, where they already drop the wrong instruction ([Pitfalls of KV Cache Compression (ACL 2026)](https://arxiv.org/abs/2510.00231)); none is **scored by win rate in a live RTS**, where that lost context loses the match.

> How much does command cost, in latency and memory, at game speed, and how do we drive it down?

---

<!-- _class: tight -->
# <span class="sec">2</span> Preliminaries

The background this work builds on:

| Area | What it gives us |
|---|---|
| **Reinforcement learning** | A game is a Markov decision process: an agent acts, and win rate is the reward. We need to *understand* this to read the field; the work runs models by prompting, training none of its own. |
| **Efficient LLM inference** | KV-cache eviction (H2O, SnapKV, StreamingLLM, [OBCache](https://arxiv.org/abs/2510.07651)), structured pruning, quantization, distillation: the methods this work puts to the test. |
| **Vision-language-action models** | [π0](https://arxiv.org/abs/2410.24164): a slow vision-language backbone driving a fast action expert, trained by imitation. A model for splitting a slow strategic brain from fast executors. |
| **The StarCraft II agent stack** | [PySC2](https://github.com/google-deepmind/pysc2), [TextStarCraft II](https://arxiv.org/abs/2312.11865), LLM-PySC2: the environment we inherit rather than rebuild. |
| **Tokenization beyond text** | Byte-pair encoding and [graph tokenization (ICLR 2026)](https://www.diaoenmao.com): the basis for a learned game-state tokenizer. |

---

<!-- _class: tight -->
# <span class="sec">3</span> The Roadmap: Three Projects

**World Commander** is a research **program**, delivered as three **projects** (each a top-tier paper's worth of work) across environments of growing complexity (a toy room → StarCraft II → multiplayer → a full game), under one shared **harness**. The end-state game is the long-term goal, not a deliverable; each project answers a question its community already cares about, beyond the game.

| Project | Phase | The question | Who cares |
|---|---|---|---|
| Real-time commander benchmark | 1 | Which efficiency methods survive a closed-loop game clock? | KV-cache and pruning |
| Game-state tokenizer | 1 to 2 | Does compact tokenization extend to entity and event streams? | Tokenization beyond text |
| Crowd motion under budget (embodiment) | 3 | Can language-commanded crowds move in real time on one GPU? | Motion generation, graphics |

---

# <span class="sec">4</span> The Command Arena

**The first step:** a warm-up task that validates the streaming-command infrastructure cheaply, before StarCraft II.

<div class="columns" style="grid-template-columns: 41% 56%">
<div>

- Colour-tagged agents in a room; each moves in **one of four directions** on command.
- One command is trivial; the test is the **stream**: many, fast.
- Harder with **rate**, **compositional orders** ("everyone but the yellow one"), and **memory** ("the one I moved west").
- Measured: **grounding accuracy**, **command-to-action latency**, **deadline misses**.

</div>
<div class="col-img">

<img src="fig/arena.svg" style="max-height: 384px;">

<div class="caption"><strong>Figure 2: the command arena.</strong> Colour-tagged agents, each moving in one of four directions on command.</div>

</div>
</div>

