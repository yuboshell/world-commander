# World Commander

Natural-language command of agent crowds in real-time strategy games, under latency and memory budgets.

Created 2026-06-10; its own git repo under `~/github/world-commander`.

## What's here
- `index.md` — **the entry hub** (start here): a Map of Content that links
  every node below with a one-line summary, adapting the `llm-wiki.md` pattern.
  Update its catalog whenever a file is added, renamed, or removed.
- `PROPOSAL.md` — the research program ("World Commander"). One spine,
  **execution** (the LLM carries out the human commander's intent at game
  speed, under latency and memory budgets), rolled out across three phases
  (1 Benchmarks / 2 Methods / 3 Real interface); environments are a
  complexity ladder (arena → StarCraft II → multiplayer → game) folded into
  the phases. Embodiment (crowd-scale motion) is one later direction, not a
  near-term job; the earlier "three jobs" axis and the Foresee what-if
  advisor are dropped.
  Phase-1 wedge spec (real-time StarCraft II commander benchmark plus the
  command-arena warm-up, KV-cache eviction evaluated by win rate), project
  inventory, prior-art map with verified links, discussion log. Drafted
  2026-06-10 for discussion with Dr. Enmao Diao. Canonical remote: GitHub
  `yuboshell/world-commander` (git remote `yuboshell`; the working branch tracks it),
  served publicly via GitHub Pages at https://yuboshell.github.io/world-commander/.
  GitLab `worldcommander/world-commander` (remote `gitlab`) is kept as a mirror; push
  both. Retired: the former GitHub org remote `DreamSoul-AI/world-commander` (2026-06-20
  suspension; still the stale local `origin`, so push by explicit remote name) and the
  frozen v1 snapshot `yubohuangai/game-commander`.
- `world-commander.md` / `.pdf` / `.html` — the Marp slide deck
  (named after the title, not "deck"): a clean, small mirror of PROPOSAL.md
  for presenting and sharing at any time, and Yubo's own review artifact.
  Style: Keynote-White (ported from the weekly-report decks); no em-dashes
  anywhere (external audience), Canadian spelling, self-contained slides,
  citations as Handle (Venue Year); never use publication-tier words ("top-tier", "world-class") on slides, even though every project still targets a top-tier venue. Plain academic register
  throughout: no promotional or slogan-style vocabulary and no coined catchphrases
  (e.g. "gap", "lever", "the new axis", "loses the match", "warning shots"); describe
  prior work plainly and keep claims measured. Slide 1 is a dense title-plus-abstract
  page (top-aligned, no wasted whitespace).
- `DECISIONS.md` — append-only decision log: one entry per decision
  (what / why / rejected / revisit-when), newest first.

## Documentation workflow (the contract)
- PROPOSAL.md is canonical. Any session that changes it substantively
  must update world-commander.md and re-render both outputs
  before committing:
  `marp world-commander.md --html -o world-commander.pdf --allow-local-files && marp world-commander.md --html -o world-commander.html --allow-local-files`
  The `--html` flag is required — without it Marp strips the layout
  `<div>`s and the two-column slides collapse. Verify dense slides
  visually: `pdftoppm -png -r 95 -f N -l N -singlefile world-commander.pdf /tmp/slide`.
  PDF is the sharing format; the `.html` is for presenting (it plays
  GIF/video once the project has its own footage).
- Any decision made in conversation gets a DECISIONS.md entry in the
  same session.
- index.md is the entry hub; cross-references use relative links
  (`[text](file.md)`), not `[[wikilinks]]`, so they work on GitHub and in
  Obsidian's graph view alike.
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
- **Terminology ladder**: *World Commander* is the **program**; a **project** is one paper-sized unit (top-tier conference scale); a **task** is a short step within a project.
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
