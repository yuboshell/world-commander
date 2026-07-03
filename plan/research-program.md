# World Commander — Research Program Plan

A concrete, executable decomposition of the program into **projects** and **tasks**,
grounded in the E1–E4 experiments and the 89-paper survey (`survey/command-crowds.csv`).
This supersedes the proposal's vision-level framing: every project below names its
**challenge**, **prior-art density**, **metrics**, **datasets**, **baselines**, and the
**data it must synthesize**.

Drafted 2026-06-27. Terminology: *program* > *project* (paper-sized) > *task* (a step).

---

## 1. The paradigm, made concrete

The **human** is the **strategic commander** — they view the world and decide intent
(strategy, planning). The **LLM** is the **executor**: it *grounds* the human's free-form
natural-language command into coordinated agent actions, **fast**, under a
**time-to-consequence deadline** and a **memory budget**. The commander is off the
system's critical path; **only the executor's grounding latency is timed** (established
across E1–E3).

This split is load-bearing because it plays to the LLM's strength and avoids its weakness:
- **Strength — reference resolution** (named / spatial / temporal: "the red one", "the top
  half", "the ones I sent west"). ~1.00 on a 4B model, fast. The executor's job.
- **Weakness — open-ended planning** (macro geometry). Capability-bound, never solved
  cheaply (4B/8B ~0.35, 14B 0.59). The *human's* job — or routed to code.

So the executor is not "an LLM that plays the game". It is: **classify the command's intent
→ (resolve a reference | execute computable geometry in code | escalate genuinely open
planning to a larger model)** — within the deadline. Macro *intent* classification is ~1.00
on 4B even when macro *geometry* is 0.38, so intent-classify (LLM) + geometry (code) gives
macro grounding ~1.00 on a small model. One natural-language channel; underneath,
classify → (reference | code-execute | escalate).

The executor's **output** is coordinated agent actions in one of two domains: **game units**
(RTS commands) or **a crowd** (full-body motion). Everything upstream — interpretation, the
intent router, the efficiency machinery, the budget — is domain-agnostic; only the
executor's action space swaps.

---

## 2. Program structure

Five paper-sized projects, along the pipeline, under the budget spine:

```
human command ─▶ [interpreter / intent router] ─▶ [coordination] ─▶ [executor] ─▶ action
   P1 benchmark — measures the whole loop's cost under the real-time clock
   P2 efficiency — optimizes the executor under the latency + memory budget
   P3 tokenization — compresses the state the executor reads
   P4 coordination — turns one command into many-agent action
   P5 motion executor — renders a commanded crowd in real time
```

- **Sequence.** P1 is the instrument (largely built: E1+E2). P2 builds on P1. P3 feeds
  P1/P2/P5 (smaller state → less latency + memory). P4 feeds P5 (coordination → the crowd).
  P5 is the dual-aligned capstone (E4 has a v0).
- **Team.** P1/P2: Yubo + Diao. P3: Diao. P4: Hongsong. P5: Li Cheng.
- **Novelty gradient** (least → most open): **P1** (crowded, but anchored by our drop-late
  result) → **P3 / P4** (emerging) → **P2** (methods crowded, but the *in-game setting* is
  empty) → **P5** (the open quadrant — 0/89 papers hit all four axes; the wedge).

---

## 3. The projects

### P1 — Real-time command benchmark *(the instrument)*
- **Goal.** A benchmark for the *cost of real-time command*: grounding accuracy +
  command-to-action latency + the **drop-late deadline frontier**, across a complexity
  ladder (command arena → StarCraft II).
- **Status.** Substantially built. E1 (Grid Arena): the three metrics, output-schema +
  model-size frontiers, the micro/macro taxonomy, the classify→(reference|code|escalate)
  router. E2 (SC2): the validated **drop-late real-time clock** (declining frontier
  ~87%→62% as the deadline crosses the ~25 s latency); win-rate is auto-attack-confounded
  (4B edge ~+10 pp, **not significant**) — so the frontier, not win-rate, is the result.
- **Tasks.** (1) the arena + 3 metrics + the command-stream load model (rate vs deadline);
  (2) the command taxonomy (micro/reference, region, memory, macro/planning); (3) the SC2
  real-time wrapper with hard drop-late (done) + a clean high-n frontier (calibration
  pending); (4) the intent router (classify → reference | code | escalate).
- **Challenge.** Defining the deadline as *time-to-consequence*, not an arbitrary tick;
  isolating grounding from planning (the arena does this; SC2's auto-attack confounds
  win-rate); a clean high-n SC2 frontier (camera calibration is run-fragile).
- **Prior art — moderate/crowded.** SC2-LLM cluster (TextStarCraft II, LLM-PySC2,
  SwarmBrain, Adaptive Command — Weiyu Ma's group); real-time-eval cluster (VideoGameBench,
  AgileThinker). The **budget / drop-late** framing + grounding-vs-planning isolation is
  underdone — our angle.
- **Metrics.** grounding accuracy; command-to-action latency (p50/p95); deadline-miss rate;
  sustainable command rate; win rate (SC2 — only as LLM-vs-auto-attack, balanced matchup, adequate n).
- **Datasets.** the command arena (synthetic, ours); SC2 via python-sc2 / LLM-PySC2;
  SC2EGSet (replays); SMAC.
- **Baselines.** output schemas (json/pairs/grouped); model sizes (0.6B–32B); the router
  (micro→small, macro→code/large); built-in SC2 AI; auto-attack (no-LLM control).

### P2 — Efficient executor under the live clock *(the methods)*
- **Goal.** Evaluate efficient-inference methods (KV-cache eviction, quantization,
  distillation, speculative decoding) + the established levers **inside a running game**,
  where discarding the wrong information changes the *outcome* — and chart the
  quality-vs-budget frontier. This is the proposal's central thesis.
- **Status.** Levers established (E1): **output × decode dominates latency; input is
  cacheable** (prefix-cache the static prefix); terse schema + right-size (4B) +
  code-routing cut latency. KV-cache methods not yet ported in-game.
- **Tasks.** (1) port KV-cache methods (H2O, SnapKV, StreamingLLM, OBCache) into the
  arena/SC2 executor loop; (2) the quality-vs-budget Pareto (grounding / win-rate at fixed
  latency + VRAM budgets); (3) the **VRAM ceiling** (the memory axis, "still to add");
  (4) characterize *which* evictions hurt in-game.
- **Challenge.** The methods are validated only on **static text** benchmarks; in a game in
  progress, discarding the wrong info can lose the match; the quality metric is in-game
  (grounding / win-rate), not perplexity.
- **Prior art — methods very crowded, setting empty.** H2O, SnapKV, StreamingLLM, OBCache,
  + the pitfalls line (DefensiveKV, SideQuest, "Pitfalls of KV-Cache Compression"). **None
  evaluated inside a running game** — the in-game setting is the contribution.
  WorldMemArena (2026) makes the parallel argument for agent memory.
- **Metrics.** quality (grounding / win-rate) at fixed latency + memory budgets; the
  quality–budget Pareto; the per-method "what mattered that was evicted" analysis.
- **Datasets.** the arena + SC2 (from P1); an SC2-scale static prefix (for the prefix-cache lever).
- **Baselines.** full-cache; H2O; SnapKV; StreamingLLM; OBCache; AWQ (quantization); a
  distilled small model; the terse-schema + prefix-cache + right-size levers.

### P3 — Compact state / motion tokenization *(the representation)*
- **Goal.** Compress the structured state the executor reads (game state; motion) into
  fewer tokens via **graph + BPE tokenization** → less latency (output × decode + cacheable
  input) and memory.
- **Status.** The Motion BPE viability probe (does motion have reusable BPE motifs?) exists;
  graph tokenization is Diao's line (Guo, Diao, ICLR 2026).
- **Tasks.** (1) tokenize SC2 game state (graph/BPE) → tokens-per-decision + downstream
  grounding; (2) a motion BPE tokenizer (viability → a real tokenizer) + generation; (3) vs
  VQ-VAE motion tokens (MoMask / T2M-GPT line).
- **Challenge.** Lossless-ish compression of relational state; whether motion has reusable
  BPE motifs (the real-vs-shuffled signal); tying token count to executor latency.
- **Prior art — moderate.** Motion-VQ crowded (MoMask, T2M-GPT, MotionGPT, MotionStreamer);
  graph tokenization newer (Diao).
- **Metrics.** tokens-per-decision / per-frame; reconstruction + downstream quality
  (grounding / FID); latency + memory savings.
- **Datasets.** SC2 state (SC2EGSet replays); motion (HumanML3D, AMASS, the user's MoCap).
- **Baselines.** raw-text state encoding; VQ-VAE; MoMask tokens; T2M-GPT tokens.

### P4 — Language-conditioned crowd coordination *(the brain)*
- **Goal.** Turn one (possibly abstract) command into coordinated multi-agent action — the
  executor grounding a command into *per-agent* goals across a crowd, **learned (RL/MARL)**
  where rule-based won't scale.
- **Status.** Scoped (the coordination layer in `research-plan.md`); not built (E4's v0 uses
  a rule-based sim).
- **Tasks.** (1) a coordination policy: command → per-agent goals (rule-based → RL/MARL);
  (2) abstract-intent → coordination (拉高文本自由度) via classify-then-coordinate or
  reward-from-language; (3) scale to crowd sizes (the O(N²) sim is a known bottleneck);
  (4) human-interpretable coordination.
- **Challenge.** Scalable coordination from **abstract** intent (no ground truth for "look
  panicked as a group"); reward-from-language vs supervision; the synthetic→real command gap.
- **Prior art — emerging/growing.** LangGround (NeurIPS 2024), GLAM, LLM-MARL, instructRL,
  HMASD, FMH. The novelty is abstract-intent + crowd-scale + real-time + budget.
- **Metrics.** coordination quality (collision rate, formation error, completion time);
  command-following (concrete measurable, abstract human-rated); scalability (vs N agents);
  ad-hoc / zero-shot teammates.
- **Dataset — SYNTHESIZE.** *(free-form command → coordinated crowd behaviour)* — does not
  exist. L1 sim (RVO/scripted formations) → L2 LLM paraphrase → coordination labels. Plus a
  small human eval set.
- **Baselines.** MAPPO; QMIX; LLM-MARL; independent per-agent (no coordination); rule-based
  assignment.

### P5 — Real-time crowd-motion command *(the motion executor — the capstone)*
- **Goal.** Ground a free-form (incl. abstract) command into a small crowd's coordinated
  **full-body motion, in real time, on a latency/memory budget**. The dual-aligned project
  (brings in Li Cheng).
- **Status.** v0 done (E4): the synthetic pipeline (L1 sim → L2 served-Qwen → L3 OmniControl)
  + the model-in-the-loop grounding test — **concrete 0.88→0.96, abstract 0.18→0.74** (with
  the coordinate guard). Open: real-time (OmniControl is ~16× slower than real-time), the
  coordination layer (P4), the O(N²) sim.
- **Tasks.** (1) the motion-command arena + metrics (v0 done); (2) **real-time** steerable
  motion (distill / MotionLCM / DART / CAMDM — replace OmniControl); (3) scale to crowds
  (CrowdMoGen-style planning + P4's coordination); (4) abstract command → crowd motion + the
  human eval; (5) the **budget frontier** (FPS / latency / VRAM vs quality + crowd size).
- **Challenge.** real-time × crowd × abstract × budget **all at once** (the open quadrant);
  the synthetic→real gap; the coordination × quality × budget trade-off; **abstract-intent
  grounding** (the genuinely novel + hard part).
- **Prior art — the open quadrant, sparsest/most novel.** Each closest paper misses ≥1 axis:
  Text-Crowd (offline), CAMDM (real-time, single-char), CrowdMoGen (offline crowd), DART /
  MotionLCM / TLControl (real-time, single-char). **0/89 hit all four.**
- **Metrics.** command-grounding (concrete measurable, abstract human-rated); motion quality
  (FID, foot-skating); the budget frontier (FPS, end-to-end latency, peak VRAM); coordination
  (collision, formation error).
- **Dataset — SYNTHESIZE.** *(free-form command → coordinated crowd motion)* — does not
  exist. The L1→L2→L3 pipeline (v0 built). Plus a small human-issued eval set.
- **Baselines.** Text-Crowd (offline); independent per-agent generation; CAMDM / TLControl
  (single-char real-time); rule-based; no-interpreter (literal command).

---

## 4. Cross-cutting

### 4.1 The two datasets that must be synthesized
Neither exists; both come from one 3-layer pipeline (built for E4, reused for P4):
- **L1 — behaviour (ground truth):** a crowd sim (RVO/ORCA + scripted formations: go-to,
  form-line, disperse, regroup, flank) → coordinated trajectories per *canonical* command.
- **L2 — language (free-form/abstract):** an LLM paraphrases each canonical command into many
  free-form + abstract variants — the source of 拉高文本自由度.
- **L3 — motion (P5 only):** render trajectories with a pretrained controllable model
  (TLControl / CAMDM / MotionLCM).

→ **P4** needs `(command → coordination)` [L1+L2]; **P5** needs `(command → crowd motion)`
[L1+L2+L3]. Each also needs a small **human-issued eval set** — the only honest way to score
abstract intent (and to measure the synthetic→real gap).

### 4.2 Abstract-intent grounding (拉高文本自由度) — the shared hard problem
Concrete commands are measurable; abstract ones ("be aggressive", "look panicked") have no
ground truth. This is the program's genuinely novel + hard problem (P4 + P5). Likely tools:
classify-then-act (E1's intent router, ~1.00 on 4B), reward-from-language (Eureka /
Text2Reward), or preference data — not supervision. E4's abstract 0.18→0.74 (with a guard)
is first evidence it's tractable.

### 4.3 The budget axis — the spine
Every project measures under a **time-to-consequence deadline** + a **memory (VRAM) budget**.
The deadline is the world's consequence horizon (voice-paced command has seconds), not a
game clock. The durable cross-project result so far is the **drop-late real-time frontier**
(E1 + E2): under a hard deadline, quality falls toward the no-LLM floor as the deadline
tightens — that curve is the program's real-time-viability instrument.

---

## 5. Status snapshot
- **P1** — substantially done (E1 arena + E2 SC2 drop-late). Remaining: clean high-n SC2 frontier.
- **P2** — levers established (E1); KV-cache-in-game + the VRAM ceiling are the open work.
- **P3** — viability probe done (Motion BPE); the real tokenizers are open.
- **P4** — scoped, not built — needs the synthetic `(command → coordination)` dataset + the RL policy.
- **P5** — v0 done (E4) — needs real-time motion + the coordination layer + the human eval.

Basis: `survey/command-crowds.csv` (89 refs), `plan/research-plan.md` (P5 detail),
`DECISIONS.md` (the E1–E4 findings), and the bench-hub reports (E1–E4).
