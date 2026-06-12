# game-commander

Natural-language-commanded strategy games under real-time compute budgets.

Created 2026-06-10; its own git repo under `~/github/game-commander`.

## What's here
- `PROPOSAL.md` — the research agenda ("Command at the Speed of Thought"):
  three-layer program (strategy / foresight / embodiment), four-rung
  environment roadmap, Phase-1 wedge-paper spec (real-time StarCraft II
  commander benchmark, KV-cache eviction evaluated by win rate), paper
  inventory, prior-art map with verified links, discussion log. Drafted
  2026-06-10 for discussion with Dr. Enmao Diao. Canonical remote:
  `DreamSoul-AI/game-commander` (private org repo — Diao sees it as org owner,
  no invite needed; visible to all org members). A frozen v1 snapshot sits
  archived at `yubohuangai/game-commander`.
- `DECK.md` / `DECK.pdf` — the Marp slide deck: a clean, small mirror of
  PROPOSAL.md for presenting and sharing at any time, and Yubo's own
  review artifact. Style: Keynote-White (ported from the weekly-report
  decks); no em-dashes anywhere (external audience), Canadian spelling,
  self-contained slides, citations as Handle (Venue Year).
- `DECISIONS.md` — append-only decision log: one entry per decision
  (what / why / rejected / revisit-when), newest first.

## Documentation workflow (the contract)
- PROPOSAL.md is canonical. Any session that changes it substantively
  must update DECK.md and re-render both outputs before committing:
  `marp DECK.md --html -o DECK.pdf --allow-local-files && marp DECK.md --html -o DECK.html --allow-local-files`
  The `--html` flag is required — without it Marp strips the layout
  `<div>`s and the two-column slides collapse. Verify dense slides
  visually: `pdftoppm -png -r 95 -f N -l N -singlefile DECK.pdf /tmp/slide`.
  PDF is the sharing format; DECK.html is for presenting (it plays
  GIF/video once the project has its own footage).
- Any decision made in conversation gets a DECISIONS.md entry in the
  same session.
- Transferable lessons still get proposed for memex ingestion at
  milestones; DECISIONS.md holds project-local rationale only.

## Status
- Proposal stage. No code yet. First discussion round with Dr. Diao
  (WeChat, 2026-06-11): direction endorsed; pointers to robot
  vision-language-action architectures (π0) and to the long arc being
  "RL in a virtual world". Outcomes folded into PROPOSAL.md (Discussion
  log section).
- Next: Yubo surveys RL fundamentals and consults RL colleagues; arena
  v0 design comes after that.

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
