# game-commander

Natural-language-commanded strategy games under real-time compute budgets.

Created 2026-06-10; its own git repo under `~/github/game-commander`.

## What's here
- `PROPOSAL.md` — the research agenda ("Command at the Speed of Thought"):
  three-layer program (strategy / foresight / embodiment), Phase-1 wedge-paper
  spec (real-time StarCraft II commander benchmark, KV-cache eviction evaluated
  by win rate), prior-art map with verified links. Drafted 2026-06-10 for
  discussion with Dr. Enmao Diao; he gets collaborator access to this repo.

## Status
- Proposal stage. No code yet. Next step: Yubo discusses the proposal with
  Dr. Diao; outcomes get folded back into PROPOSAL.md before any build starts.

## Build & run
- (no build yet — proposal stage)

## Conventions
- **Name things by engineering function**, not vendor SKU (the SKU is secondary).
- **Self-contained**: explain any new term where it appears, or leave it out.
- **Figures**: every figure gets a number + name + caption; never bake an explanatory paragraph into a figure image.
- Clean / monochrome by default; use colour only when it carries information.

## Relationship to memex
Durable knowledge lives in `~/github/memex` (the second brain). Claude Code's
auto-memory is **per-directory**, so memex's *auto-memory* does not load here
(the global `~/.claude/CLAUDE.md` still does) — project must-knows go in this
file. Pull prior art from memex at project start
(`grep` it or discuss in a memex session); ingest transferable lessons back
into memex at session end.
