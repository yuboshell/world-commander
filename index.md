# World Commander — Index

Natural-language command of agent crowds in real-time strategy games, under latency and memory budgets.

The hub for this repo: start here and follow the links. The structure borrows the
[LLM-wiki pattern](llm-wiki.md) — immutable sources, interlinked working documents,
and a schema file (`CLAUDE.md`) that says how to maintain them.

## Start here
- [Proposal](PROPOSAL.md) — the canonical research program: the spine (execution under budget), the three phases, the Phase-1 wedge, the prior-art map, and the discussion log.
- [Slide deck](world-commander.md) — the presentation view (5 slides plus a related-work appendix); renders to [PDF](world-commander.pdf) and [HTML](world-commander.html).

## Implementation
- [world-commander-bench](https://gitlab.com/worldcommander/world-commander-bench) — the Phase-1 code: the command arena now, the StarCraft II real-time harness later. Separate private repo, synced across machines; the arena harness is light Python plus an HTTP call to a served model.

## Working documents
- [Literature review](LITERATURE.md) — related-work survey, 81 verified references, grouped by theme: agents in real-time games, efficient inference, VLA fast/slow execution, game-state representation, and motion.
- [Decisions and log](DECISIONS.md) — append-only, newest first: what was chosen, why, and what was rejected. Doubles as the project's chronological work log.
- [Embodiment env (E3) design note](embodiment-env-design.md) — proposed third environment (button-press / motion): adds *physical execution time* as a budget term and the LLM→motion-controller handoff. Sibling to the command arena (E1) and StarCraft II (E2).
- [SC2 split (E2) design note](sc2-split-design.md) — spec (for yubopc, Windows) for the slow-commander / fast-executor decomposition in StarCraft II: the hierarchy finding tested on the hard environment.
- [Research plan (crowd-motion)](plan/research-plan.md) — the concrete experimental protocol for the dual-aligned (Li Cheng) direction: system, synthetic-data pipeline, evaluation, milestones.
- [Open-quadrant options](plan/open-quadrant-options.md) — method-agnostic map of how to attack the open quadrant per pillar, so no single tool (tokenization included) is assumed; the substrate for planning.
- [Agent guide](CLAUDE.md) — the schema: conventions, the documentation contract, and how this repo is maintained.

## Sources and assets
- `papers/` — local PDFs of key references (gitignored, not in the remote). The annotated list with links lives in the [literature review](LITERATURE.md).
- `fig/` — figures used by the deck and proposal.

## History
- The [decision log](DECISIONS.md) is the human-readable timeline; `git log` is the full record.

## Reference
- [LLM-wiki pattern](llm-wiki.md) — the knowledge-base pattern this repo's structure is borrowed from.

## Status
Phase-1 build underway: the command-arena scaffold is in [world-commander-bench](https://gitlab.com/worldcommander/world-commander-bench). Next: run it on amax against the deployed model. Current state lives in the [proposal](PROPOSAL.md) and the latest [decisions](DECISIONS.md).
