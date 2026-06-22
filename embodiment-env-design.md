# Embodiment / motion environment (E3) — Phase-1 design note

**Status:** draft proposal for a *third* World Commander environment. Sibling to
E1 (command arena, grid) and E2 (StarCraft II). Aligns with the lab's human-motion /
embodiment interest.

## 1. Why a third environment
World Commander = a human gives natural-language commands to agents in real time,
under latency/memory budgets; the LLM is the **executor** that parses + grounds the
command (see DECISIONS: "two LLM roles"). E1 and E2 measure grounding + decision
latency, but in both, *acting is instantaneous* (a move is applied as a discrete
event). E3 adds the axis they miss:

> **Physical execution time.** The agent has a body; carrying out a command takes
> *motion*, which takes *time and space*. So the real-time budget becomes
> `parse + ground (LLM) + execute the motion (body) < deadline`, not just decision latency.

E3 is also the natural testbed for the **LLM → motion-controller handoff** (the
embodiment instance of the hierarchy we found: LLM for intent, a fast controller for
execution), and the clean place to plug in a real **motion-generation** model — the
lab's area — as that fast layer, under a clock.

Two terms, plainly:
- **Embodiment** — the agent acts through a *body* in a (simulated) physical world;
  movement is constrained by kinematics and takes time.
- **Motion generation** — producing the actual *movement* (a reach trajectory/animation),
  not just a discrete action label.

## 2. The setup (refined from the button-press seed)
A virtual character sits at a desk with a small panel of **buttons** (start: 2;
extensible to N, varied positions). Timeline per round:
`all dark (T_off) → one random button lights for a window W → dark → …`
A command is issued; the **LLM executor** grounds it to a target button; a **motion
controller** generates the character's reach; **success = the lit button is pressed
while still lit** (i.e. the whole chain finished within W).

The seed task ("press whichever is lit") is deliberately the *reaction floor* — it
isolates timing. The benchmark value comes from (a) making the motion *cost real
time* and (b) enriching the command so the executor does genuine grounding (below).

## 3. Roles (per the locked "two LLM roles" decision)
- **Human** = commander: views the world, issues the natural-language command (intent).
  Phase 1 uses a **scripted stand-in** (as E1's `sample_command` does).
- **LLM executor** = parse the command + **ground it to a target** ("press button k"),
  fast. *Optimized.* It never plans the reach.
- **Motion controller** (fast layer) = turn "press k" into a reach **trajectory** and
  execute it. The **handoff** is this LLM→controller boundary.

## 4. What's genuinely new: motion makes the deadline physical
Pressing is a **timed reach**: motion duration scales with hand-to-button distance and
the character's speed. So:
`success ⇔ parse+ground latency + motion duration ≤ W` (the lit window).
Sweep **W** → a **success-vs-deadline frontier**, exactly mirroring the arena's
deadline frontier — but now the budget includes an *execution* term, not just decision.
This is E3's contribution.

## 5. Command taxonomy (executor's job — grounding, not planning)
Reuse E1's reference taxonomy, adapted (planning stays the human's job, so it is *not*
an executor metric):
- **direct** (reaction floor): "press the lit button."
- **spatial reference**: "press the button on your left", "the one nearer your right hand."
- **temporal / memory**: "press the one that lit *last* time", "the colour I named earlier"
  (history in the prompt context, as E1's memory commands do).
- **conditional**: "if the red light is on press left, else right."
Each command resolves to a target set + is scored by **acceptable-set grounding**
(reuse `arena/commands.py` semantics).

## 6. Metrics
- **Grounding accuracy** — did the executor resolve the command to the right target?
- **End-to-end success rate** — pressed the right button *while lit* (parse+ground +
  motion within W).
- **Latency breakdown** — LLM parse+ground latency vs motion duration; the
  **success-vs-W frontier** is the headline (per model size / schema).
- **Efficiency levers carry over** — terse output, prefix-cache, right-size/4B, the
  hierarchy/code-route — all shrink parse+ground latency → widen the viable-W frontier.

## 7. The LLM → motion handoff: fidelity ladder
Keep the program's "light harness" rule; escalate fidelity only as needed.
- **L0 (light, recommended first):** no renderer. Pressing is discrete, but charged a
  **reach-time model** (`t_move = dist / speed`); the controller is a stub that returns
  that duration. Pure-Python; reuses E1's harness, metrics, deadline-frontier, rate, and
  router. Already captures the new axis (motion time vs deadline) and the handoff.
- **L1 (medium):** a 2D kinematic arm (interpolated reach) + simple visualization.
- **L2 (heavy):** a 3D character driven by a **text-to-motion model** (the lab's area)
  generating the reach — realistic motion *and* realistic timing; the fast layer is a
  genuine motion generator / VLA-style controller.

**Recommendation:** build **L0 first** — it answers the core question (does parse+ground
+ motion fit the deadline, and how do the efficiency levers move the frontier) with no
heavy deps. Escalate to L1/L2 to study real motion generation and the fast controller.

## 8. What E3 tests that E1/E2 don't
- Physical **execution time** as a first-class budget term.
- The **LLM ↔ motion-controller handoff** under a real clock — the embodiment instance
  of the hierarchy finding (cf. SC2's drop-late clock, E1's deadline frontier).
- A clean home for a real **motion-generation** model as the fast executor (lab tie-in),
  measured under a deadline rather than offline.

## 9. Phase-1 scope (minimal first slice)
L0: N=2 buttons at fixed positions, window W, scripted stand-in commander, LLM executor
(reuse `RealClient`), a `reach_time` model, and a **success-vs-W sweep** across W,
command type, and model size — output a frontier + a parse+ground/motion latency
breakdown, mirroring the arena report. Reuse E1's `commands`, `metrics`, `rate`,
deadline-frontier, and `RouterClient`.

## 9a. First L0 result (2026-06-21) — the axis works
Built in the bench repo (`desk/`, `scripts/run_desk.py`; 5 TDD tests). First run, 4B on
GPU 2, 80 rounds, 2 buttons:
- **Executor grounding 0.91** — resolves the reference (direct/colour/spatial) to the lit button.
- **Parse+ground p50 ≈ 69 ms** — far below the arena's ~500 ms, because the prompt is tiny and
  the output is one word (consistent with "output length dominates latency").
- **Reach time — not LLM latency — gates the tight window:** at W=300 ms the cross-desk reaches
  (~340 ms) drop success to 0.53; by W≥500 ms success ≈ the grounding ceiling (0.91).

So physical execution time is the binding term at short windows, as designed — E3's new axis is
real and measurable. **Caveat:** hand carry-over + only 2 buttons means ~half the reaches are 0
(the lit button is already under the hand); to surface reach more cleanly, return the hand to a
rest position each round and/or use more, wider-spaced buttons. Next: that refinement, then add
the LLM↔motion handoff at higher fidelity (L1/L2 with a real reach/motion model).

## 10. Open questions
- Fidelity to commit to (L0 now; trigger for L1/L2).
- Which text-to-motion model for L2 (the lab tie-in).
- Multi-character / command *sequences* (richer grounding) — later.
- Working name: "reaction-desk" / "button-panel" embodiment env.
