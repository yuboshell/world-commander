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

/* appendix landscape slides: run-in related-work paragraphs, vertically centred */
section.landscape { font-size: 23px; line-height: 1.32; justify-content: center !important; }
section.landscape h1 { font-size: 30px; }
section.landscape p { margin: 0.62em 0; }
section.landscape .lead { font-size: 0.78em; color: #555; margin: 0 0 0.5em 0; }

/* outline / agenda slide: vertically centred list */
section.outline { justify-content: center !important; }
section.outline li { margin: 0.55em 0; }

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

<p class="sub">Natural-language command of agent crowds in real-time strategy games, under latency and memory budgets</p>

<p class="by">This proposal grew from Yubo Huang's interest and insight, under the guidance of Dr. Enmao Diao.</p>

<div class="figs">
<div class="col-img">

<img src="fig/hero.svg" style="max-height: 280px;">

<div class="caption">What we build: real-time, language-commanded agent crowds (here, two players commanding their own).</div>

</div>
<div class="col-img">

<img src="fig/command-station.png" style="max-height: 280px;">

<div class="caption">The long-term goal: a new kind of video game, played by voice from the commander's chair.</div>

<div class="credit">Image generated with GPT Image 2.</div>

</div>
</div>

<p class="date">June 2026</p>

---

<!-- _class: outline -->
# Outline

1. **Related Work**: agents, real-time benchmarks, and efficient inference
2. **The Roadmap**: one question, across steadily harder environments
3. **The Command Arena**: the first step, before StarCraft II

---

<!-- _class: tight -->
# <span class="sec">1</span> Related Work

- The interface shipped once ([Tom Clancy's EndWar (2008)](https://en.wikipedia.org/wiki/Tom_Clancy's_EndWar)), but on a 70-word grammar. Language models lifted that limit; they still **cannot act at game pace**.
- LLMs already play StarCraft II, by text ([TextStarCraft II (NeurIPS 2024)](https://arxiv.org/abs/2312.11865)) or screenshots ([AVA (2026)](https://arxiv.org/abs/2503.05383)), but only by **pausing or slowing the clock**.
- Real-time is only now being measured ([VideoGameBench (2025)](https://arxiv.org/abs/2505.18134): performance drops once the clock runs), and only for single agents, **not the efficiency methods**.
- Eviction, quantization, and distillation are tuned on perplexity, where they already drop the wrong instruction ([Pitfalls of KV Cache Compression (ACL 2026)](https://arxiv.org/abs/2510.00231)); none is **tested inside a running game**, where a discarded detail can decide the match.

> How much does command cost, in latency and memory, at game speed, and how can it be reduced?

---

<!-- _class: landscape -->
# Related Work: The Landscape (1 of 2)

<p class="lead">Agents at game speed, and the methods under test. The fuller field behind the argument; the canonical review with every link is <code>LITERATURE.md</code>.</p>

**Agents in real-time games.** [AlphaStar](https://www.nature.com/articles/s41586-019-1724-z) (Nature 2019) mastered StarCraft II by full reinforcement learning (no language, datacentre scale, fully autonomous); the precedent we deliberately do not repeat. LLMs now issue SC2 commands (TextStarCraft II, LLM-PySC2, AVA), but only with the clock paused or slowed. Real-time play has only recently been benchmarked: VideoGameBench and AgileThinker show performance dropping under time pressure. Closest to us, [HLA](https://arxiv.org/abs/2312.15224), Adaptive Command, and DPT-Agent put a human in command with a fast-slow split, but cooperatively, or by steering a hand-built behaviour tree. CivRealm is the turn-based-strategy contrast.

**Efficient inference, under latency and memory.** The methods evaluated here: KV-cache eviction (H2O, SnapKV, StreamingLLM, [OBCache](https://arxiv.org/abs/2510.07651)), plus action-level Speculative Actions, which cuts latency losslessly. Recent analyses (Pitfalls of KV Cache Compression, DefensiveKV, SideQuest) show eviction can discard the wrong information, and that its effect is task-dependent. [WorldMemArena](https://arxiv.org/abs/2605.29341) pushes agent-memory evaluation into a closed interaction loop: a different "memory" from the KV-cache, but the same methodological turn we make.

---

<!-- _class: landscape -->
# Related Work: The Landscape (2 of 2)

<p class="lead">Fast-slow execution, game-state representation, and the motion stack.</p>

**Hierarchical and VLA fast-slow execution.** [π0](https://arxiv.org/abs/2410.24164) pairs a slow vision-language brain with a fast action expert (up to 50 Hz); Fast-in-Slow folds both into one backbone; OpenVLA is the open "tokens-as-actions" baseline. This is the split we adapt for commander plus executors. Language-conditioned precedents: NL-to-StarCraft II grounding (2019) and CALVIN.

**Game-state representation and world models.** Toward fewer tokens per decision: Diao's [graph tokenization](https://arxiv.org/abs/2603.11099) (ICLR 2026), VQ-VAE, and IRIS / Δ-IRIS (context-aware delta tokenization). Action-conditioned world models, WHAM / WHAMM (Nature 2025), GameNGen, and DreamerV3, are the engines behind any what-if forecaster.

**Crowd and real-time motion (embodiment, deferred).** CrowdMoGen has an LLM plan a crowd's motion, but makes no real-time claim. Per-character real-time generators under budget: MotionLCM, MotionPCM, MotionStreamer, and [MotionBricks](https://arxiv.org/abs/2604.24833) (NVIDIA, SIGGRAPH 2026; 350k skills from one backbone). Single-character today; language-commanded crowds on one GPU remain open.

---

<!-- _class: tight -->
# <span class="sec">2</span> The Roadmap

**One program, one question:** what does command cost at game speed, and how can it be reduced? That question holds across the whole program; the one thing that grows is the environment we test it in:

<p style="text-align: center; font-size: 1.18em; margin: 0.7em 0;"><strong>Toy Arena&nbsp;&nbsp;→&nbsp;&nbsp;StarCraft II&nbsp;&nbsp;→&nbsp;&nbsp;Multiplayer&nbsp;&nbsp;→&nbsp;&nbsp;Full Game</strong></p>

Throughout, one loop: **measure** the cost of command, **build methods** to cut it, behind a single **commander interface**. Three milestones fall out along the way, each a paper a community already wants:

- **Real-time commander benchmark:** the cost, measured against a live clock (KV-cache and pruning)
- **Game-state tokenizer:** fewer tokens per decision, so less latency and memory (tokenization beyond text)
- **Crowd-motion embodiment:** command at scale on one GPU, deferred (motion generation and graphics)

The end-state game is the long-term goal, not a deliverable.

---

<!-- _class: tight -->
# <span class="sec">3</span> The Command Arena

**The first step:** a warm-up task that validates the streaming-command infrastructure cheaply, before StarCraft II.

<div class="columns" style="grid-template-columns: 41% 56%">
<div>

- Colour-tagged agents in a room; each moves in **one of four directions** on command.
- One command is trivial; the test is the **stream**: many, fast.
- Harder with **rate**, **grouping** ("everyone except the yellow one"), and **memory** ("the one I sent west earlier, now move it north").
- **Not single-sided:** uncontrolled agents move on their own, so a late command concedes ground.
- Measured: **grounding accuracy**, **command-to-action latency**, **deadline misses**.

</div>
<div class="col-img">

<img src="fig/arena.svg" style="max-height: 360px;">

<div class="caption"><strong>The command arena.</strong> Colour-tagged agents, each moving in one of four directions on command.</div>

</div>
</div>

---

<!-- _class: tight -->
# Team

<p style="margin: 0.2em 0 0.7em 0;">Who builds what, across the command-to-action loop.</p>

| Member | Focus |
|---|---|
| **Yubo Huang** | Command interpreter, benchmark and harness, the budget framing |
| **Enmao Diao** (advisor) | Efficient inference: KV-cache eviction, pruning, tokenization |
| **Hongsong Tang** (Tencent Timi Studio) | Multi-agent coordination (RL / MARL) |
| **Xirui Shi** (University of Alberta, Amii) | Embodiment and VLA (vision-language-action) execution: model-generated motion for commanded units |

