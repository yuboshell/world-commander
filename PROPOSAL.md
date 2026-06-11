# Command at the Speed of Thought

Natural-language-commanded strategy games under real-time compute budgets.

Draft research agenda for discussion. Yubo Huang, 2026-06-10.

## Vision

In a real-time strategy (RTS) game, most of a player's effort goes into micromanagement: drag-selecting units, hunting for icons, sustaining hundreds of actions per minute across keyboard and mouse. The strategic thinking that makes these games rewarding occupies a fraction of the player's attention; the rest is manual labor that the interface forces onto the human.

The alternative interface already exists in another domain. Working with coding agents, a person speaks an intent, an agent executes the low-level operations, and the person reviews and redirects. The same division of labor applied to strategy games turns the player into a commander: watch, think, speak; subordinates execute. Tom Clancy's EndWar shipped a fully voice-commanded RTS in 2008 on a rigid 70-word grammar ([Wikipedia](https://en.wikipedia.org/wiki/Tom_Clancy's_EndWar)), so the interface concept predates modern language models by 15 years. What was missing then was free-form language understanding. What is missing now is speed: language models understand the commands but cannot act at game pace.

This agenda asks the question that decides whether the commander interface is buildable: how much does natural-language command cost, in latency and memory, at game speed, and how can that cost be driven down?

## Background

Three lines of prior work frame the opportunity.

LLM agents already play RTS games through text interfaces. [TextStarCraft II (Ma et al., NeurIPS 2024)](https://arxiv.org/abs/2312.11865) wraps StarCraft II in a textual observation/action space; with chain-of-summarization prompting, off-the-shelf LLMs defeat the level-5 built-in AI ([code](https://github.com/histmeisah/Large-Language-Models-play-StarCraftII)). [SwarmBrain (Shao et al., 2024)](https://arxiv.org/pdf/2401.17749) takes a similar agent-as-player approach. [Adaptive Command (Ma et al., 2025)](https://arxiv.org/abs/2508.16580) adds the human back in: an LLM strategic advisor with a speech interface adjusts policy in StarCraft II, with the largest gains for novice players and players with disabilities. These systems establish feasibility but largely sidestep real-time constraints by slowing or pausing the game clock.

Efficiency is documented as the open problem. The [ACM Computing Surveys survey of LLM game agents](https://arxiv.org/abs/2404.02039) ([paper list](https://github.com/git-disl/awesome-LLM-game-agent-papers)) names low-latency control and the cost of ever-growing context as core challenges. A recent result makes the point concrete: a [1.3M-parameter specialized model outperforms LLMs up to 92,000x larger at real-time DOOM](https://arxiv.org/abs/2604.07385), deciding in 31 ms while the LLMs mostly fail to act in time. General-purpose language models do not currently survive contact with a game clock.

Efficiency methods are never evaluated where the stakes are real. KV-cache eviction and compression methods are scored on perplexity, retrieval suites, and recently [reasoning benchmarks](https://arxiv.org/html/2512.12008v1) or [learned-eviction setups](https://arxiv.org/abs/2602.10238). No existing work evaluates cache eviction closed-loop inside a live game, where evicting the wrong memory loses the match minutes later. A streaming game is arguably the most natural stress test for these methods: context grows continuously, history matters non-uniformly, and the ground-truth metric (win or lose) is external to the model.

## Research program: three layers

The commander interface decomposes into a stack, each layer a publishable line of work sharing one evaluation philosophy: performance as a function of latency and memory budget.

| Layer | Function | Status |
|---|---|---|
| Strategy | An LLM commander reads the game state stream and issues macro decisions under hard latency and KV-cache budgets | Phase 1 (wedge) |
| Foresight | A compact entity-level world model answers the commander's counterfactual queries ("if the army pushes now, does the fight win?") | Phase 2-3 |
| Embodiment | Units execute commands with generated motion at crowd scale on a consumer GPU | Phase 2-3 |

## Roadmap: from arena to game

The end state — a full commander-interface strategy game in the spirit of Age of Empires — is a product vision, years out, and not the deliverable. Its role is to fix the two constraints every paper inherits: an unpausable clock and a hard compute budget. The path toward it is a ladder of environments sharing one harness, one command protocol, and one evaluation philosophy; each rung isolates a measurable question that publishes on its own.

| Rung | Environment | What it isolates |
|---|---|---|
| 0 | Command arena: color-tagged agents in a minimal room move in discrete directions under streamed language commands, no motion detail | Per-entity command grounding against the clock: grounding accuracy, utterance-to-action latency, deadline misses as command rate rises |
| 1 | StarCraft II, clock unpaused | Strategic judgment under latency and KV-cache budgets (the Phase 1 wedge) |
| 2 | Multi-user arena: several players command their own units from their own machines in one shared real-time world | Efficiency as competitiveness: matches between efficiency configurations (Phase 3) |
| 3 | The commander game | Product north star, beyond the paper horizon |

The arena costs weeks, not months: no game engineering, no motion data, agents that simply move. Single commands are trivially easy for any modern model — by design; the test is the stream. Difficulty rises along three axes: command rate, compositional addressing ("everyone except the yellow one, gather at the door"), and commands that depend on remembered state ("the one who was sitting earlier — move him west"). Building the arena first validates the streaming-command infrastructure and latency protocol that every later rung, including the wedge, reuses. It is also where the embodiment layer eventually lands: swap discrete moves for generated full-body motion at crowd scale, and the harness and metrics carry over unchanged.

Rung 2 changes what latency means: in a competitive match it stops being a constraint to measure and becomes what decides the winner. The headline question — does a fast small commander beat a slow large one head-to-head? — turns the efficiency frontier into Elo-style ratings (chess's system for ranking players by match outcomes), an evaluation no static corpus can imitate. Multi-user play also surfaces the systems questions — per-client inference versus a shared server budget, fairness across heterogeneous player hardware — that extend the Phase 2 scheduling line.

## Phase 1: the wedge paper

A benchmark and empirical study: can an LLM command at game speed, and which efficiency techniques preserve its judgment?

Environment. Build on the TextStarCraft II / [LLM-PySC2](https://arxiv.org/pdf/2411.05348) stack with one decisive change: the game clock does not pause. The harness enforces wall-clock decision deadlines and a VRAM ceiling; a late decision is a no-op, as it is for a human.

Experimental variables.

- KV-cache policy: full cache, [StreamingLLM](https://arxiv.org/abs/2309.17453)-style attention sinks, H2O (Zhang et al., 2023), SnapKV (Li et al., 2024), and [OBCache](https://arxiv.org/abs/2510.07651), treating the game-state stream as the long context.
- Model scale and sparsity: open-weight models from 1B to 70B, plus structurally pruned variants (GISP, RESP) and quantized variants.
- Architecture: monolithic commander versus a commander/executor split (slow strategic model, fast small executors), the architecture suggested by the DOOM result.
- State encoding: plain-text serialization versus a learned tokenizer over structured game state (see below).

Metrics. Win rate against fixed built-in AI levels as a function of (decision latency budget, VRAM budget): an efficiency frontier rather than a single score. Secondary: actions issued per minute, decision deadline misses, tokens per decision.

Strategic-memory probes. Scripted scenarios where winning requires recalling information observed minutes earlier (scouted tech switches, hidden expansions). These convert cache-eviction failures from abstract retrieval misses into observable lost games, and give eviction methods a task-grounded report card no perplexity benchmark provides.

State tokenization module. Game state is a structured, non-text modality: entities, positions, event streams. Following the program of extending byte-pair-style tokenization beyond text ([Graph Tokenization, ICLR 2026](https://www.diaoenmao.com)), train a tokenizer on StarCraft II replay corpora and measure tokens-per-decision and end-to-end latency at equal win rate against text serialization. A compact state code shrinks every downstream cost in the stack.

Deliverables: the open-source harness and benchmark, the efficiency-frontier study, and the memory-probe suite.

## Phase 2: methods

Whatever Phase 1 exposes as the bottleneck becomes the method work. Candidates: game-aware KV eviction that exploits entity lifetimes and spatial locality; learned state tokenizers trained jointly with the policy; distilled small commanders trained on large-model match traces; commander/executor scheduling under a shared GPU budget.

## Phase 3: toward the real interface

Reintroduce the human. A voice-commanded mode (the commander speaks, agents execute) evaluated on intent throughput, cognitive load, and accessibility, extending what Adaptive Command began — then humans, plural: the multi-user arena (roadmap rung 2), where matches between players turn efficiency into competitiveness. In parallel, the foresight and embodiment layers mature: entity-level world models for in-game counterfactuals (cheaper, queryable analogues of [WHAM](https://www.nature.com/articles/s41586-025-08600-3)-style gameplay models), and crowd-scale language-conditioned motion generation under compute budgets, building on the real-time text-to-motion line ([MotionLCM](https://arxiv.org/pdf/2404.19759), [MotionStreamer](https://arxiv.org/pdf/2503.15451), [CrowdMoGen](https://yukangcao.github.io/CrowdMoGen/)). These layers align with motion-generation and character-world-model research directions in Yubo's prospective PhD work and are listed here as the agenda's growth surface rather than Phase 1 commitments.

## Paper inventory

The program is research-first: the game is the north star, the papers are the milestones. The test each paper must pass is answering a question its community already cares about while caring nothing about the game; the budget-frontier evaluation is what passes it.

| Paper | The question | Who cares, independent of the game |
|---|---|---|
| Real-time commander benchmark (the Phase 1 wedge) | Which efficiency methods survive a closed-loop game clock? | KV-cache and pruning researchers, whose methods are scored on static corpora today, never by win rate |
| Game-state tokenizer (inside the wedge or standalone — open question 3) | Does byte-pair tokenization extend to entity and event streams, and what does a compact state code buy at equal win rate? | The tokenization-beyond-text program |
| Command-arena benchmark (rung 0) | How does per-entity command grounding degrade as command rate rises against a hard clock? | Real-time agent and interactive-systems researchers |
| Competitive-efficiency study (rung 2) | Does a fast small commander beat a slow large one head-to-head — Elo as a function of compute budget? | Inference-efficiency and agents communities; an evaluation-paradigm result |
| Crowd motion under budget (embodiment layer) | Can language-commanded full-body crowds run in real time on one consumer GPU? | The motion-generation and graphics community |

Benchmark papers live or die on adoption: open source, one-command install, credible baselines — the Phase 1 deliverables are scoped with that in mind.

## Why this collaboration

The wedge paper needs two things at once: the efficiency-methods stack (cache eviction, structured pruning, tokenization beyond text), where Dr. Diao's recent work supplies both methods and baselines, and benchmark/harness engineering plus genuine RTS fluency, which Yubo brings. The niche is defensible because this combination is rare: agent-interface groups lack the efficiency depth, and efficiency groups evaluate on static corpora rather than closed-loop games.

## Risks

- Environment engineering on StarCraft II is real work; mitigated by inheriting the TextStarCraft II stack rather than building from scratch.
- The "KV eviction in closed-loop games" gap could be filled by others; the surveys already name it, so the wedge paper should move fast.
- Latency results age as inference gets cheaper; the benchmark's framing (performance versus budget) remains meaningful regardless of which model currently wins.

## Open questions for discussion

1. Venue and timing for the wedge paper (ICLR 2027 versus a slower, stronger NeurIPS 2027 submission).
2. Model scale and compute: which open-weight families, and on whose GPUs the frontier sweep runs.
3. Whether the state-tokenization module belongs in the wedge paper or stands alone as a second paper.
4. Whether DreamSoul has product interest in the commander interface beyond the papers.
