# Open-Quadrant Options — a method-agnostic map

Companion to `research-plan.md`. That plan commits to one concrete protocol
(real-time crowd-motion command). This note keeps the **method choices open**: it
lists the candidate ways to hit the open quadrant per pillar, so no single tool —
**tokenization included** — is assumed. Use it as the menu when we plan.

Drafted 2026-06-27, after a methodological-independence correction (see
`DECISIONS.md`, 2026-06-27).

## The frame

Open quadrant (from `literature.html`): **free-form command × real-time ×
multi-agent × budget-aware**, measured closed-loop. Pipeline pillars:
**Command → Interpreter → Coordination → Executor**, with **Budget** cross-cutting
(the wedge sits on the interpreter). The contribution is the budget-aware
closed-loop corner; methods compete on **fit-to-goal × lab-alignment × novelty**,
not pedigree.

## Selection principle

- Do not privilege a method because a collaborator used it. When reaching for
  tokenization/KV-cache, name a non-Diao alternative and why it loses.
- The lab's moat is **reconstruction / mocap / human-animal pose** (Li Cheng).
  Prefer contributions that use *that* moat over a generic LLM-compression race.

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
and the command/action *stream*, but 勉强 for a static game-state graph (a set/graph,
not a sequence; BPE only applies through a serialization crutch, where continuous
fields fragment exact-match merges). The lever is **structure-aware serialization**,
not BPE; require **reversibility / permutation-invariance**; the contribution is the
**closed-loop budget measurement**, not the compression ratio. Detail + roadmap:
Graph-Tokenization repo `applications/motion-bpe/README.md`.

### Command / Interpreter — maybe the real hard part
Grounding ambiguous free-form orders ("flank", "hold the line", "the one I moved
west") into spatial-temporal objectives under partial observation. Draws on
referring expressions / situated dialogue / reward-from-language — not compression.
Plausibly the true novelty, and orthogonal to the budget race.

### Coordination (multi-agent) — mostly token-free
RVO/ORCA, flow / potential fields, optimal transport (Sinkhorn) assignment, MARL.
The LLM sets the objective; cheap classical methods solve the crowd. Already the
plan of record — see `research-plan.md` §3–4.

### Executor — motion — token-free options
Pretrained controllable models (CAMDM / MoMask / MotionLCM / TLControl);
**motion matching** (game-industry real-time clip database); **physics controllers**
(DeepMimic / AMP / ASE / PHC); **diffusion / flow-matching** made real-time via
consistency distillation. None require tokenization. See `research-plan.md` §4.

## What's genuinely open (the next decisions)

1. Is the contribution a **method**, a **benchmark** (the closed-loop budget eval),
   or a **dataset/pipeline** (the synthetic command→motion triples, `research-plan.md` §3)?
2. Which budget approach do we actually bet on — and does it beat "get the LLM off
   the inner loop" on the frontier?
3. Where does the lab moat (mocap / reconstruction) give an unfair advantage — and
   does that pick the executor/data direction over the interpreter-budget direction?
4. Reconcile the outdated **phases** framing in `PROPOSAL.md` / `index.md` with the
   current 4-axis paradigm in `literature.html`.
