# World Commander — Index

Natural-language command of agent crowds in real-time strategy games, under latency and memory budgets.

The hub for this repo: start here and follow the links. The structure borrows the
[LLM-wiki pattern](llm-wiki.md) — immutable sources, interlinked working documents,
and a schema file (`CLAUDE.md`) that says how to maintain them.

## Start here
- [Proposal](PROPOSAL.md) — the canonical research program: the spine (execution under budget), the three phases, the Phase-1 wedge, the prior-art map, and the discussion log.
- [Slide deck](world-commander.md) — the presentation view (5 slides plus a related-work appendix); renders to [PDF](world-commander.pdf) and [HTML](world-commander.html).

## Working documents
- [Literature review](LITERATURE.md) — related-work survey, 30+ verified references, grouped by theme: agents in real-time games, efficient inference, VLA fast/slow execution, game-state representation, and motion.
- [Decisions and log](DECISIONS.md) — append-only, newest first: what was chosen, why, and what was rejected. Doubles as the project's chronological work log.
- [Agent guide](CLAUDE.md) — the schema: conventions, the documentation contract, and how this repo is maintained.

## Sources and assets
- `papers/` — local PDFs of key references (gitignored, not in the remote). The annotated list with links lives in the [literature review](LITERATURE.md).
- `fig/` — figures used by the deck and proposal.

## History
- The [decision log](DECISIONS.md) is the human-readable timeline; `git log` is the full record.

## Reference
- [LLM-wiki pattern](llm-wiki.md) — the knowledge-base pattern this repo's structure is borrowed from.

## Status
Proposal stage, no code yet. Next up: a reinforcement-learning fundamentals survey, then the arena v0 design. Current state lives in the [proposal](PROPOSAL.md) and the latest [decisions](DECISIONS.md).
