# Open-Quadrant Options — a method-agnostic map

Companion to `research-plan.md`. That plan commits to one concrete protocol
(real-time crowd-motion command). This note keeps the **method choices open**: it
lists the candidate ways to hit the open quadrant per pillar, so no single tool —
**tokenization included** — is assumed. Use it as the menu when we plan.

Drafted 2026-06-27, after a methodological-independence correction (see
`DECISIONS.md`, 2026-06-27).

**Decision (2026-06-27):** the research act is **A** — keep a slow natural-language
reasoner in command of a fast, multi-agent world in real time (the *live-clock
control problem*). Focus on the **act**; the artifact (benchmark / dataset /
method) is a downstream side-product. See `DECISIONS.md`.

## The frame

Open quadrant (from `literature.html`): **free-form command × real-time ×
multi-agent × budget-aware**, measured closed-loop. Pipeline pillars:
**Command → Interpreter → Coordination → Executor**, with **Budget** cross-cutting
(the wedge sits on the interpreter). The contribution is the budget-aware
closed-loop corner; methods compete on **fit-to-goal × lab-alignment × novelty**,
not pedigree.

## Selection principle

- Choose direction by **community white space** (important × meaningful ×
  under-explored), **not** by lab moat. The moat (mocap / reconstruction) sits in
  the *most crowded* pillar (Executor, 41/89), so it is not a tiebreaker — the
  white space is the command/control loop under budget.
- Do not privilege a method because a collaborator used it. When reaching for
  tokenization/KV-cache, name a non-Diao alternative and why it loses.
- **Keep a portfolio.** Do not kill an idea for being off the current thesis (A);
  park off-A ideas as parallel tracks (e.g., BPE-for-motion) — more good ideas =
  more researcher benefit.

## Per-pillar menu

### Budget (the wedge) — where we over-forced tokenization
Goal: hit a latency / VRAM / tokens target at equal quality, measured in the live loop.

| Approach | Idea | Fit | Lab-align | Novelty |
|---|---|---|---|---|
| **Get the LLM off the inner loop** | distill command→behaviour into a small reactive policy; the LLM compiles once per command, not per frame | high | med | med |
| **Hierarchical / async** | slow planner emits a behaviour-tree / GOAP / parametric goal; a cheap classical layer runs at frame rate (HLA slow/fast) | high | med | med |
| **Architecture, not eviction** | SSM / Mamba long context; retrieval / symbolic blackboard for "what I commanded 2 min ago" | med | low | med |
| **Tokenization (one option, de-privileged)** | fewer tokens per decision for the interpreter | conditional | low (Diao) | med |

**Tokenization caveats (if chosen).** It is **sequence-native** — fine for motion
and the command/action *stream*, but a stretch for a static game-state graph (a
set/graph, not a sequence; BPE only applies through a serialization crutch, where
continuous fields fragment exact-match merges). The lever is **structure-aware
serialization**, not BPE; require **reversibility / permutation-invariance**; the
contribution is the **closed-loop budget measurement**, not the compression ratio.
Detail + roadmap: Graph-Tokenization repo `applications/motion-bpe/README.md`.

### Command / Interpreter — maybe the real hard part
Grounding ambiguous free-form orders ("flank", "hold the line", "the one I moved
west") into spatial-temporal objectives under partial observation. Draws on
referring expressions / situated dialogue / reward-from-language — not compression.
Plausibly the true novelty, and orthogonal to the budget race. (This is "B"; under
the 2026-06-27 decision it is a sub-capability *inside* A, not the spine.)

### Coordination (multi-agent) — mostly token-free
RVO/ORCA, flow / potential fields, optimal transport (Sinkhorn) assignment, MARL.
The LLM sets the objective; cheap classical methods solve the crowd. Already the
plan of record — see `research-plan.md` §3–4.

### Executor — motion — token-free options
Pretrained controllable models (CAMDM / MoMask / MotionLCM / TLControl);
**motion matching** (game-industry real-time clip database); **physics controllers**
(DeepMimic / AMP / ASE / PHC); **diffusion / flow-matching** made real-time via
consistency distillation. None require tokenization. See `research-plan.md` §4.
Under the 2026-06-27 decision, for A the motion generator is a **reused component**,
not our research.

## Parked ideas (off-A, kept — not rejected)

- **BPE for motion generation.** Motion is sequence-native, so BPE is a *natural* fit
  (unlike static game state, where it is a stretch). But standalone novelty looks
  low-to-modest: discrete-token motion via learned **VQ codebooks** is the mainstream
  (T2M-GPT, MotionGPT, MoMask), and "BPE a non-text modality" is already published
  (FreeMesh for mesh, MDBPE for visual). For A it would be a reusable component, not
  the contribution. Kept as a portfolio probe (Graph-Tokenization repo
  `applications/motion-bpe/`); run a focused novelty search before investing.

## What's genuinely open / next

- *(resolved 2026-06-27)* Focus = the **act (A)**, not the artifact type — the
  benchmark / dataset / method is a side-product that follows from doing A.
- *(resolved 2026-06-27)* Direction chosen by **community white space**, not moat →
  the command/control loop, not the crowded executor pillar.
- **Open — the budget bet:** within A, which approach hits the latency / VRAM /
  tokens target — and does it beat "get the LLM off the inner loop" on the frontier?
- **Open — reconcile** the outdated *phases* framing in `PROPOSAL.md` / `index.md`
  with the 4-axis paradigm in `literature.html`.
- **Next session:** spec **A** — the environment, the slow-intent / fast-execution
  decomposition, and the re-planning trigger (handling the reasoner's stale view).
