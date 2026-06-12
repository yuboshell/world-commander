---
marp: true
paginate: true
size: 16:9
title: "Command at the Speed of Thought"
---

<style>
/* ── Keynote-White theme ─────────────────────────────────────────────────── */
section {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #1a1a1a;
  background: #ffffff;
  font-size: 24px;
  line-height: 1.36;
  padding: 46px 56px 54px 56px;
  justify-content: flex-start !important;   /* top-align all slides, beat default theme */
}
h1 {                                   /* slide title: white bg, thin rule */
  font-size: 33px;
  font-weight: 600;
  color: #000;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1.5px solid #c9c9c9;
}
a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
strong { font-weight: 600; }
ul, ol { margin: 0.25em 0; padding-left: 1.15em; }
li { margin: 0.20em 0; }
li > ul { margin-top: 0.18em; }
p { margin: 0.5em 0; }
code { font-size: 0.92em; background: #f0f0f0; padding: 0 4px; border-radius: 3px; }

/* booktabs-style rules: reset default-theme borders/zebra first, then add rules */
table { border-collapse: collapse; }
table, tr, th, td { border: none !important; background: transparent !important; }
th, td { padding: 3px 10px; text-align: left; vertical-align: top; }
table { border-top: 1.5px solid #333 !important; border-bottom: 1.5px solid #333 !important; }
thead th { border-bottom: 1px solid #333 !important; font-weight: 600; }

/* two-column scaffold; ratios set inline per slide */
.columns { display: grid; gap: 26px; align-items: start; }
.caption { font-size: 0.74em; color: #444; line-height: 1.28; margin-top: 6px; text-align: left; }

/* page number bottom-right as "current / total" */
section::after {
  content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
  font-size: 14px; color: #8a8a8a;
}

/* dense slides */
section.tight { font-size: 20px; line-height: 1.3; }
section.tight h1 { font-size: 30px; }
</style>

# Outline

**Command at the Speed of Thought**: natural-language-commanded strategy games under real-time compute budgets.

1. **Vision**: play a strategy game the way a commander works, by speaking.
2. **The research question**: what does language command cost at game speed?
3. **Prior work and the open gap.**
4. **The program**: three layers of research, four rungs of environments.
5. **Phase 1**: the first benchmark paper.
6. **Architecture, papers, collaboration, risks.**

Yubo Huang, June 2026. Full proposal: `PROPOSAL.md` in this repository.

---

# Vision: the Commander Interface

In a real-time strategy (RTS) game, most player effort is micromanagement: drag-selecting units, hunting icons, sustaining hundreds of actions per minute. The strategic thinking that makes the genre rewarding gets a fraction of the player's attention. The rest is manual labour forced by the interface.

The alternative division of work already exists in coding agents: the person speaks intent, agents execute, the person reviews and redirects. Applied to strategy games, the player becomes a commander: **watch, think, speak; subordinates execute.**

- The interface concept shipped in 2008: EndWar, a fully voice-commanded RTS, on a rigid 70-word grammar.
- Language models removed the grammar limit: free-form commands are now understood.
- What is still missing is **speed**: language models cannot yet act at game pace.

---

# The Research Question

**How much does natural-language command cost, in latency and memory, at game speed, and how can that cost be driven down?**

The evaluation philosophy, shared by every part of the program:

- Score systems by **performance as a function of latency budget and VRAM budget**: an efficiency frontier, not a single number.
- The clock never pauses. A decision that arrives late is a no-op, exactly as it is for a human player.

This is the question that decides whether the commander interface is buildable at all.

---

<!-- _class: tight -->
# Prior Work, and the Gap

**LLMs already play RTS through text.** TextStarCraft II (NeurIPS 2024): off-the-shelf models beat the level-5 built-in AI with chain-of-summarization prompting. Adaptive Command (arXiv 2025) adds a speech-interfaced strategic advisor for human players. Both sidestep real time by slowing or pausing the clock.

**Efficiency is the named open problem.** The ACM Computing Surveys review of LLM game agents lists low-latency control and growing context cost as core challenges. A 1.3M-parameter specialist beats LLMs up to 92,000 times larger at real-time DOOM, deciding in 31 ms: general models do not currently survive contact with a game clock.

**Efficiency methods are never evaluated where stakes are real.** KV-cache eviction (dropping old context to fit memory) is scored on perplexity and retrieval suites. No existing work evaluates eviction closed-loop inside a live game, where evicting the wrong memory loses the match minutes later.

**The gap, in one line**: a streaming game is the natural stress test for efficient-inference methods, and nobody has run it. The gap is named in public surveys; speed decides who fills it.

---

# The Program: Three Layers

| Layer | Function | Status |
|---|---|---|
| **Strategy** | An LLM commander reads the game-state stream and issues macro decisions under hard latency and KV-cache budgets | Phase 1 |
| **Foresight** | A compact entity-level world model answers the commander's counterfactual queries: "if the army pushes now, does the fight win?" | Phase 2 to 3 |
| **Embodiment** | Units execute commands with generated motion at crowd scale on a consumer GPU | Phase 2 to 3 |

Each layer is a publishable line of work; all share the budget-frontier evaluation.

---

<!-- _class: tight -->
# The Roadmap: Four Rungs, One Harness

| Rung | Environment | What it isolates |
|---|---|---|
| 0 | **Command arena**: colour-tagged agents in a minimal room, moving in discrete directions under streamed language commands | Per-entity command grounding against the clock: grounding accuracy, utterance-to-action latency, deadline misses, as command rate rises |
| 1 | **StarCraft II, clock unpaused** | Strategic judgment under latency and KV-cache budgets: the Phase 1 paper |
| 2 | **Multi-user arena**: several players command their own units from their own machines in one shared real-time world | Efficiency as competitiveness: does a fast small commander beat a slow large one head-to-head? |
| 3 | **The commander game** | Product north star, beyond the paper horizon |

The end-state game is a vision, not a deliverable: its role is to fix the two constraints every paper inherits, an unpausable clock and a hard compute budget. Each rung publishes on its own; the harness, command protocol, and metrics carry upward.

---

<!-- _class: tight -->
# Phase 1: the Wedge Benchmark

The wedge: a deliberately narrow, fast first paper that opens the agenda behind it. Here, a benchmark and empirical study: **can an LLM command at game speed, and which efficiency techniques preserve its judgment?** Built on the TextStarCraft II stack, with the clock unpaused, wall-clock decision deadlines, and a VRAM ceiling.

**Experimental variables**

- KV-cache policy: full cache, StreamingLLM sinks, H2O, SnapKV, OBCache (ICML 2026)
- Model scale and sparsity: 1B to 70B open-weight models, structurally pruned and quantized variants
- Architecture: monolithic commander vs a commander/executor split
- State encoding: plain text vs a learned tokenizer over structured game state

**Metrics**: win rate against fixed built-in AI levels as a function of (latency budget, VRAM budget); actions per minute, deadline misses, tokens per decision.

**Strategic-memory probes**: scripted scenarios where winning requires recalling information observed minutes earlier. They convert cache-eviction failures from abstract retrieval misses into observable lost games.

---

# Architecture: Slow Thinker, Fast Actors

The variable most likely to matter: **monolithic commander vs a commander/executor split**, a slow strategic model directing fast small executors.

Two independent lines of support:

- The DOOM result: a 1.3M-parameter specialist decides in 31 ms while far larger models miss the deadline. Small executors can hold the clock.
- Robotics arrived at the same shape: π0 (arXiv 2024) pairs a slow vision-language backbone with a fast action expert controlling at up to 50 Hz. A game is the cheap, safe place to iterate on that split.

**State tokenization**: game state is a structured, non-text modality (entities, positions, events). Following Graph Tokenization (ICLR 2026), train a byte-pair tokenizer on replay corpora; measure tokens per decision and latency at equal win rate. A compact state code shrinks every downstream cost.

---

<!-- _class: tight -->
# The Papers This Produces

| Paper | The question it answers | Who cares, independent of the game |
|---|---|---|
| Real-time commander benchmark (Phase 1) | Which efficiency methods survive a closed-loop game clock? | KV-cache and pruning researchers: their methods are never scored by win rate |
| Game-state tokenizer | Does byte-pair tokenization extend to entity and event streams? | The tokenization-beyond-text programme |
| Command-arena benchmark (rung 0) | How does per-entity grounding degrade as command rate rises? | Real-time agent and interactive-systems researchers |
| Competitive-efficiency study (rung 2) | Does a fast small commander beat a slow large one? Rating vs compute budget | Inference-efficiency and agents communities |
| Crowd motion under budget (embodiment) | Can language-commanded full-body crowds run in real time on one GPU? | Motion-generation and graphics community |

The test each paper must pass: it answers a question its community already cares about, while caring nothing about the game.

---

# Collaboration, Risks, Open Questions

**Why this collaboration.** The wedge needs two things at once: the efficiency-methods stack (cache eviction, structured pruning, tokenization beyond text), where Dr. Diao's recent work supplies methods and baselines, and benchmark engineering plus genuine RTS fluency. The combination is rare: agent-interface groups lack the efficiency depth; efficiency groups evaluate on static corpora.

**Risks**

- Environment engineering is real work: mitigated by inheriting the TextStarCraft II stack.
- The gap is named in public surveys and could be filled by others: the first paper rewards being first more than being perfect.
- Latency results age as inference gets cheaper: the framing, performance vs budget, remains meaningful regardless of which model currently wins.

**Open questions**: venue and timing (ICLR vs NeurIPS 2027); whose GPUs run the frontier sweep; tokenizer inside the first paper or standalone; DreamSoul product interest beyond the papers.
