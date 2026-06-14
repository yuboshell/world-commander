# World Commander

Natural-language command of agent crowds in strategy games, under real-time compute budgets.

Draft research agenda for discussion. Yubo Huang, 2026-06-10.

## Vision

In a real-time strategy (RTS) game, most of a player's effort goes into micromanagement: drag-selecting units, hunting for icons, sustaining hundreds of actions per minute across keyboard and mouse. The strategic thinking that makes these games rewarding occupies a fraction of the player's attention; the rest is manual labor that the interface forces onto the human.

The alternative interface already exists in another domain. Working with coding agents, a person speaks an intent, an agent executes the low-level operations, and the person reviews and redirects. The same division of labor applied to strategy games turns the player into a commander: watch, listen, think, speak; subordinates execute. Tom Clancy's EndWar shipped a fully voice-commanded RTS in 2008 on a rigid 70-word grammar ([Wikipedia](https://en.wikipedia.org/wiki/Tom_Clancy's_EndWar)), so the interface concept predates modern language models by 15 years. What was missing then was free-form language understanding. What is missing now is speed: language models understand the commands but cannot act at game pace.

This agenda asks the question that decides whether the commander interface is buildable: how much does natural-language command cost, in latency and memory, at game speed, and how can that cost be driven down?

## Background

Three lines of prior work frame the opportunity.

LLM agents already play RTS games through text interfaces. [TextStarCraft II (Ma et al., NeurIPS 2024)](https://arxiv.org/abs/2312.11865) wraps StarCraft II in a textual observation/action space; with chain-of-summarization prompting, off-the-shelf LLMs defeat the level-5 built-in AI ([code](https://github.com/histmeisah/Large-Language-Models-play-StarCraftII)). [SwarmBrain (Shao et al., 2024)](https://arxiv.org/pdf/2401.17749) takes a similar agent-as-player approach. [Adaptive Command (Ma et al., 2025)](https://arxiv.org/abs/2508.16580) adds the human back in: an LLM strategic advisor with a speech interface adjusts policy in StarCraft II, with the largest gains for novice players and players with disabilities. These systems establish feasibility but largely sidestep real-time constraints by slowing or pausing the game clock.

Efficiency is documented as the open problem. The [ACM Computing Surveys survey of LLM game agents](https://arxiv.org/abs/2404.02039) ([paper list](https://github.com/git-disl/awesome-LLM-game-agent-papers)) devotes a section (§8.1, "Action Games: Low-Latency Response") to it — "the core challenge is low-latency response, which shapes agent design by requiring fast action and hybrid architectures that reconcile LLM reasoning with frame-level responsiveness" — and lists memory among its open challenges (§9.1). A recent result makes the point concrete: a [1.3M-parameter specialized model outperforms LLMs up to 92,000x larger at real-time DOOM](https://arxiv.org/abs/2604.07385), deciding in 31 ms while the LLMs mostly fail to act in time. General-purpose language models do not currently survive contact with a game clock.

Efficiency methods are never evaluated where the stakes are real. KV-cache eviction and compression methods are scored on perplexity, retrieval suites, and recently [reasoning benchmarks](https://arxiv.org/html/2512.12008v1) or [learned-eviction setups](https://arxiv.org/abs/2602.10238). No existing work evaluates cache eviction closed-loop inside a live game, where evicting the wrong memory loses the match minutes later. A streaming game is arguably the most natural stress test for these methods: context grows continuously, history matters non-uniformly, and the ground-truth metric (win or lose) is external to the model.

## The three jobs

The **human is the strategic commander**; the LLM-driven system carries the orders out. It needs three capabilities, separate lines of work that will eventually run together, sharing one evaluation philosophy: performance as a function of latency and memory budget.

| Job | What it does |
|---|---|
| **Execute** | An LLM turns the commander's spoken intent into the right in-game actions, in real time, under hard latency and memory budgets |
| **Foresee** | A compact world model the commander can query before committing ("if the army pushes now, does the fight win?") |
| **Embody** | Units carry out the actions with model-generated motion (synthesized for the order, not replayed animation clips) at crowd scale on one consumer GPU |

This proposal is about getting **Execute** right first. **Foresee** and **Embody** are the growth surface, built in the later phases and aligned with motion-generation and world-model research directions in Yubo's prospective PhD work. Note the LLM is the *executor* of the commander's intent, not an autonomous strategist: in Phase 1 the commander is a scripted command stream, so the benchmark isolates how well and how cheaply the LLM carries orders out, not whose strategy is better. (Earlier framings that scored an "LLM commander" by win rate are superseded; see the discussion log.)

## The plan: three phases

The three jobs above are the *parts*; the three phases below are the *order*. We build in increasingly complex environments, with one shared **harness** under all of them — the command protocol, the unpausable clock, deadline enforcement, and metric logging — so the engineering and the evaluation transfer upward.

| Phase | Focus | What happens |
|---|---|---|
| **Phase 1** | Benchmarks | Build the harness and the efficiency-frontier evaluation, on two testbeds: a command arena (warm-up) and StarCraft II with the clock unpaused (the flagship wedge). |
| **Phase 2** | Methods | Attack whatever Phase 1 exposes as the bottleneck: game-aware eviction, a learned state tokenizer, distilled commanders, commander/executor scheduling. |
| **Phase 3** | The real interface | Reintroduce the human (voice command), then humans plural (multiplayer competition); grow the Foresee and Embody jobs. |

The environments grow with the phases, simplest to hardest:

> a toy room (abstract agents)  →  StarCraft II  →  multiplayer  →  a full game

The end state, a full commander-interface game in the spirit of Age of Empires, is a product vision years out, not a deliverable. Its role is to fix the two constraints every paper inherits: an unpausable clock and a hard compute budget.

## Phase 1: the benchmark (the wedge)

The **wedge** is a deliberately narrow, fast first paper that opens the agenda behind it. It builds the harness and asks: can an LLM command at game speed, and which efficiency techniques preserve its judgment? Two testbeds.

**The command arena (warm-up).** Color-tagged agents in a minimal room move in discrete directions under streamed language commands, with no motion detail and no game engineering. It costs weeks, not months, and proves out the streaming-command infrastructure that StarCraft II and every later phase reuse. One command is trivially easy for any modern model, by design; the test is the *stream*. Difficulty rises along three axes: command rate, compositional addressing ("everyone except the yellow one, gather at the door"), and commands that depend on remembered state ("the one who was sitting earlier, move west"). Measured: command-grounding accuracy, utterance-to-action latency, and deadline misses as command rate rises.

**StarCraft II, clock unpaused (flagship).** Build on the TextStarCraft II / [LLM-PySC2](https://arxiv.org/pdf/2411.05348) stack with one decisive change: the game clock does not pause. The harness enforces wall-clock decision deadlines and a VRAM ceiling; a late decision simply does not happen, as it is for a human.

Experimental variables.

- KV-cache policy: full cache, [StreamingLLM](https://arxiv.org/abs/2309.17453)-style attention sinks, H2O (Zhang et al., 2023), SnapKV (Li et al., 2024), and [OBCache](https://arxiv.org/abs/2510.07651), treating the game-state stream as the long context.
- Model scale and sparsity: open-weight models from 1B to 70B, plus structurally pruned variants (GISP, RESP) and quantized variants.
- Architecture: monolithic commander versus a commander/executor split (slow strategic model, fast small executors), the architecture suggested by the DOOM result and, in robotics, by vision-language-action models: [π0](https://arxiv.org/abs/2410.24164) pairs a slow vision-language backbone with a fast action expert controlling at up to 50 Hz.
- State encoding: plain-text serialization versus a learned tokenizer over structured game state (see below).

Metrics. Win rate against fixed built-in AI levels as a function of (decision latency budget, VRAM budget): an efficiency frontier rather than a single score. Secondary: actions issued per minute, decision deadline misses, tokens per decision.

Strategic-memory probes. Scripted scenarios where winning requires recalling information observed minutes earlier (scouted tech switches, hidden expansions). These convert cache-eviction failures from abstract retrieval misses into observable lost games, and give eviction methods a task-grounded report card no perplexity benchmark provides.

State tokenization module. Game state is a structured, non-text modality: entities, positions, event streams. Following the program of extending byte-pair-style tokenization beyond text ([Graph Tokenization, ICLR 2026](https://www.diaoenmao.com)), train a tokenizer on StarCraft II replay corpora and measure tokens-per-decision and end-to-end latency at equal win rate against text serialization. A compact state code shrinks every downstream cost in the stack.

Deliverables: the open-source harness and the two benchmarks, the efficiency-frontier study, and the memory-probe suite.

## Phase 2: methods

Whatever Phase 1 exposes as the bottleneck becomes the method work. Candidates: game-aware KV eviction that exploits entity lifetimes and spatial locality; learned state tokenizers trained jointly with the policy; distilled small commanders trained on large-model match traces; commander/executor scheduling under a shared GPU budget.

## Phase 3: the real interface

Reintroduce the human. A voice-commanded mode (the commander speaks, agents execute) evaluated on intent throughput, cognitive load, and accessibility, extending what Adaptive Command began. Then humans, plural: a multiplayer arena where several players command their own units from their own machines in one shared real-time world. There, latency stops being a constraint to measure and becomes what decides the winner. The headline question — does a fast small commander beat a slow large one head-to-head? — turns the efficiency frontier into Elo-style ratings (chess's system for ranking players by match outcomes), an evaluation no static corpus can imitate, and surfaces the systems questions (per-client inference versus a shared server budget, fairness across heterogeneous player hardware) that extend the Phase 2 scheduling line.

In parallel, the Foresee and Embody jobs mature: entity-level world models for in-game counterfactuals (cheaper, queryable analogues of [WHAM](https://www.nature.com/articles/s41586-025-08600-3)-style gameplay models), and crowd-scale language-conditioned motion generation under compute budgets, building on the real-time text-to-motion line ([MotionLCM](https://arxiv.org/pdf/2404.19759), [MotionStreamer](https://arxiv.org/pdf/2503.15451), [CrowdMoGen](https://yukangcao.github.io/CrowdMoGen/)). For the motion-generation community, this reads as real-time control of multiple virtual characters.

## Paper inventory

The program is research-first: the game is the north star, the papers are the milestones. The test each paper must pass is to answer a question its community already cares about while caring nothing about the game; the budget-frontier evaluation is what passes it. Papers are listed roughly in build order.

| Paper | Phase | The question | Who cares, independent of the game |
|---|---|---|---|
| Command-arena benchmark | 1 | How does per-entity command grounding degrade as command rate rises against a hard clock? | Real-time agent and interactive-systems researchers |
| Real-time commander benchmark (the wedge) | 1 | Which efficiency methods survive a closed-loop game clock? | KV-cache and pruning researchers, whose methods are scored on static corpora today, never by win rate |
| Game-state tokenizer | 1 to 2 | Does byte-pair tokenization extend to entity and event streams, and what does a compact state code buy at equal win rate? | The tokenization-beyond-text program |
| Competitive-efficiency study | 3 | Does a fast small commander beat a slow large one head-to-head, Elo as a function of compute budget? | Inference-efficiency and agents communities; an evaluation-paradigm result |
| Crowd motion under budget | 3 | Can language-commanded full-body crowds run in real time on one consumer GPU? | The motion-generation and graphics community |

Whether the game-state tokenizer ships inside the wedge or stands alone as a second paper is an open question (below). Benchmark papers live or die on adoption: open source, one-command install, credible baselines, all of which the Phase 1 deliverables are scoped for.

## Why this collaboration

The wedge needs two things at once: the efficiency-methods stack (cache eviction, structured pruning, tokenization beyond text), where Dr. Diao's recent work supplies both methods and baselines, and benchmark/harness engineering plus genuine RTS fluency, which Yubo brings. The niche is defensible because this combination is rare: agent-interface groups lack the efficiency depth, and efficiency groups evaluate on static corpora rather than closed-loop games.

## Risks

- Environment engineering on StarCraft II is real work; mitigated by inheriting the TextStarCraft II stack rather than building from scratch.
- The "KV eviction in closed-loop games" gap could be filled by others; the surveys already name it, so the wedge should move fast.
- Latency results age as inference gets cheaper; the benchmark's framing (performance versus budget) remains meaningful regardless of which model currently wins.

## Discussion log

**2026-06-11 — first round with Dr. Diao (WeChat).** Direction endorsed. Three signals, folded back into the agenda:

- Latency is the fight: large-model control is slow against the speed that mouse control demands. This is the wedge's thesis restated as a concern — the benchmark exists to measure exactly that gap and what closes it.
- Architecture pointer: borrow from robot vision-language-action models (the [π0](https://arxiv.org/abs/2410.24164) line), where a slow vision-language backbone drives a fast action expert at real-time rates. Added to the Phase 1 architecture variable; a game is the cheaper, safer place to iterate on the same split.
- "Essentially RL in a virtual world": the long arc runs through reinforcement learning, so RL literacy is a prerequisite to build. Phase 1 itself needs no RL training (off-the-shelf and pruned models, prompted), but learned executors, the Foresee job, and any trained policy do. Near-term action: survey RL fundamentals and consult RL colleagues.

**2026-06-13 — executor framing (to confirm with Dr. Diao).** The human is the strategic commander; the LLM is the *executor* of that intent, not an autonomous strategist. Earlier framing (inherited from TextStarCraft II) scored an "LLM commander" by win rate, which conflicts with the human-as-commander vision. Resolution: in Phase 1 the commander is a scripted command stream, and the benchmark measures how well and how cheaply the LLM carries orders out — command-following in the arena, and win rate while executing a fixed strategy in StarCraft II. Renamed the "Decide" job to **Execute**, and Foresee is a what-if advisor the commander queries. This changes what the benchmark measures, so it is the next thing to put to Dr. Diao (his efficiency methods are scored by whichever metric). Project also renamed to **World Commander**.

## Open questions for discussion

1. Venue and timing for the wedge paper (ICLR 2027 versus a slower, stronger NeurIPS 2027 submission).
2. Model scale and compute: which open-weight families, and on whose GPUs the frontier sweep runs.
3. Whether the state-tokenization module belongs in the wedge paper or stands alone as a second paper.
4. Whether DreamSoul has product interest in the commander interface beyond the papers.
