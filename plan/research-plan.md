# Research Plan — Real-Time Crowd-Motion Command

A concrete experimental protocol for the dual-aligned World Commander direction
(the one that brings in Li Cheng). This is the *machinery*, not the story.
Grounded in `survey/command-crowds.csv` (73 verified references).

Drafted 2026-06-23.

## 1. Research question

Can a person command a small crowd of virtual characters **in real time**, in
**free-form natural language** (concrete orders *and* abstract intent), and have
the system generate their **coordinated full-body motion** on a fixed
**latency/memory budget**?

**Novelty (the open quadrant).** Each ingredient has precedent but the
combination is unbuilt: *real-time + central free-form/abstract command +
crowd-scale + closed-loop coordination + steerable motion + compute budget.*
Closest prior art and why it is not this: Text-Crowd (SIGGRAPH 2024) is *offline*
scene authoring; CAMDM (SIGGRAPH 2024) is real-time control of *one* character;
CrowdMoGen (IJCV 2025) is *offline* crowd generation.

## 2. System (three components)

```
command (free-form text) + world/agent state
  -> [A] Command interpreter (LLM)        : -> per-agent/group goals (target, action, style)
  -> [B] Coordination (rule-based -> RL)  : assigns/refines goals, resolves conflicts, keeps formation
  -> [C] Motion generator (pretrained,    : goal + style -> full-body motion per agent, in real time
         controllable, real-time)
  -> rendered crowd motion   [measured: grounding, latency, VRAM, motion quality]
```

The streaming-command harness from the `world-commander-bench` repo (grounding /
latency / deadline-miss metrics) transfers directly as the measurement layer.

## 3. Data plan (the crux — a synthetic pipeline, no manual annotation)

There is no (free-form command -> coordinated crowd motion) dataset, so building
one is part of the research. Three programmatic layers plus a small human test set:

- **L1 - Behaviour (ground truth).** A crowd simulator (RVO/ORCA + scripted
  formations: go-to, form-line, disperse, regroup, flank) produces coordinated
  agent **trajectories** for each *canonical* command. Free and exact.
  Optional upgrade: a learned crowd model (GREIL-Crowds / CEDRL).
- **L2 - Language (the free-form / abstract part).** An LLM paraphrases each
  canonical command into many free-form + abstract variants
  ("fall back" / "we are overextended, pull to the trees" / "regroup behind
  cover"). This is Text-Crowd's LLM-canonicalization run *in reverse*, and it is
  where the text-freedom (拉高文本自由度) actually comes from.
- **L3 - Motion (full body).** Render the L1 trajectories into full-body motion
  with a *pretrained* controllable model (TLControl / CAMDM take trajectory + style
  -> motion).

Output: **(free-form command, world state, coordinated full-body motion)** triples,
generated rather than annotated.

- **Human eval set (test only).** Collect a small set of *real* human commands for
  fixed scenes, render outputs, and human-rate intent match. This is the honest
  test set and the only sound way to score abstract intent.
- **Base assets.** Motion: HumanML3D, AMASS, BABEL, 100STYLE. Crowd trajectories:
  ETH/UCY, Stanford Drone, for the simulator and realism checks.

## 4. Model and training (reuse first, staged)

- **[C] Motion generator** — start from pretrained CAMDM / TLControl / MotionLCM;
  fine-tune or condition on goal + style. Do **not** train from scratch.
- **[A] Interpreter** — frozen LLM + prompt for v0 (use amax's served model);
  fine-tune on synthetic (command -> goal) pairs later.
- **[B] Coordination** — v0 is **rule-based / optimization** (target assignment +
  RVO navigation) so there is a working end-to-end baseline; v1 swaps in
  **RL / MARL** (Hongsong), reward = command-satisfaction + realism + budget,
  trained in the simulator. RL comes *after* the non-RL baseline runs.
- **Objectives** — behaviour cloning on synthetic data for A and B; the usual
  generative loss (reused) for C; RL fine-tune for B.

## 5. Evaluation (what makes it a paper, not a demo)

- **Command-grounding accuracy** — concrete commands measurable (did the agents
  reach/form the target); abstract commands human-rated.
- **Motion quality** — FID, foot-skating ratio, vs the motion-generation baselines.
- **Real-time / budget frontier** — FPS, end-to-end latency, peak VRAM: the
  quality-vs-budget curve (the World Commander spine).
- **Coordination** — collision rate, formation error, command-completion time.
- **Baselines** — Text-Crowd (offline); independent per-agent generation (no
  coordination); rule-based-only; no-interpreter (literal command).
- **Benchmark** — a "motion command arena" (a small standard scene + command suite)
  plus a human study for abstract intent.

## 6. Compute

- **Primary experiments: amax41** (Yubo's first choice). The motion models are
  small (MoMask ~44M params; MotionLCM / CAMDM modest), so amax's 3x RTX 2080 Ti
  comfortably handle training + RL fine-tuning; the served LLM (Qwen) does the
  interpretation. No frontier-scale model is needed for this direction.
- **Consumer-GPU real-time claim: yubopc** (RTX 4060, modern Ada) — the
  "runs on one consumer GPU" measurement, as Light-T2M / MotionBricks frame it.
- **Scale, if needed: Alliance** (larger crowds, bigger motion models).

## 7. Staging / milestones

- **v0 (de-risk, ~1-2 weeks).** 3-5 agents, *two* canonical commands
  ("form a line", "go to X"), a few hundred synthetic triples, condition *one*
  pretrained controllable model, measure grounding + FPS. Tests the two riskiest
  assumptions: (a) the synthetic pipeline yields usable data; (b) a controllable
  model follows a command in real time.
- **v1 (coordination).** Add the coordination layer (rule-based -> RL), more
  agents, formation + conflict resolution; produce the budget frontier.
- **v2 (abstract intent).** Add the free-form / abstract command axis + the human
  eval; reward-from-language for ungroundable intent.
- **v3 (scale + write-up).** Crowd-scale, full benchmark, paper.

## 8. Risks and de-risking (where the research actually is)

| Risk | Why it is hard | De-risk by |
|---|---|---|
| Synthetic -> real gap | LLM-generated commands are not real human phrasing | Test on the human eval set from v0; measure the drop |
| Grounding abstract intent | "look panicked as a group" has no ground truth | Reward-from-language (Eureka / Text2Reward) or preference data; human-rate. This is the novelty |
| Real-time x coordination x quality x budget | coordinating a live crowd under a VRAM/latency cap is unsolved | the budget-frontier curve *is* the contribution; measure it explicitly |
| Coordination realism | independent per-agent motion looks uncoordinated | the coordination layer (B) + collision/formation metrics |

## 9. Roles

- **Yubo** — command interpreter + benchmark/harness + the budget framing.
- **Diao** — efficiency (KV-cache eviction, pruning, tokenization) applied to the
  interpreter and the motion tokenizer.
- **Hongsong** — the coordination RL / MARL layer.
- **Li Cheng** — the controllable real-time motion generator (the MoMask line) +
  supervision.

## 10. Relationship to the rest of the repo

- **Basis:** `survey/command-crowds.csv` (73 verified references).
- **Program:** `PROPOSAL.md` (the broader World Commander). The StarCraft II line
  shares the same core technology — efficient, real-time, tokenized command of a
  crowd under a budget — and is a parallel instantiation in game units rather than
  motion; methods carry over.
- This plan is the concrete protocol for the dual-aligned (Li Cheng) direction.
