# Decisions

Append-only log of project decisions: what was chosen, why, what was
rejected and why it was rejected. Newest first. One entry per decision,
written in the session the decision happens. Rationale recorded here is
project-local; transferable lessons still go to memex at milestones.

## 2026-06-20: StarCraft II testbed bring-up (smoke test passing)

**Decision (milestone)**: the StarCraft II testbed runs end-to-end against our own
controllable vLLM. SC2 4.10 Linux (headless) + LLM-PySC2 + Qwen3-4B-AWQ on a
dedicated GPU runs the `2s3z` SMAC task: the LLM agent observed the game, queried
our vLLM, and issued 120 actions with zero errors, completing an episode and
saving a replay. The streaming-command core proven in the arena transfers up, as
intended. Reproducible recipe + integration patches are documented in the bench
repo's `SC2.md`.

**Decision (base + integration)**: build on LLM-PySC2 (full PySC2 action space,
OpenAI-compatible client) rather than reimplement the interface. Three small
patches were needed and are recorded: disable Qwen3 thinking in the API call
(the same gotcha as the arena), route arbitrary served model ids to the OpenAI
client, and point the example config at our endpoint. These live in the gitignored
vendored copy, so the recipe is captured in `SC2.md` to survive re-clone.

**Decision (what's next, unchanged sequencing)**: this is a "the loop drives the
game" smoke test, not the benchmark. Next is to port the arena's real-time layer
onto it (wall-clock decision deadlines, drop late actions, VRAM ceiling, metric
logging), then scale the model for win-rate and sweep KV-cache policies on our own
vLLM (long SC2 context is where eviction finally bites).
**Rejected**: treating the smoke test as a result (no deadline enforcement or
metrics yet); running win-rate on a 4B (used only to validate the pipeline).

## 2026-06-19: Arena concurrent clock done; StarCraft II readiness and sequencing

**Decision (clock)**: the command arena now runs a real concurrent clock. A
background thread ticks the uncontrolled agents every tick_ms of wall-clock time
while the model thinks, so a slow response sees and concedes to a changed world,
not merely a dropped action. Implemented in the bench repo
(`arena/clock.py`, thread-safe `GridWorld`, separate RNGs for command stream vs
NPC moves). This is the shared real-time primitive every later environment reuses,
so it was built and validated in the cheap arena first.
**Why**: a single synchronous tick per command did not model the binding RTS
constraint (the opponent keeps acting during your decision); the concurrent clock
makes "correct but late" cost something, which is what the benchmark measures.

**Decision (SC2 readiness)**: not ready to run StarCraft II today, but
well-positioned. The arena has de-risked the streaming-command core (command to
served-LLM to parsed action to metrics), the served Qwen3-14B endpoint, the
reporting/visualization, and now the concurrent clock. Remaining gaps before a
first SC2 game: (1) install the SC2 Linux game and maps on amax41; (2) stand up
LLM-PySC2 (Python 3.9 env) and point its LLM client at our vLLM; (3) add our
real-time layer on top (wall-clock deadline enforcement, dropped late actions,
VRAM ceiling, metric logging), which neither reference repo provides.

**Decision (sequencing)**: (a) finish the arena concurrent clock first [done];
(b) bring up SC2 + LLM-PySC2 plumbing and run one built-in scenario as a smoke
test; (c) port the real-time deadline layer onto it; (d) the efficiency frontier
sweep (KV-cache, VRAM budgets) comes last and needs our own controllable vLLM,
not the shared inventory-bot instance.
**Why LLM-PySC2 as the base**: it exposes the full PySC2 action space to LLMs and
uses an asynchronous query architecture that keeps latency roughly constant as the
agent population grows, the closest existing match to our concurrent-clock needs.
We add the real-time benchmark layer rather than reinventing the interface.

**Vendored** (gitignored, bench repo `reference/`): `NKAI-Decision-Team/LLM-PySC2`
and `histmeisah/Large-Language-Models-play-StarCraftII` (TextStarCraft II,
Chain-of-Summarization; defeats built-in AI to level 5 on modest hardware), for
interface study.
**Rejected (for now)**: building the SC2 harness from scratch (the references
already wrap PySC2); attempting the efficiency sweep on the shared vLLM (no
control over KV-cache policy or VRAM budget there).

## 2026-06-19: Phase-1 implementation repo, and the compute plan for the first task

**Decision (repo)**: the Phase-1 code lives in a separate repo,
`DreamSoul-AI/world-commander-bench` (private), not in this docs repo. It holds the
command arena now and the StarCraft II harness later (shared streaming-command core).
**Why**: keeps the docs repo (deck, Obsidian vault, proposal) clean, is light to clone
on servers, and lets the benchmark open-source at publication without exposing the
proposal. Synced across machines via GitHub; Claude Code runs on each.
**Rejected**: a `code/` subdirectory in this repo (mixes docs and code, and the private
proposal would block opening the code).

**Decision (compute)**: develop on the MacBook (editor only; M2, 8 GB); run the first
task on **amax41** (3x RTX 2080 Ti, headless, interactive, internet) against its
already-deployed vLLM (Qwen3-14B-AWQ, OpenAI-compatible API) -> no model download.
**yubopc** (RTX 4060, 8 GB, Ada sm_89, Windows/WSL2) is earmarked as the modern
consumer-GPU measurement box; Alliance for the later 1B-70B sweep.
**Why**: fastest path to a first result, and a fleet spanning consumer GPU (yubopc) to
datacentre (Alliance). The shared deployed model is fine for command-following
validation; the efficiency sweep (KV-cache, VRAM budgets) will need our own controllable
vLLM instance -- a later step, not the first task.

## 2026-06-19: Roadmap recast as a continuous arc; a NeurIPS-styled web article becomes the sharing format

**Decision (roadmap)**: replaced the three-phase roadmap with a single continuous
framing: one question (the cost of command at game speed) pursued across the only
thing that progresses, the environment (toy arena -> StarCraft II -> multiplayer ->
full game). Benchmarking, methods, and the interface are a constant loop, not phases;
the deliverable papers are milestones along the arc. Dropped the Preliminaries slide
(redundant with Related Work and the appendix); merged the related-work appendix into
the Related Work section; restored the Command Arena as a detail slide. **Supersedes**
the earlier 2026-06-18 "three phases" recast.
**Why**: the phase table sliced always-true activities (benchmark / method / interface)
into false sequential stages; the environment is the only real axis of progress.

**Decision (sharing format)**: the program is shared as an unlisted, NeurIPS-styled
web article (GitHub Pages, a personal repo with an opaque slug), in place of mailing a
PDF; the Marp deck stays as the presentation version. "Unlisted" is obscurity only
(noindex + unguessable URL, source kept in a deck-only repo); the link is treated as a
semi-secret password, not true access control.
**Why**: a readable article suits a browsing audience better than slides, and a link is
easier to share than a file. ICML's two-column layout does not translate to a scrolling
page, so NeurIPS (single-column) is the faithful template.
**Rejected**: ICML web styling (two columns) and a public Pages site (would expose the
proposal and enable scooping).

**Decision (register)**: slides and the article use a plain academic register, with no
promotional or slogan vocabulary; recorded in CLAUDE.md deck conventions.

**Discussion**: the 2026-06-19 micro-operation-vs-big-picture round is in PROPOSAL.md's
Discussion log; the open decision (which regime to build first) is Open Question #5.

## 2026-06-18: Adopted an index.md hub (LLM-wiki structure); README demoted to a pointer

**Decision**: created index.md as the repository's entry hub — a Map of Content
linking every node (proposal, deck, literature, decisions, sources) with one-line
summaries — adapting the LLM-wiki pattern (see llm-wiki.md). README.md is slimmed to
a one-line pointer to index.md; the slide deck stays a leaf node (a presentation
view), not the entrance.
**Why not the deck as entrance**: world-commander.md is a Marp render artifact
(frontmatter, `<style>`, slide-break `---`, HTML layout); it presents, it does not
navigate.
**Why index.md, not README, as the hub**: the repo is browsed in Obsidian, with
GitHub as the backup/sharing remote rather than a reading surface, so GitHub's
auto-rendered-README advantage does not apply, and index.md matches the borrowed
pattern. README stays as a courtesy landing for any GitHub visitor.
**Decision (links)**: cross-references use relative markdown links (`[text](file.md)`),
not `[[wikilinks]]`. They are clickable on GitHub and in Obsidian, and Obsidian's
graph view includes them, so the graph and backlinks work without breaking GitHub.
**Rejected**: `[[wikilinks]]` (Obsidian-only, break on GitHub) — revisit only if
Obsidian becomes the sole surface and the authoring ergonomics are wanted.
**Revisit when**: the repo outgrows a hand-maintained index (the LLM-wiki pattern
suggests a search tool such as qmd around ~100 sources); far off at the current size.

## 2026-06-18: Subtitle fixed; Roadmap recast as phases (not "three projects"); related-work Landscape appendix added

**Decision (subtitle)**: changed the one-liner from "...in strategy games, under
real-time compute budgets" to "...in real-time strategy games, under latency and
memory budgets", synced across deck, README, PROPOSAL, CLAUDE.md. The old wording
split the standard genre term "real-time strategy (RTS)" in half (real-time
modified *budgets*, not the game) and used the vaguer "compute budget".
**Why "budget" stays**: it is standard top-tier vocabulary in this subfield
(compute budget in scaling laws; cache/memory budget in KV-cache work; latency
budget in real-time ML). The fix was precision, not dropping the word.

**Decision (roadmap)**: recast the Roadmap slide from a "three projects" table into
a three-phase ladder (1 Benchmarks: measure the cost; 2 Methods: drive it down;
3 Interface: ship), with the environment ladder and one paper-sized deliverable per
phase. **Rejected**: keeping "three projects" alongside "three phases" — they are
different cuts (phases = maturity stages, projects = deliverables within), so
presenting them as parallel axes read as incoherent.

**Decision (tokenizer)**: reframed the game-state tokenizer as the flagship Phase-2
method, justified by its mechanism: tokens per decision is the multiplier on both
latency and KV-cache memory, so compressing structured game state attacks the
central cost directly (and extends "tokenization beyond text" to dynamic
entity/event streams, building on Diao's graph tokenization). The prior slide
stated the question but hid the stakes.

**Decision (related work)**: added a two-slide "Related-Work Landscape" appendix
(themed, condensed from LITERATURE.md, vertically centred), leaving the argument
slide untouched; added AlphaStar, WorldMemArena, MotionBricks to LITERATURE.md
(AlphaStar was a genuine gap, absent from all prior refs). **Rejected**: expanding
the argument slide, which is at its legibility ceiling.

**Decision (style)**: slides never use publication-tier words ("top-tier",
"world-class"); recorded in CLAUDE.md deck conventions and scrubbed the one
occurrence on the Roadmap slide.

**Decision (wording)**: avoid "lever" in formal paper prose (a colloquial
metaphor); prefer "mechanism / technique / knob". Kept out of the deck text;
"latency lever" remains in LITERATURE.md notes only.

**Revisit when**: phase boundaries firm up after arena v0 and the RL survey; the
appendix depth may grow if a talk audience wants more.

## 2026-06-14: Folded the literature review into the proposal and deck; narrowed the novelty claim

**Decision**: integrated the top new papers from LITERATURE.md into PROPOSAL.md
(Related work, plus Phase 1 architecture and tokenizer) and the deck's Related
Work slide: HLA, AVA, CivRealm, VideoGameBench, AgileThinker (game agents and the
real-time challenge); Pitfalls of KV Cache Compression and Speculative Actions
(efficiency methods reaching agentic settings); IRIS / Δ-IRIS (learned
world-model tokenizers).
**Decision (claim)**: narrowed the contribution claim. The earlier deck line
"a streaming game ... nobody has run it" is no longer accurate, since
VideoGameBench and AgileThinker now measure real-time LLM play directly. The
precise, still-open gap is restated: the efficient-inference methods (cache
eviction and the rest) have never been scored by win rate, closed-loop, in a
live competitive RTS under a latency and memory budget.
**Why**: honesty after the literature review; an overclaim would not survive
review or Dr. Diao's scrutiny, and the narrower claim is what the related work
actually supports.

## 2026-06-14: Deck trimmed to 5 slides; reordered to overview-then-detail

**Decision**: removed the "Problem and the Vision" slide. For a researcher
audience the video-game motivation is over-explained, and the title slide's
North-Star figure already carries the long-term vision. (The deck loses its only
StarCraft II screenshot; it can move onto the Gap slide if wanted.)
**Decision (order)**: reversed the previous roadmap-before-preliminaries call.
New order: Gap, Preliminaries, Roadmap, Command Arena, so the deck runs problem
to background to overview (the program and its projects) to detail (the first
project's warm-up task). This also removes the forward reference the earlier
order introduced (the roadmap named the tokenizer before Preliminaries defined
it).
**Why**: the Gap slide is the related-work / gap analysis, so with the title
carrying the vision a separate motivation slide is redundant. Five slides now:
Title, Gap, Preliminaries, Roadmap, Command Arena.

## 2026-06-14: Terminology ladder (program / project / task); deck restructured

**Decision (terminology)**: fixed the vocabulary, which had used "paper" and
"project" loosely. **World Commander** is the **research program** (the
umbrella); a **project** is one paper-sized unit of work (top-tier conference
scale); a **task** is a short step inside a project. ("Framework" was rejected
for the whole: it names an artifact, not a research effort.) The roadmap now
lists **projects**, not "papers," and the **command arena is a task** (a
warm-up), not a project, so it left the inventory. The first project is the
real-time commander benchmark.
**Decision (deck structure)**, per Yubo: the author by-line moved directly under
the title; the Roadmap moved to right before Preliminaries (plan first,
background second, which suits an advisor audience and lets the roadmap frame
what follows); the Command Arena is reframed as the warm-up task and now closes
the deck. New order: Problem, Gap, Roadmap, Preliminaries, Command Arena.
**Applies to**: deck (restructured and re-rendered, 6 slides), PROPOSAL.md
("Paper inventory" to "Project inventory"; "agenda" to "program"; "paper" to
"project" throughout), CLAUDE.md (What's here, plus a Conventions bullet).

## 2026-06-14: Deck merged the phases and papers slides into one Roadmap

**Decision**: the deck's phases slide ("The Plan: Three Phases") and papers slide
("What This Produces") overlapped, both walking the phased program. Merged them
into a single closing slide, **"The Roadmap and What It Produces"** (phases,
harness, environments ladder, and north star as the intro; then the
paper-per-phase table). The deck drops to six slides; the Command Arena is now
section 3.
**Why**: the deck skill's one-idea-one-home rule. A differentiate-not-merge first
attempt (leaning the phases slide down to just its arc) left that slide too
sparse, so merging won.
**Scope**: deck only. PROPOSAL.md keeps its separate Plan and Paper-inventory
sections (a prose proposal naturally has both).

## 2026-06-14: Local folder renamed; jobs axis dropped (Execute is the spine)

**Decision (folder)**: the local clone is now `~/github/world-commander` too,
matching the GitHub repo and the session name. CLAUDE.md's path reference is
updated. (Completes the rename deferred on 2026-06-13.)

**Decision (framing)**: dropped the **three-jobs axis** (Execute / Foresee /
Embody). It duplicated the phase axis as a second framing of the same vision,
adding weight a first paper does not need; the vision is already carried by the
North Star and the three phases. The proposal now has **one spine, execution**,
rolled out across the phases. **Foresee** (the what-if / world-model advisor) is
removed entirely. **Embodiment** (crowd-scale motion) is kept as a single later
direction and one paper in the inventory, not a co-equal job, because Yubo wants
the embodiment thread (and the term) in view. The "Competitive-efficiency study"
paper is also dropped from PROPOSAL.md, aligning it with the deck (it was cut
from the deck earlier as too thin to stand alone).
**Why**: first-paper focus, plus the deck skill's own rule against a second
framing of the same idea (one idea, one home).
**Rejected**: removing crowd motion too (option B), which would have reversed
the earlier "keep crowd motion; it's the embodiment line" call.
**Applies to**: deck (removed the Three Jobs slide, renumbered 3.2 to 3, updated
Phase 3), PROPOSAL.md (replaced "The three jobs" section, updated the phases and
Phase 3 prose, trimmed the paper inventory), CLAUDE.md ("What's here").

## 2026-06-13: GitHub repo renamed game-commander → world-commander

**Decision**: renamed the GitHub repo to **DreamSoul-AI/world-commander** to
match the project title (slug is lowercase-hyphenated; GitHub repo names can't
have spaces). The git remote, plus the README and CLAUDE.md headings/refs, are
updated. Supersedes the earlier "repo slug stays game-commander" note.
**Notes**: GitHub redirects the old URL, so links already shared still work.
The local clone stays `~/github/game-commander` for now (renaming it
mid-session would break the working directory); rename separately when
convenient. The frozen v1 archive `yubohuangai/game-commander` is unchanged.

## 2026-06-13: North Star broadened to a revolutionary video game (not genre-bound)

**Decision**: the North-Star framing is **"the next revolutionary video game"**
(cross-genre), not "the next strategy game." Strategy is the research vehicle
and testbed; the command-by-voice interface is not bound to one genre. Updated
the cover caption, slide 1.1's punchline ("Strategy is where we start; the
interface could be the next revolutionary game, in any genre"), and the
PROPOSAL.md end-state.
**Why**: Yubo's point — gaming has stalled for lack of a genuinely new way to
play, and "command instead of click" applies to any genre where directing
beats micro-managing, so the North Star should claim that scope. I had
narrowed it to "strategy game" by scoping to the research, conflating the
vehicle with the dream. Distinction to keep: strategy = the vehicle; a
revolutionary cross-genre game = the North Star.

## 2026-06-13: renamed to "World Commander"; LLM reframed as executor, not commander

**Decision** (both approved by Yubo): (1) project renamed **Real-Time Crowd
Commander → World Commander** (more ambitious, rides the "world model"
resonance; subtitle carries the specifics). Applied to the deck (title +
filenames `world-commander.{md,pdf,html}`), PROPOSAL.md, CLAUDE.md. (2) The
human is the strategic commander; the LLM is the **executor** of that intent,
not an autonomous strategist. The "Decide" job is renamed **Execute**; Foresee
is a what-if advisor the human queries; in Phase 1 the commander is a scripted
command stream, so the benchmark isolates how well/cheaply the LLM carries
orders out (command-following in the arena; win rate while executing a fixed
strategy in StarCraft II). Supersedes the inherited "LLM commander scored by
win rate" framing.
**Why**: Yubo's vision has the human commanding, so an autonomous "LLM
commander" was incoherent and confusing. The executor framing makes the whole
deck consistent and isolates the LLM's contribution (efficiency) from human
strategy.
**Next**: put the framing change to Dr. Diao — it decides what the benchmark
measures, and his efficiency methods are scored by that metric.

## 2026-06-13: cover figures swapped, citations fixed, efficiency framing broadened

**Applied**: cover figures swapped (diagram first = the technical/build view,
command-station photo second = the North-Star product) with reframed captions;
authorship enlarged and reworded to "This proposal grew from..."; citations
fixed to one hyperlink each (EndWar now linked; TextStarCraft II and the CSUR
survey no longer split into two links — the split came from bolding inside the
link); skill citation rule strengthened ("one link per citation, no bold
inside"); the Gap slide broadened from "above all KV-cache eviction" to the
wider efficient-inference toolbox (eviction, quantization, distillation,
smaller models). Kept SVG for the diagram (vector = agent-editable; a raster
PNG is not).
**Held for Yubo's decision**:
1. Rename to **World Commander** (endorsed; a multi-file rename + filenames, so
   it waits for a clean "go").
2. **Human-vs-LLM-commander framing.** Yubo's vision has the *human* as the
   strategic commander, so an "LLM commander scored by win rate" (inherited
   from TextStarCraft II) is incoherent. Recommendation: the LLM is the
   **executor** of a scripted/human command stream; benchmark command-following
   under budget (the arena already does this), and reframe win rate as
   *executing a fixed strategy under budget*, not an autonomous LLM strategist.
   This reshapes the Three Jobs (Decide = executor; Foresee = a what-if advisor
   the human consults) and the win-rate framing. Worth settling with Diao.

## 2026-06-13: deck overhaul — bullets, trimmed to 9 slides, two-figure cover

**Decision**: major revision per Yubo's feedback, and the slide-decks skill
gained the lessons behind it (bullets-not-paragraphs; captions on every
figure incl. the cover; don't-name-what-you-can't-show; no hype words ahead
of evidence; no discussion asides on slides; don't over-detail future
phases; de-dup table columns). Deck changes: all prose slides converted to
short bullets; the cover now carries two captioned figures (command-station
photo + the multiplayer diagram, moved up from its own slide) with larger
authorship; the Missing-Piece and Gap slides merged into one (1.2); the
Phase column de-duped (cells "1/2/3"); the arena figure redrawn to
four-direction movement only (no sitting), enlarged, and the "costs weeks,
not months..." sequencing aside removed; the StarCraft slide cut to a plain
three-bullet "next environment" (no "flagship/wedge", no premature
benchmark detail, since the arena isn't built); Age of Empires dropped from
1.1 (no AoE figure to show; StarCraft suffices); the Open Questions slide
removed (the whole proposal is open questions); the dedicated multiplayer
slide removed (figure now on the cover). 12 → 9 slides.
**Why**: audiences listen, they don't read paragraphs; the deck was
long-winded, over-promised unbuilt phases, and used hype ahead of results.
The skill now encodes all of this so it persists.

## 2026-06-13: created a slide-decks skill; applied it to fix the deck

**Decision**: created `~/.claude/skills/slide-decks/SKILL.md` codifying
Yubo's deck preferences (Keynote-White visual style, paper-numbered
structure, concise-but-large writing, figure/citation conventions, a
redundancy audit, and an anti-patterns list of the specific mistakes made
this session). Applied it to the deck: the cover is now a clean title page
(title, scope, large hero, author — no prose, which removes the cover/1.1
duplication); slide 1.2 is condensed to one setup sentence plus the
research question; the Gap (2) is cut to two tight paragraphs (both
references kept); Preliminaries (3) reworded to remove the "Phase 1" and
"commander/executor split" forward references. Re-audit: the
budget-frontier framing now appears once (on 5.2).
**Why**: Yubo was justifiably unhappy with inconsistent slide-writing and
proposed a skill as the durable fix — a written spec stops the per-turn
drift. The slide edits follow his feedback on slides 1-5.
**Note**: the skill lives in `~/.claude/skills/` (global, auto-triggers
from next session). It can be moved into `~/github/claude-config` if Yubo
wants it version-controlled and synced like his CLAUDE.md.

## 2026-06-13: cover slide de-teched to a storytelling hook

**Decision**: on the title slide, replace the abstract-plus-research-
question with a short storytelling hook (the problem + the vision). The
cost/latency/memory framing and the formal research question move off the
cover; the question now appears once, on slide 1.2.
**Why**: Yubo's point — the cover is for background and storytelling, so
the technical thesis is premature there; and the research question was
near-verbatim duplicated between the cover and slide 1.2 (the redundancy
the numbered structure is meant to remove).

## 2026-06-13: deck reorganized into a paper-style numbered structure

**Decision**: restructure the deck into numbered sections, with muted
section-number prefixes on slide titles: 1 Motivation (1.1 the problem &
vision, 1.2 the missing piece + research question), 2 The Gap, 3
Preliminaries, 4 Approach (4.1 three jobs, 4.2 three phases), 5 Phase 1
(5.1 the command arena, 5.2 the StarCraft II benchmark), 6 Outlook (6.1
the papers, 6.2 the multiplayer endgame), 7 Open Questions. Added a new
**Preliminaries** slide (RL, efficient inference, VLA/π0, the SC2 stack,
tokenization), placed before the Approach per paper convention. Trimmed
repeated statements of the budget-frontier philosophy.
**Why**: Yubo found the deck illogically organized and redundant; a
paper-style index forces a hierarchy, makes redundancy visible (same idea
→ same section), and matches how Dr. Diao reads. He noted papers put
preliminaries before the method, so Preliminaries is section 3.
**Rejected**: heavy academic numbering on every line (kept the numbers as
light, muted title prefixes so the slides still read visually).

## 2026-06-13: removed the "Key Bet" architecture slide (medium-phase, redundant)

**Decision**: cut the slide "The Key Bet: Slow Thinker, Fast Actors" (the
commander/executor split, the π0 analogy, the DOOM result, the learned
tokenizer). Deck 12 → 11 slides; the multiplayer figure renumbered 4 → 3.
**Why**: Yubo's point — the architecture choice and the state tokenizer
are already listed as Phase-1 variables on the Phase 1 slide ("the
architecture; how game state is encoded"), so a whole slide elaborating
them is redundant, and the deep treatment is Phase 1-2 *methods*, which
over-weights medium-phase work in a deck whose focus is the near-term
arena. The supporting points (DOOM, π0) stay in PROPOSAL.md;
`fig/sc2-featurelayers.jpg` kept in the repo, just unused now.

## 2026-06-13: closing slide de-pitched to "Open Questions"

**Decision**: replace the "Why Now, Why Us, What's Next" closing slide
with a plain "Open Questions" slide — the four decisions to make together
(first-paper scope, compute envelope, venue/timing, product-vs-research).
**Why**: Yubo found it redundant (the "be first" point was already on the
gap slide; the collaboration rationale needn't be sold to the collaborator
himself) and too promotional (grant/investor-pitch tone — wrong register
for a working discussion with Dr. Diao). The open questions are the
genuinely useful, collaborative way to end. The "why this collaboration"
rationale still lives in PROPOSAL.md for any wider audience.

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
