# game-commander

Natural-language command of agent crowds in strategy games, under real-time compute budgets.

Created 2026-06-10; its own git repo under `~/github/game-commander`.

## What's here
- `PROPOSAL.md` — the research agenda ("Real-Time Crowd Commander"). Two axes:
  three jobs (Decide / Foresee / Embody = the system's capabilities) and
  three phases (1 Benchmarks / 2 Methods / 3 Real interface = the
  timeline); environments are a complexity ladder (arena → StarCraft II →
  multiplayer → game) folded into the phases, not a separate scheme.
  Phase-1 wedge spec (real-time StarCraft II commander benchmark plus the
  command-arena warm-up, KV-cache eviction evaluated by win rate), paper
  inventory, prior-art map with verified links, discussion log. Drafted
  2026-06-10 for discussion with Dr. Enmao Diao. Canonical remote:
  `DreamSoul-AI/game-commander` (private org repo — Diao sees it as org owner,
  no invite needed; visible to all org members). A frozen v1 snapshot sits
  archived at `yubohuangai/game-commander`.
- `real-time-crowd-commander.md` / `.pdf` / `.html` — the Marp slide deck
  (named after the title, not "deck"): a clean, small mirror of PROPOSAL.md
  for presenting and sharing at any time, and Yubo's own review artifact.
  Style: Keynote-White (ported from the weekly-report decks); no em-dashes
  anywhere (external audience), Canadian spelling, self-contained slides,
  citations as Handle (Venue Year). Slide 1 is a dense title-plus-abstract
  page (top-aligned, no wasted whitespace).
- `DECISIONS.md` — append-only decision log: one entry per decision
  (what / why / rejected / revisit-when), newest first.

## Documentation workflow (the contract)
- PROPOSAL.md is canonical. Any session that changes it substantively
  must update real-time-crowd-commander.md and re-render both outputs
  before committing:
  `marp real-time-crowd-commander.md --html -o real-time-crowd-commander.pdf --allow-local-files && marp real-time-crowd-commander.md --html -o real-time-crowd-commander.html --allow-local-files`
  The `--html` flag is required — without it Marp strips the layout
  `<div>`s and the two-column slides collapse. Verify dense slides
  visually: `pdftoppm -png -r 95 -f N -l N -singlefile real-time-crowd-commander.pdf /tmp/slide`.
  PDF is the sharing format; the `.html` is for presenting (it plays
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
