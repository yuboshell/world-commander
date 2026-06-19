# raw/ — reading inbox (clips not committed)

A staging area for Markdown clipped from the web (Obsidian Web Clipper) and other raw
reading. **The clips themselves are gitignored** (`raw/*`); only this README is tracked.

## Why

A web clip is a full, uncurated, partly-copyrighted article. The repository should carry
the *distilled* node, not the dump: the clip is reproducible (re-clip anytime), and the
value worth keeping is the summary.

## Workflow (the index.md / llm-wiki pattern)

1. **Clip** a page into `raw/` (Obsidian Web Clipper, or drop the Markdown here).
2. **Read** it.
3. **Distil** into a curated node, routed by scope:
   - **General, cross-project concept** (e.g. vision-language-action models) -> a concept
     note in `~/github/memex/` via its `raw/` -> ingestion workflow. memex is the durable
     second brain; do not rebuild that pipeline here.
   - **Project-specific** angle -> a short entry in [`LITERATURE.md`](../LITERATURE.md),
     linked from [`index.md`](../index.md).
4. The clip stays here as your source; the committed artifact is the node.

## First worked example

The VLA page (Dr. Diao's pointer, 2026-06-19) was distilled into a memex concept note
(`memex/raw/Vision-Language-Action Models.md`, staged for ingestion). The project-specific
angle (VLA = the fast executor in the commander/executor split) already lives in
`LITERATURE.md` via the π0, OpenVLA, and Fast-in-Slow entries, so nothing was duplicated here.
