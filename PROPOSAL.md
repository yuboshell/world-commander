# World Commander

Natural-language command of agent crowds in real-time strategy games, under latency and memory budgets.

Draft research program for discussion. Yubo Huang, 2026-06-10.

## Vision

In a real-time strategy (RTS) game, most of a player's effort goes into micromanagement: drag-selecting units, hunting for icons, sustaining hundreds of actions per minute across keyboard and mouse. The strategic thinking that makes these games rewarding occupies a fraction of the player's attention; the rest is manual labor that the interface forces onto the human.

The alternative interface already exists in another domain. Working with coding agents, a person speaks an intent, an agent executes the low-level operations, and the person reviews and redirects. The same division of labor applied to strategy games turns the player into a commander: watch, listen, think, speak; subordinates execute. Tom Clancy's EndWar shipped a fully voice-commanded RTS in 2008 on a rigid 70-word grammar ([Wikipedia](https://en.wikipedia.org/wiki/Tom_Clancy's_EndWar)), so the interface concept predates modern language models by 15 years. What was missing then was free-form language understanding. What is missing now is speed: language models understand the commands but cannot act at game pace.

This program asks the question that decides whether the commander interface is buildable: how much does natural-language command cost, in latency and memory, at game speed, and how can that cost be driven down?

## Related work

Three lines of prior work frame the opportunity.

Full reinforcement learning already mastered StarCraft II: [AlphaStar (Vinyals et al., Nature 2019)](https://www.nature.com/articles/s41586-019-1724-z) reached Grandmaster rank, but as an autonomous policy trained at datacentre scale with no language in the loop, orthogonal to the language-command axis this program takes. Closer to that axis, LLM agents already play RTS games through text interfaces. [TextStarCraft II (Ma et al., NeurIPS 2024)](https://arxiv.org/abs/2312.11865) wraps StarCraft II in a textual observation/action space; with chain-of-summarization prompting, off-the-shelf LLMs defeat the level-5 built-in AI ([code](https://github.com/histmeisah/Large-Language-Models-play-StarCraftII)). [SwarmBrain (Shao et al., 2024)](https://arxiv.org/pdf/2401.17749) takes a similar agent-as-player approach. [Adaptive Command (Ma et al., 2025)](https://arxiv.org/abs/2508.16580) adds the human back in: an LLM strategic advisor with a speech interface adjusts policy in StarCraft II, with the largest gains for novice players and players with disabilities. [HLA (Liu et al., AAMAS 2024)](https://arxiv.org/abs/2312.15224) adds a slow-mind / fast-mind / executor hierarchy for real-time human-AI coordination in a cooperative game, and [AVA (Ma et al., 2026)](https://arxiv.org/abs/2503.05383) drives a screenshot-based VLM commander in StarCraft II at roughly 2 Hz; [CivRealm (Qi et al., ICLR 2024)](https://arxiv.org/abs/2401.10568) pairs RL and LLM agents in the turn-based strategy game Freeciv. These systems establish feasibility but sidestep the real-time constraint by slowing, pausing, or staying turn-based.

Efficiency is documented as the open problem. The [ACM Computing Surveys survey of LLM game agents](https://arxiv.org/abs/2404.02039) ([paper list](https://github.com/git-disl/awesome-LLM-game-agent-papers)) devotes a section (§8.1, "Action Games: Low-Latency Response") to it — "the core challenge is low-latency response, which shapes agent design by requiring fast action and hybrid architectures that reconcile LLM reasoning with frame-level responsiveness" — and lists memory among its open challenges (§9.1). A recent result makes the point concrete: a [1.3M-parameter specialized model outperforms LLMs up to 92,000x larger at real-time DOOM](https://arxiv.org/abs/2604.07385), deciding in 31 ms while the LLMs mostly fail to act in time. General-purpose language models do not currently survive contact with a game clock. Two recent benchmarks measure this directly ([VideoGameBench (Zhang et al., 2025)](https://arxiv.org/abs/2505.18134), where frontier models drop from 1.6% to 0.48% completion once the clock keeps running, and [AgileThinker (Wen et al., 2025)](https://arxiv.org/abs/2511.04898), a real-time-reasoning gym), confirming latency as the wall, though on single agents rather than the efficiency methods.

Efficiency methods are never evaluated where the stakes are real. KV-cache eviction and compression methods are scored on perplexity, retrieval suites, and recently [reasoning benchmarks](https://arxiv.org/html/2512.12008v1) or [learned-eviction setups](https://arxiv.org/abs/2602.10238); under multi-instruction prompting, eviction has been shown to silently drop specific instructions ([Pitfalls of KV Cache Compression, ACL 2026](https://arxiv.org/abs/2510.00231)), and action-level speculative decoding has only just reached agentic loops ([Speculative Actions, 2025](https://arxiv.org/abs/2510.04371)). No existing work evaluates cache eviction closed-loop inside a live game, where evicting the wrong memory loses the match minutes later. A streaming game is arguably the most natural stress test for these methods: context grows continuously, history matters non-uniformly, and the ground-truth metric (win or lose) is external to the model.

## The system: commander and executor

The **human is the strategic commander**; the LLM-driven system carries the orders out. The whole near-term effort is one capability, **execution**: an LLM turning the commander's spoken intent into the right in-game actions, in real time, under hard latency and memory budgets, evaluated as performance against that budget.

The LLM is the *executor* of the commander's intent, not an autonomous strategist: in Phase 1 the commander is a scripted command stream, so the benchmark isolates how well and how cheaply the LLM carries orders out, not whose strategy is better. (Earlier framings that scored an "LLM commander" by win rate are superseded; see the discussion log.)

Execution is the spine of every phase below. One direction sits further out and stays in view because it defines the end-state experience: **embodiment**, units carrying out orders with model-generated motion (synthesized for the order, not replayed animation clips) at crowd scale on one consumer GPU, aligned with the motion-generation direction in Yubo's prospective PhD work. It appears in Phase 3 and as one project in the inventory, not as near-term work.

## The plan: three phases

We build in increasingly complex environments, with one shared **harness** under all of them (the command protocol, the unpausable clock, deadline enforcement, and metric logging), so the engineering and the evaluation transfer upward.

| Phase | Focus | What happens |
|---|---|---|
| **Phase 1** | Benchmarks | Build the harness and the efficiency-frontier evaluation, on two testbeds: a command arena (warm-up) and StarCraft II with the clock unpaused (the first project). |
| **Phase 2** | Methods | Attack whatever Phase 1 exposes as the bottleneck: game-aware eviction, a learned state tokenizer, distilled commanders, commander/executor scheduling. |
| **Phase 3** | The real interface | Reintroduce the human (voice command), then humans plural (multiplayer competition); grow toward embodiment (crowd-scale motion). |

The environments grow with the phases, simplest to hardest:

> a toy room (abstract agents)  →  StarCraft II  →  multiplayer  →  a full game

The end state, a genuinely new kind of video game played by command rather than by frantic input, is a product vision years out, not a deliverable. We start with strategy (the best testbed), but the voice-command interface is not bound to one genre: the long-term goal is a revolutionary game, not a strategy game specifically. Its role here is to fix the two constraints every project inherits: an unpausable clock and a hard compute budget.

## Phase 1: the benchmark (the first project)

The **first project** is deliberately narrow and fast, the entry point that opens the program behind it. It builds the harness and asks: can an LLM command at game speed, and which efficiency techniques preserve its judgment? Two testbeds.

**The command arena (warm-up).** Color-tagged agents in a minimal room move in discrete directions under streamed language commands, with no motion detail and no game engineering. It costs weeks, not months, and proves out the streaming-command infrastructure that StarCraft II and every later phase reuse. One command is trivially easy for any modern model, by design; the test is the *stream*. The room is not single-sided: a few uncontrolled agents move on their own clock, so that a late command concedes ground, the way a slow decision concedes to an opponent in a real game. Difficulty rises along three axes: command rate, compositional addressing ("everyone except the yellow one, gather at the door"), and commands that depend on remembered state ("the one I sent west earlier, now move it north"). Measured: command-grounding accuracy, utterance-to-action latency, and deadline misses as command rate rises.

**StarCraft II, clock unpaused (the first project).** Build on the TextStarCraft II / [LLM-PySC2](https://arxiv.org/pdf/2411.05348) stack with one decisive change: the game clock does not pause. The harness enforces wall-clock decision deadlines and a VRAM ceiling; a late decision simply does not happen, as it is for a human.

Experimental variables.

- KV-cache policy: full cache, [StreamingLLM](https://arxiv.org/abs/2309.17453)-style attention sinks, H2O (Zhang et al., 2023), SnapKV (Li et al., 2024), and [OBCache](https://arxiv.org/abs/2510.07651), treating the game-state stream as the long context.
- Model scale and sparsity: open-weight models from 1B to 70B, plus structurally pruned variants (GISP, RESP) and quantized variants.
- Architecture: monolithic commander versus a commander/executor split (slow strategic model, fast small executors), the architecture suggested by the DOOM result and, in robotics, by vision-language-action models: [π0](https://arxiv.org/abs/2410.24164) pairs a slow vision-language backbone with a fast action expert controlling at up to 50 Hz, and [HLA (AAMAS 2024)](https://arxiv.org/abs/2312.15224) and [DPT-Agent (ACL 2025)](https://arxiv.org/abs/2502.11882) instantiate the same slow/fast split for real-time agents in games.
- State encoding: plain-text serialization versus a learned tokenizer over structured game state (see below).

Metrics. Win rate against fixed built-in AI levels as a function of (decision latency budget, VRAM budget): an efficiency frontier rather than a single score. Secondary: actions issued per minute, decision deadline misses, tokens per decision.

Strategic-memory probes. Scripted scenarios where winning requires recalling information observed minutes earlier (scouted tech switches, hidden expansions). These convert cache-eviction failures from abstract retrieval misses into observable lost games, and give eviction methods a task-grounded report card no perplexity benchmark provides.

State tokenization module. Game state is a structured, non-text modality: entities, positions, event streams. Following the program of extending byte-pair-style tokenization beyond text ([Graph Tokenization, ICLR 2026](https://www.diaoenmao.com)), and learned discrete world-model tokenizers that already cut tokens-per-step ([IRIS, ICLR 2023](https://arxiv.org/abs/2209.00588); [Δ-IRIS, ICML 2024](https://arxiv.org/abs/2406.19320)), train a tokenizer on StarCraft II replay corpora and measure tokens-per-decision and end-to-end latency at equal win rate against text serialization. A compact state code shrinks every downstream cost in the stack.

Deliverables: the open-source harness and the two benchmarks, the efficiency-frontier study, and the memory-probe suite.

**Near-term execution (practical staging).** Both testbeds are on the coarse (discrete-action) track, and both run now, in parallel, because neither needs model training: off-the-shelf and pruned models, prompted.

- *M0, the arena, on amax.* The E1 scaffold already exists; run it against a deployed model to produce the first drop-late frontier (command-grounding accuracy, utterance-to-action latency, deadline misses versus command rate). It de-risks the streaming-command and deadline harness with no game engineering.
- *M1, StarCraft II, on yubopc.* Stand up LLM-PySC2 with the clock unpaused; the LLM executes a fixed scripted strategy, so the benchmark isolates execution, not strategy. The headline metric is the deadline frontier, not raw win rate (which is confounded by the built-in auto-attack).
- *M2, one method.* Apply a single efficiency technique (KV-cache eviction, a distilled small commander, or speculative actions) to whatever M1 exposes as the binding cost, and show it moves the frontier at equal win rate.

The fine (continuous-motion) track stays deferred to Phase 3: it needs motion synthesis, real-time rendering, a synthetic-data pipeline, and abstract-intent grounding, none of which the coarse track requires. Starting coarse yields a shippable result while those problems remain open.

## Phase 2: methods

Whatever Phase 1 exposes as the bottleneck becomes the method work. Candidates: game-aware KV eviction that exploits entity lifetimes and spatial locality; learned state tokenizers trained jointly with the policy; distilled small commanders trained on large-model match traces; commander/executor scheduling under a shared GPU budget.

## Phase 3: the real interface

Reintroduce the human. A voice-commanded mode (the commander speaks, agents execute) evaluated on intent throughput, cognitive load, and accessibility, extending what Adaptive Command began. Then humans, plural: a multiplayer arena where several players command their own units from their own machines in one shared real-time world. There, latency stops being a constraint to measure and becomes what decides the winner. The headline question — does a fast small commander beat a slow large one head-to-head? — turns the efficiency frontier into Elo-style ratings (chess's system for ranking players by match outcomes), an evaluation no static corpus can imitate, and surfaces the systems questions (per-client inference versus a shared server budget, fairness across heterogeneous player hardware) that extend the Phase 2 scheduling line.

In parallel, **embodiment** matures: crowd-scale language-conditioned motion generation under compute budgets, building on the real-time motion-generation line ([MotionLCM](https://arxiv.org/pdf/2404.19759), [MotionStreamer](https://arxiv.org/pdf/2503.15451), [MotionBricks](https://arxiv.org/abs/2604.24833), [CrowdMoGen](https://yukangcao.github.io/CrowdMoGen/)). For the motion-generation community, this reads as real-time control of multiple virtual characters.

## Project inventory

The program is research-first: the game is the long-term goal, the projects are the milestones. Each project is a top-tier paper's worth of work, and the test each must pass is to answer a question its community already cares about while caring nothing about the game; the budget-frontier evaluation is what passes it. The command arena is a warm-up task, not a project, so it does not appear here. Projects are listed roughly in build order.

| Project | Phase | The question | Who cares, independent of the game |
|---|---|---|---|
| Real-time commander benchmark | 1 | Which efficiency methods survive a closed-loop game clock? | KV-cache and pruning researchers, whose methods are scored on static corpora today, never by win rate |
| Game-state tokenizer | 1 to 2 | Does byte-pair tokenization extend to entity and event streams, and what does a compact state code buy at equal win rate? | The tokenization-beyond-text program |
| Crowd motion under budget (embodiment) | 3 | Can language-commanded full-body crowds run in real time on one consumer GPU? | The motion-generation and graphics community |

Whether the game-state tokenizer ships inside the first project or stands alone as a second is an open question (below). Benchmark projects live or die on adoption: open source, one-command install, credible baselines, all of which the Phase 1 deliverables are scoped for.

## Why this collaboration

The first project needs two things at once: the efficiency-methods stack (cache eviction, structured pruning, tokenization beyond text), where Dr. Diao's recent work supplies both methods and baselines, and benchmark/harness engineering plus genuine RTS fluency, which Yubo brings. The niche is defensible because this combination is rare: agent-interface groups lack the efficiency depth, and efficiency groups evaluate on static corpora rather than closed-loop games.

## Risks

- Environment engineering on StarCraft II is real work; mitigated by inheriting the TextStarCraft II stack rather than building from scratch.
- The "KV eviction in closed-loop games" gap could be filled by others; the surveys already name it, so the first project should move fast.
- Latency results age as inference gets cheaper; the benchmark's framing (performance versus budget) remains meaningful regardless of which model currently wins.

## Discussion log

**2026-06-11 — first round with Dr. Diao (WeChat).** Direction endorsed. Three signals, folded back into the program:

- Latency is the fight: large-model control is slow against the speed that mouse control demands. This is the first project's thesis restated as a concern — the benchmark exists to measure exactly that gap and what closes it.
- Architecture pointer: borrow from robot vision-language-action models (the [π0](https://arxiv.org/abs/2410.24164) line), where a slow vision-language backbone drives a fast action expert at real-time rates. Added to the Phase 1 architecture variable; a game is the cheaper, safer place to iterate on the same split.
- "Essentially RL in a virtual world": the long arc runs through reinforcement learning, so RL literacy is a prerequisite to build. Phase 1 itself needs no RL training (off-the-shelf and pruned models, prompted), but learned executors, the Foresee job, and any trained policy do. Near-term action: survey RL fundamentals and consult RL colleagues.

**2026-06-13 — executor framing (to confirm with Dr. Diao).** The human is the strategic commander; the LLM is the *executor* of that intent, not an autonomous strategist. Earlier framing (inherited from TextStarCraft II) scored an "LLM commander" by win rate, which conflicts with the human-as-commander vision. Resolution: in Phase 1 the commander is a scripted command stream, and the benchmark measures how well and how cheaply the LLM carries orders out — command-following in the arena, and win rate while executing a fixed strategy in StarCraft II. Renamed the "Decide" job to **Execute**, and Foresee is a what-if advisor the commander queries. This changes what the benchmark measures, so it is the next thing to put to Dr. Diao (his efficiency methods are scored by whichever metric). Project also renamed to **World Commander**.

**2026-06-14 — scope narrowed to execution.** Dropped the three-jobs axis (Execute / Foresee / Embody) as a redundant second framing of the phases: the vision is already carried by the long-term goal and the three phases. The proposal now runs on one spine, execution, across the phases. Foresee (the what-if advisor) is removed; embodiment (crowd-scale motion) is kept as one later direction and one project, not a co-equal job. The standalone "Competitive-efficiency study" project is dropped, aligning the inventory with the deck.

**2026-06-14 — input from Hongsong Tang (potential co-author, RL).** Pointed to [CivRealm (ICLR 2024)](https://arxiv.org/abs/2401.10568), an LLM-plus-RL decision-making environment on the turn-based strategy game Freeciv, as adjacent prior art (added to the literature review). Framed the real-time-versus-turn-based distinction as essentially latency: a turn-based game becomes real-time once each step is fast enough. Refinement carried forward: real-time also means the clock does not pause for the decision (the opponent keeps acting and a late decision is forfeited), so per-decision latency under an unpausable, concurrent clock is the binding constraint.

**2026-06-19 — micro-operation versus big-picture command (WeChat, with Hongsong Tang and Dr. Diao).** A near-term framing axis surfaced.

- **Two regimes.** *Big-picture* (strategic) command: the LLM interprets high-level language and issues actions through the game API; Dr. Diao frames this as an **agent** problem ("do it more agent-leaning"). *Micro-operation* (per-unit tactical) control: Dr. Diao frames it as embodiment, the [vision-language-action (VLA)](https://en.wikipedia.org/wiki/Vision%E2%80%93language%E2%80%93action_model) approach of the π0 line. Near-term action for Yubo: read the VLA literature.
- **Interface.** For big-picture command the LLM acts through the game's API, not by simulating mouse input; mouse emulation is unnecessary at the strategic level. This sharpens the slow-brain / fast-executor split already in Preliminaries: big-picture is the slow LLM brain (agent); micro-operation is the fast VLA executor below it.
- **RL's role depends on the choice (Hongsong).** For autonomous play, RL trains top-level strategy; for a big-picture *interactive* RTS, RL instead trains the bottom-level execution that turns one language command into a sequence of in-game micro-actions.
- **Command arena.** Hongsong: sound as an early latency-validation task. Adopted: it was single-sided control, so the arena now includes uncontrolled agents that move on their own clock, giving a late command a real cost (the real-time, unpausable-clock pressure that defines an RTS).
- **New reference.** [SMAC-R1 (Deng, Ma et al., 2024)](https://arxiv.org/abs/2410.16024): an LLM generates interpretable decision-tree scripts for the StarCraft Multi-Agent Challenge, refined by environment feedback and distilled into a smaller model. The offline-script-generation alternative to real-time language command (compare PORTAL); added to the literature review.
- **Open decision, near-term plan.** Yubo: long-term, build both regimes; short-term, decide which first (unresolved, added to open questions). Plan: finish the arena, get a preliminary result, then pitch the full program to 程立 (Cheng Li).

**2026-07-01 — executor axis = level of detail (not "units versus crowd").** A logic flaw in the hub's paradigm figure: the two executors were labelled "game units / discrete commands" and "crowd / full-body motion", which conflates two axes (a crowd is also made of game units, and the human's command is discrete in both regimes). The clean single discriminator is the **level of detail of the executor's output**: *coarse* (discrete, high-level actions issued through the game API, which the engine actuates: StarCraft II) versus *fine* (continuous full-body motion the model generates itself, frame by frame: embodiment). Both regimes are multi-agent; **scale (few → crowd) is a separate axis**, shared by both, not the discriminator. This sharpens the 2026-06-19 big-picture (agent, via API) versus micro-operation (VLA, motion) split; "level of detail" was chosen over "abstraction level" for concreteness. The hub paradigm figures were relabelled to match.

## Open questions for discussion

1. Venue and timing for the first project (ICLR 2027 versus a slower, stronger NeurIPS 2027 submission).
2. Model scale and compute: which open-weight families, and on whose GPUs the frontier sweep runs.
3. Whether the state-tokenization module belongs in the first project or stands alone as a second project.
4. Whether DreamSoul has product interest in the commander interface beyond the projects.
5. Which regime to build first: big-picture (agent) command, or micro-operation (VLA) execution. Long-term, both are in scope (Discussion log, 2026-06-19).
