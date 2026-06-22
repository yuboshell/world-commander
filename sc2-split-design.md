# SC2 commander/executor split (E2) — design note

**Status:** spec, for **yubopc** to implement and run on **Windows**. SC2 *win-rate*
needs SC2 ≥ 5.0.15 (Windows only — the Linux build is capped at 4.10); amax can scope this
and measure *latency* on 4.10, but not win-rate. This note is the amax-side scoping; the
experiment lives in the SC2 thread.

Builds on the decision *"Two-LLM pipeline … the general structure across E1/E2/E3"*
(DECISIONS, 2026-06-22) and the E3 design note. E2 is the environment where the split
actually matters, because **commanding SC2 is hard** (real strategy), unlike the trivial
reference-commands of E1/E3.

## 1. Why split E2
Today the SC2 LLM does **both** jobs at once: it reasons about strategy *and* emits unit
actions, every decision cycle. That couples a slow, expensive reasoning step to the
real-time clock — and our measurements show why that fails: decision latency is seconds
(1.7B 2.7 s → 14B 7.5 s at ~3000-token context) and misses the drop-late deadline, so
win-rate collapses. The program's own findings point to the fix: **LLM for intent, a fast
layer for execution** (the hierarchy result; the classify-intent-then-execute capstone;
HLA's slow-mind / fast-mind, see LITERATURE).

So split the one LLM into two:

## 2. The two roles
- **Slow commander (strategic mind).** Periodically (not every tick) reads the game state
  and issues a **high-level natural-language intent**: e.g. *"focus fire the enemy stalkers"*,
  *"pull the zealots back"*, *"group up and push the left ramp"*. This is the **macro/planning**
  step — the hard part — so a **larger model and a slower cadence** are fine. It is **off the
  per-tick real-time deadline** (amortized over many ticks).
- **Fast executor (tactical mind).** Every decision cycle, takes the **current intent + current
  state** and grounds it to concrete SC2 unit actions, **fast**. This is **reference grounding**
  — the part our arena shows is *solved and cheap* on a small model — so a **small model on the
  real-time deadline**. This is the role on the **drop-late clock**.

**Cadence:** commander every *C* seconds (e.g. 3–10 s), executor every decision cycle. The
executor always acts on the **most recent** intent (and must degrade gracefully when the intent
is stale — keep executing the last order until a new one arrives).

## 3. What it tests
- **The hierarchy finding on the hard environment.** E1 showed routing macro→large / micro→small
  is a Pareto win on a toy grid; E2 is the real test: does a slow-commander/fast-executor split
  beat a single LLM under a real-time clock?
- **The executor stays under the deadline** while the commander supplies the strategy the
  executor lacks — decoupling "good play" from "fast enough".

## 4. Metrics
1. **Executor decision latency** vs the real-time / drop-late deadline (must beat it — the whole
   point of making it the small, fast role).
2. **Win-rate**, three arms on the same matchup/seeds:
   - **split** (slow commander + fast executor),
   - **single-LLM** (current: one LLM does both),
   - **auto-attack baseline** (no effective LLM) — the confound control from the SC2 thread.
3. **Commander cadence sweep** — win-rate vs *C* (how often to re-strategize): too slow = stale
   orders, too fast = wasted compute / back on the latency wall.
4. **Drop-late frontier** for the executor (win-rate vs deadline), as already built for E2.

## 5. Implementation notes (LLM-PySC2, for yubopc)
- Two model roles. Either two endpoints (e.g. a larger commander + a 4B executor) or one served
  model called with two different prompts/cadences.
- **Commander prompt:** state → one short strategic order (the intent vocabulary above). Called
  every *C* s; cache its output as the "current intent".
- **Executor prompt:** current intent + current state → concrete unit actions, terse output
  (reuse the arena's terse-schema / no-think latency levers). Called every cycle, on the deadline.
- Log commander and executor latency **separately** (only the executor is on the deadline path).
- Reuse the existing drop-late harness and the no-commander baseline.

## 6. Controls & caveats
- **Auto-attack confound:** SC2 units auto-attack, so "focus the nearest/weakest" is partly free.
  Keep the **no-effective-LLM control**; pick a **matchup where micro/macro matters beyond
  auto-attack** (the SC2 thread found 3s5z's LLM edge was ~+10 pp and not significant — the split
  needs a setting where strategy actually pays, or it will look like noise again).
- **Capability-bound win-rate:** an unwinnable force composition (2s3z 0/8) tells you nothing about
  the split — choose a winnable, strategy-sensitive matchup.
- **Soft vs hard deadline:** report the split under the *hard* drop-late clock (late executor
  actions dropped), which is where the real-time effect lives.
- **Stale-intent handling** is part of the design, not an afterthought — measure how often the
  executor runs on an out-of-date order at each cadence.

## 7. Where it runs
- **Win-rate + drop-late:** Windows / yubopc, SC2 5.0.15. **Latency-only** characterization of the
  two prompts can be done on amax (SC2 4.10) if useful, but not win-rate.

## 8. Open questions
- Commander model size and cadence *C* (the two main knobs).
- Intent vocabulary — free-form NL vs a small fixed set of orders (a fixed set makes the executor's
  grounding cleaner and the commander's job a classification, echoing the E1 capstone).
- Does the executor need the *commander's* model occasionally for hard tactical moments (escalation),
  or is a fixed small executor enough?
