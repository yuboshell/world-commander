# Decisions

Append-only log of project decisions: what was chosen, why, what was
rejected and why it was rejected. Newest first. One entry per decision,
written in the session the decision happens. Rationale recorded here is
project-local; transferable lessons still go to memex at milestones.

## 2026-06-13: kept the vector hero — new "multiplayer endgame" slide (Figure 4)

**Decision**: instead of discarding the vector hero (`fig/hero.svg`) when
the command-station photo took the title slide, give it a dedicated slide
before the closing — "Where It Leads: Players vs. Players" — with the SVG
as Figure 4 and a caption on the competitive-efficiency idea (does a fast
small commander beat a slow large one, settled by Elo). Deck now 12 slides.
**Why**: Yubo likes both images; they are different styles (photoreal vs
clean diagram), so both earn a place. The SVG's two-players-two-armies
view finally *shows* the multiplayer endgame the deck previously only
stated in words.

## 2026-06-13: bigger content; command-station hero image on the title slide

**Decision**: (1) increase deck content size for space efficiency — base
font 24→27, dense-slide font 20→22, slide titles up, padding trimmed to
34/50/36/50; verified no overflow on the densest slides (gap, Phase 1,
paper inventory). (2) Replace the title-slide placeholder SVG diagram with
a generated photoreal hero, `fig/command-station.png` (GPT Image 2): a
player at a modern console commanding an Age-of-Empires-style battle by
voice — headset, raised hand, blue-vs-amber armies on a curved screen,
audio waveform on the desk. Plain flat image (no drop shadow, no rounded
corners — the initial shadow/rounding was removed as unnecessary
decoration per the deck's clean/flat rule); two-column title layout kept
(text left, image right).
**Why**: Yubo asked to make the content bigger and to add the generated
image he liked. The command-station image shows the *interaction* (a
player commanding by voice through a screen) — the project's actual idea —
not just the game world, which is why it beats the earlier medieval-battle
poster.
**Rejected**: full-bleed title background with overlaid title text (bigger
redesign; can revisit); deleting the vector hero (kept as `fig/hero.svg`,
a clean fallback / content-slide option).

## 2026-06-13: hero — players and agents drawn as distinct species

**Decision**: redraw so the real-human players and the virtual-character
agents no longer look alike. Players = solid filled human silhouettes
wearing comms headsets, standing OUTSIDE a thin rounded-rectangle
"screen," pointing in. Agents = line-art pictogram characters INSIDE the
screen (the virtual world). Solid-vs-line plus outside-vs-inside makes
the real/virtual split read at a glance, even at thumbnail size.
**Why**: Yubo noted players and agents were the same pictogram, so they
read as the same kind of being; players are real people commanding,
agents are the virtual characters being commanded.
**Rejected**: one figure style for both (ambiguous); a screen border
alone without restyling the players (weaker).

## 2026-06-13: hero revised — two commanders, embodied characters in motion

**Decision**: redraw the title-slide hero so it shows **two** commanders
(Player 1 / Player 2, colour-coded) each directing their own crowd in a
shared real-time arena, and draw the agents as small human figures in
motion (running with speed lines, walking, one sitting to hold) rather
than dots. Each team is ~10 figures in three depth-receding ranks (front
large and in motion, ranks behind smaller), so the crowds read as armies,
not squads. Also revised the GPT Image 2 prompt to match. Attribution line
reworded "based on" → "grown from ... under the guidance of."
**Why**: Yubo's point — the North Star is a multiplayer game, and the
goal is commanding virtual characters with real motion, so the title hero
(which represents the vision) should show both. The Phase-1 arena figure
(Figure 2) still uses abstract dots, keeping the body of the deck honest
about the current first step: hero = vision, arena = reality.
**Rejected**: single commander + abstract dots on the title slide
(under-sold the multiplayer, embodied North Star).

## 2026-06-12: title slide gains a hero illustration (hand-authored SVG)

**Decision**: add a vector hero illustration (`fig/hero.svg`) to the
right column of the title slide, depicting the whole idea in one picture:
a speech bubble issuing two colour-keyed orders ("Blue, push north." /
"Amber, hold the door."), command-flow lines fanning to a crowd of
colour-tagged agents, blue ones pushing north (motion arrows), amber
holding (seat lines), a clock with a sweep arrow for real time, and a
north compass. Title slide is now a two-column title-plus-abstract +
hero layout.
**Why**: Yubo asked for an image to make the deck look fancier. No
text-to-image tool is available in this environment, and a hand-authored
SVG is the better fit anyway: crisp at any size, license-clean, and
on-brand (monochrome base; colour reserved for agent identity, which
carries information, per the project figure conventions). It also reuses
the visual language of the arena figure (Figure 2), so the deck is
visually cohesive.
**Rejected**: a raster AI-generated illustration (no tool; would clash
with the clean Keynote-White style and risk licensing).
**Revisit when**: the project has real screenshots/renders to use as the
hero, or a text-to-image tool becomes available and a photographic look
is wanted.

## 2026-06-12: title finalized "Real-Time Crowd Commander"; dense title slide; files renamed

**Decision**: final title **Real-Time Crowd Commander** (Yubo's own merge
of the recommended "Real-Time Commander" with the "Crowd" object),
superseding "At Your Command." The title slide is rebuilt as a dense,
top-aligned title-plus-abstract page (title, subtitle, a three-sentence
abstract, the research question, authorship) to obey the
high-space-efficiency style rule; the old centered layout left too much
blank space. Deck files renamed from `DECK.*` to
`real-time-crowd-commander.{md,pdf,html}` (named after the title, not the
wooden "deck"); CLAUDE.md workflow commands updated to match. Repo slug
stays `game-commander`.
**Why**: Yubo's taste clarified to informative-over-clever. "At Your
Command" was clever but conveyed nothing; the earlier rejects were flat
("Commanding Crowds") or speed-only ("Command at the Speed of Thought").
"Real-Time Crowd Commander" names all three dimensions at once: real-time
(the constraint), crowd (the object), commander (the act).
**Rejected**: "At Your Command" (vague), "Game Commander" (generic
baseline), and the single-dimension forms "Real-Time Commander" /
"Crowd Commander" / "LLM Commander" (Yubo combined the first two).

## 2026-06-12: organization simplified to two axes (jobs + phases)

**Decision**: collapse the three overlapping schemes (layers / rungs /
phases) to two clear axes. (1) **Three jobs** = the system's
capabilities: Decide (the commander), Foresee (the world model), Embody
(units move). Renamed from "layers"; the Phase status column is removed.
(2) **Three phases** = the timeline: Phase 1 Benchmarks (command arena
warm-up + StarCraft II flagship), Phase 2 Methods, Phase 3 Real
interface. The word "rung" is retired; the environments become a
complexity-ladder line (toy room → StarCraft II → multiplayer → game)
folded into the phases, not a third naming scheme. The arena is now
explicitly the first testbed of Phase 1, not a free-floating "rung 0."
Applied to PROPOSAL.md (rewritten), DECK.md (slides 5–8 + inventory got
a Phase column, build-ordered), CLAUDE.md.
**Why**: Yubo (correctly) found the three schemes a mess. Rungs and
phases were near-duplicate time axes that did not line up 1:1 (Phase 1 =
SC2 = rung 1, but rung 0/arena was no phase, and Phase 2/methods was no
rung), so no reader could tell what belonged where. Two orthogonal axes
(parts vs. order) with the environments as a picture is the fix.
**Rejected**: collapsing to a single timeline (loses the capability
framing that shows scope and collaborator fit); keeping three schemes
with a map (does not remove the root cause). Chosen by Yubo from a
three-way comparison.
**Revisit when**: a fourth job or phase appears; or a venue wants the
formal three-layer-stack framing back.

## 2026-06-12: title changed to "At Your Command" (supersedes "Commanding Crowds")

**Decision**: final title is **At Your Command** (chosen by Yubo from a
four-way vivid-options comparison), superseding the same-day pick
"Commanding Crowds," which Yubo found accurate but flat (土/呆).
Subtitle unchanged. Applied across PROPOSAL.md, DECK.md, CLAUDE.md;
repo slug stays `game-commander`.
**Why**: "At Your Command" is the subordinate's reply, evoking troops
awaiting orders, the commander relationship at the heart of the idea.
More vivid than the plain "Commanding Crowds" while the subtitle still
carries the literal meaning (subject + object + speed).

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
