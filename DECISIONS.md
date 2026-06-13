# Decisions

Append-only log of project decisions: what was chosen, why, what was
rejected and why it was rejected. Newest first. One entry per decision,
written in the session the decision happens. Rationale recorded here is
project-local; transferable lessons still go to memex at milestones.

## 2026-06-12: title changed to "Commanding Crowds"

**Decision**: the proposal and deck are titled **Commanding Crowds**,
subtitle "Natural-language command of agent crowds in strategy games,
under real-time compute budgets." Applied across PROPOSAL.md, DECK.md,
CLAUDE.md, README.md. The git repo and project slug stay
`game-commander`.
**Why**: the prior title, "Command at the Speed of Thought," named only
the speed (the verb). The work is equally about the subject (who
commands, in natural language, possibly several players) and the object
(crowds of agents being controlled). "Commanding Crowds" carries the
command-to-crowd relationship and spans every layer; the subtitle now
names the object explicitly.
**Rejected**: "Words to Armies" (vivid but less professional), plain
"Game Commander" (Yubo's baseline; carries none of language/crowds/
speed itself), "Crowds at the Speed of Thought" (object + speed, but
keeps a tired riff). Chosen by Yubo from a four-way comparison.

## 2026-06-12: deck v3: rebuilt as a narrative, not an outline

**Decision**: restructure the deck for storytelling over term-dumping.
Slide 1 is now a title + authorship slide ("based on Yubo Huang's
interest and insight, with guidance from Dr. Enmao Diao"), not an
outline. Slide 2 is the personal ideation story (love RTS, strategy
buried under manual labour, players should command). The arc:
idea -> missing piece is speed + the question -> the gap -> three
layers -> roadmap -> arena -> Phase 1 -> the architecture bet ->
papers -> why now / why us / what's next. The dedicated
reinforcement-learning slide is removed (that framing is for our
discussion, lives in PROPOSAL.md's discussion log and DECISIONS.md, not
the audience deck). The gap is reframed to state *what* it is
(efficiency methods never tested closed-loop in a live game), with the
survey as supporting citation, not the subject; survey now cited in
standard form, "LLM Game Agents Survey (CSUR 2026)." The weak open-
questions list is replaced by three substantive discussion points
(first-paper scope, compute envelope, product-vs-research). Method
names (StreamingLLM, OBCache, etc.) demoted to parenthetical examples
rather than bulleted lists. 11 slides.
**Why**: an ideation pitch persuades by narrative; a wall of acronyms
on slide 1 repels. A reader cares what the gap is, not where it is
named.
**Rejected**: keeping the outline-first structure; an Age of Empires IV
screenshot on the story slide (no license-clean source fetched; using a
credited PySC2 still instead, bridged by caption). Render still needs
the `--html` flag; title slide uses `_paginate: false` and
`margin: 0 auto` to centre the authorship block.
**Revisit when**: arena v0 yields own screenshots; or an audience
beyond Diao needs a different framing.

## 2026-06-12: deck v2: figures, linked citations, glosses, RL slide, HTML channel

**Decision**: per Yubo's review, the deck gains three figures (two
credited PySC2 video stills from DeepMind: real gameplay and feature
layers; one self-authored arena SVG with commands colour-keyed to
agents); every citation is hyperlinked; the survey claim is pinpointed
to §8.1 of the ACM CSUR 2026 survey with an exact quote; on-slide
glosses added for no-op, DOOM, harness, grounding, generated motion,
and wedge; a "Where this sits relative to RL" slide carries the
round-1 framing (credited to Dr. Diao); "listen" joins the commander
loop in both deck and PROPOSAL.md; author/pointer line moved from
slide 1 to the final slide; `DECK.html` is now exported alongside the
PDF (HTML plays GIF/video for future dynamic content). Rendering needs
the `--html` flag, or layout divs are stripped.
**Why**: games need showing, not describing; the deck must be
self-contained for audiences that will include RL researchers Yubo
consults; Diao's round-1 content belongs in the shareable artifact.
**Rejected**: deleting the attribution line entirely (a standalone PDF
needs provenance, so it moved to the last slide instead); embedding
GIF/video now (no owned footage yet).
**Revisit when**: arena v0 produces its own screenshots or clips to
replace the borrowed PySC2 stills.

## 2026-06-12: documentation architecture: deck + proposal + decisions, one repo, one rule

**Decision**: `PROPOSAL.md` stays the single comprehensive source of
truth. `DECK.md`/`DECK.pdf` (Marp, Keynote-White style) is its clean,
small mirror for presenting, sharing, and Yubo's own review. This file
records decisions. Update rule: a session that substantively changes
PROPOSAL.md updates the deck before committing; a decision made in
conversation gets an entry here in the same session.
**Why**: shareable at any moment; one clone, versioned together,
org-visible; three files and one rule keeps the workflow from going
clunky.
**Rejected**: hosting the deck in the `~/report` weekly flow (that
machinery targets the Prof. Cheng channel; this project's boundary rule
keeps the lines separate); splitting the proposal into multiple files
now (premature: split the Discussion log out only when it outgrows the
document, around the 300-line mark).
**Revisit when**: PROPOSAL.md passes ~300 lines, or per-audience deck
variants become necessary.

## 2026-06-11: RL framing scoped to literacy now, depth at Phase 2-3

**Decision**: treat Dr. Diao's "essentially RL in a virtual world" as
true of the substrate (PySC2 is an RL environment; win rate is a
reward; memory probes test credit assignment) and of the long arc, not
of Phase 1's method. Near-term action: RL literacy (Sutton & Barto
early chapters, the U of A Coursera specialization, Spinning Up), not
RL training.
**Why**: Phase 1 trains nothing; its novelty is the efficiency
frontier. Real-time RL is the reconciling frame: latency inside the
decision problem.
**Rejected**: reframing the wedge as an RL paper (wrong reviewers,
wrong novelty claim).
**Revisit when**: Phase 2 methods work begins (learned commanders or
executors, foresight layer).

## 2026-06-11: π0 analogy recorded as a Phase-1 variable, not the bet

**Decision**: adopt Dr. Diao's robotics pointer (π0: slow
vision-language backbone driving a fast action expert) as a second
independent support for the commander/executor architecture variable,
alongside the 1.3M-parameter DOOM result.
**Why**: robotics and the DOOM result converged on the same split from
different directions; a game iterates that split more cheaply than
hardware. Note π0 is imitation-trained, not RL.
**Rejected**: committing to the split as *the* architecture before the
benchmark measures it against the monolithic commander.

## 2026-06-11: arena v0 strips motion: discrete-direction agents only

**Decision**: rung 0 of the roadmap uses colour-tagged abstract agents
moving in discrete directions; full-body generated motion is deferred
to the embodiment layer on the same harness.
**Why**: removes the three heaviest risks at once (no
per-entity-commanded crowd dataset exists; no rendering or motion
engineering; no mushy motion-quality metrics). Difficulty relocates to
the command stream: rate, compositional addressing, commands that
depend on remembered state.
**Rejected**: starting with realistic human crowds in a room (the
original mental picture): right destination, wrong first step. The
Cheng-facing motion rung arrives later with the harness and metrics
unchanged.

## 2026-06-10: proposal shared via the DreamSoul-AI org repo

**Decision**: canonical repo `DreamSoul-AI/game-commander`; Dr. Diao
reads it as org owner, no invitation; frozen v1 snapshot archived at
`yubohuangai/game-commander`.
**Why**: zero friction for Diao; visible to all org members by
construction.
**Rejected**: a memex branch (GitHub access is repo-level: a
collaborator would see the whole knowledge base); a personal-repo
invite (don't make Diao accept an invitation).

## 2026-06-10: environment: StarCraft II, not OpenRA or microRTS

**Decision**: build Phase 1 on the TextStarCraft II / LLM-PySC2 stack
with the clock unpaused.
**Why**: inherit working infrastructure; the strongest prior-art line
lives there; the built-in AI ladder supplies fixed opponents.
**Rejected**: OpenRA and microRTS (lighter engineering, but weaker
baselines and far less recognizable to reviewers).

## 2026-06-10: Phase 1 scope: benchmark + tokenizer; voice deferred

**Decision**: the wedge is the benchmark/harness, the efficiency
frontier, and the strategic-memory probes, with the game-state
tokenizer module attached (inside the paper or standalone: still open).
The human-in-the-loop voice study is deferred to Phase 3.
**Why**: the narrow paper publishes fast; voice adds human-subjects
machinery without sharpening the efficiency question.
