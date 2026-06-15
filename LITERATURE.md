# World Commander — Literature Review

Related-work survey for the World Commander program, compiled 2026-06-14.

- **[N]** = new from this review; **[P]** = already cited in PROPOSAL.md.
- **★** = read first.
- Links are arXiv abstract pages or official venue pages, verified during the
  search. A few residual uncertainties are flagged at the end.

The program in one line: a human commander gives natural-language commands and
an LLM executes them as in-game actions in real-time strategy games, under hard
latency and memory budgets and a live (unpausable) game clock; the research bet
is to measure and drive down that cost, and to test efficient-inference methods
closed-loop inside a live game (scored by win rate), which prior work does not do.

---

## Read these first (10)

1. **HLA** (§3) — the closest existing *system*: slow-mind / fast-mind / executor for real-time human-AI command in a game.
2. **AVA / AVACraft** (§1) — the closest *artifact* to our setting: a VLM issuing unit commands in StarCraft II, with measured latency.
3. **VideoGameBench** (§1) — the clean real-time-vs-paused ablation that isolates latency as the failure mode (our methodology).
4. **AgileThinker / Real-Time Reasoning Gym** (§1) — formalizes "reason while the world moves": the reasoning-depth vs latency tradeoff.
5. **Adaptive Command** (§1) — LLM as executor of a human's spoken intent in StarCraft II (our framing, already instantiated).
6. **Pitfalls of KV Cache Compression** (§2) — evidence that eviction silently drops the wrong instruction (our "lose the match" hypothesis, in static form).
7. **Speculative Actions** (§2) — action-level speculative decoding, evaluated in a gaming loop (a latency lever we can adopt).
8. **π0** (§3) — the slow-backbone / fast-action-expert architecture we would adapt for commander plus executors.
9. **Graph Tokenization** (§4) — Diao's graph-to-tokens recipe, the template for our game-state tokenizer.
10. **IRIS / Δ-IRIS** (§4) — learned tokenizer plus Transformer world model, with the explicit goal of fewer tokens per decision.

---

## 1. LLM agents in real-time games

**★ HLA** — LLM-Powered Hierarchical Language Agent for Real-time Human-AI Coordination. Liu, Yu, Gao et al. *AAMAS 2024*. [arXiv 2312.15224](https://arxiv.org/abs/2312.15224). **[N]**
A three-tier agent for real-time human-AI coordination in Overcooked: a "Slow Mind" LLM for intent reasoning and dialogue, a lightweight "Fast Mind" LLM emitting macro-actions, and a reactive Executor for atomic actions. Engineered to keep LLM reasoning while meeting game-speed latency.
*Relevance:* the closest published system to World Commander — same slow-brain / fast-policy / executor decomposition, same real-time-game-under-latency constraint, same human-gives-commands setup. Primary work to build on and differentiate from (it is cooperative two-player Overcooked; we are one human commanding crowds in an adversarial RTS).

**★ AVA / AVACraft** — AVA: Attentive VLM Agent for Mastering StarCraft II. Ma, Fu, Zhang, Ghanem, Li. *arXiv 2026*. [arXiv 2503.05383](https://arxiv.org/abs/2503.05383). **[N]**
A multimodal StarCraft II benchmark plus a training-free VLM agent that takes screenshots plus structured unit metadata and emits move/attack/ability commands. Reports the numbers we care about: ~2 Hz decision rate, 2.3 s/decision (proprietary), 1.8–4.5 s/step (open-source on one A100).
*Relevance:* the closest existing artifact to our interface (same game, "VLM emits unit commands"). The natural baseline whose latency we measure and attack; differs in being an autonomous strategist rather than an executor of a human's intent.

**★ VideoGameBench** — Can Vision-Language Models complete popular video games? Zhang, Griffiths, Narasimhan, Press. *arXiv 2025*. [arXiv 2505.18134](https://arxiv.org/abs/2505.18134). **[N]**
Ten 1990s games from pixels plus a high-level objective, in two modes: real-time (clock runs during inference) and "Lite" (emulator pauses while the model thinks). Frontier models collapse from 1.6% completion paused to 0.48% real-time.
*Relevance:* the cleanest demonstration of our central phenomenon — the unpausable clock makes latency a first-class metric. Borrow the paused-vs-live ablation to separate "cannot reason" from "cannot reason fast enough."

**★ AgileThinker / Real-Time Reasoning Gym** — Real-Time Reasoning Agents in Evolving Environments. Wen, Ye, Zhang, Yang, Zhu. *arXiv 2025*. [arXiv 2511.04898](https://arxiv.org/abs/2511.04898). **[N]**
Formalizes "real-time reasoning": hazards and other agents act while the agent is still thinking, forcing an explicit reasoning-depth vs latency tradeoff. Proposes running reactive and planning agents concurrently, evaluated in a Real-Time Reasoning Gym.
*Relevance:* the theoretical backbone of our core bet, in general form. Port its reactive-plus-planning concurrency to SC2 command and adopt its time-pressure-scaling evaluation curves.

**★ Adaptive Command** — Real-Time Policy Adjustment via Language Models in StarCraft II. Ma et al. *arXiv 2025 / DAI 2024*. [arXiv 2508.16580](https://arxiv.org/abs/2508.16580). **[P]**
An LLM strategic advisor over a behavior tree, with a natural-language-plus-speech interface so a human can steer policy in real time; the LLM adjusts the tree rather than controlling units directly. User studies show gains for novices and players with disabilities.
*Relevance:* the closest framing to our thesis (LLM as executor of human intent, not autonomous strategist), already in SC2 with a speech interface. The gap we fill: it offloads real-time control to a hand-built behavior tree and does not quantify or optimize the LLM's own latency/VRAM budget.

**CombatVLA** — An Efficient Vision-Language-Action Model for Combat Tasks in 3D Action RPGs. Chen, Bu, Wang et al. *ICCV 2025*. [arXiv 2503.09527](https://arxiv.org/abs/2503.09527). **[N]**
A 3B VLA trained on video-action pairs as "action-of-thought" sequences for second-level combat, with a truncated-reasoning inference strategy for a claimed 50x speedup at above-human success.
*Relevance:* a concrete recipe for the efficiency half of the bet (shrink the model, truncate the reasoning trace), and a VLA analogue of the small-model DOOM result. Borrow truncated action-of-thought as a latency lever.

**DPT-Agent** — Dual Process Theory for Real-time Simultaneous Human-AI Collaboration. Zhang, Wang, Wen et al. *ACL 2025 (Main)*. [arXiv 2502.11882](https://arxiv.org/abs/2502.11882). **[N]**
Splits the agent into System 1 (FSM plus code-as-policy, fast) and System 2 (asynchronous LLM reflection that infers human intent), so quick responses and slow deliberation run on separate tracks, for simultaneous (not turn-based) collaboration.
*Relevance:* directly addresses our twin requirements (real-time response plus acting on inferred intent) via an async fast/slow split we could adopt so a command is honored immediately while heavier reasoning catches up.

**PORTAL** — Scalable Tactical Agents via Language-Guided Policy Generation. Xu et al. *2025*. [PDF](https://zhongwen.one/pdfs/PORTAL.pdf). **[N]** *(venue unconfirmed)*
The LLM is the architect, not the per-frame actor: it generates behavior trees in a DSL that then run cheaply at game speed, sidestepping the inference-latency wall across thousands of 3D games.
*Relevance:* the main architectural alternative to putting an LLM in the real-time loop — compile intent into a fast policy offline, then run under budget. A useful contrast/fallback to direct LLM command; no live natural-language commands during play.

*Also relevant (verified):* TextStarCraft II (NeurIPS 2024, [2312.11865](https://arxiv.org/abs/2312.11865)) **[P]**; LLM-PySC2 (NeurIPS 2025, [2411.05348](https://arxiv.org/abs/2411.05348)) **[P]**; the ACM Computing Surveys survey of LLM game agents (CSUR 2026, [2404.02039](https://arxiv.org/abs/2404.02039)) **[P]**; the 1.3M-parameter real-time DOOM model ([2604.07385](https://arxiv.org/abs/2604.07385)) **[P]**; and, for a small-model-for-SC2 thread, Hierarchical Expert Prompt ([2502.11122](https://arxiv.org/abs/2502.11122)) and SC-Phi2 ([2409.18989](https://arxiv.org/abs/2409.18989)).

## 2. Efficient LLM inference under latency and memory budgets

**★ Speculative Actions** — A Lossless Framework for Faster Agentic Systems. Ye, Ahuja, Liargkovas, Lu, Kaffes, Peng. *arXiv 2025*. [arXiv 2510.04371](https://arxiv.org/abs/2510.04371). **[N]**
Speculative decoding lifted from tokens to whole actions: a small/fast model predicts likely next actions and executes them in parallel, committing only when the slow target model's verification agrees. Up to ~20% end-to-end latency reduction, and evaluated in a gaming domain.
*Relevance:* a directly transferable, lossless latency mechanism, already tested closed-loop rather than on perplexity. Adopt the small-speculator / large-verifier structure for action issuance under the game clock.

**★ Pitfalls of KV Cache Compression** — Chen, Geh, Grover, Van den Broeck, Israel. *ACL 2026*. [arXiv 2510.00231](https://arxiv.org/abs/2510.00231). **[N]**
Evaluates five eviction methods under multi-instruction prompting and shows specific instructions degrade much faster under compression — effectively silently dropped — with system-prompt leakage as a case study.
*Relevance:* the strongest existing evidence for our premise that eviction "loses the wrong memory." It shows silent instruction-dropping in a static text setting; our contribution is to show the same failure is match-losing when the dropped memory mattered minutes later.

**RRARA** — LLM-Enhanced Rapid-Reflex Async-Reflect Agent for Real-Time Decision-Making. Zheng, Mao, Zhang, Cai. *CVPR 2025 Embodied AI Workshop*. [arXiv 2506.07223](https://arxiv.org/abs/2506.07223). **[N]**
Couples a rule-based reflex agent (immediate action) with an asynchronous LLM "reflector" that refines decisions in the background, and a Time Conversion Mechanism that translates inference delay into equivalent simulation frames.
*Relevance:* an embodiment of "latency must be paid against a live clock"; its frames-as-cost metric is essentially what our scoring needs. We push the LLM itself into the loop and score by win rate rather than using a rule-based fallback.

**SideQuest** — Model-Driven KV Cache Management for Long-Horizon Agentic Reasoning. Kariyappa, Suh. *arXiv 2026*. [arXiv 2602.22603](https://arxiv.org/abs/2602.22603). **[N]**
Uses the LLM itself to decide which cached tokens are still useful (rather than attention-score heuristics) for long-running agentic tasks; cuts peak token usage up to 65% with near-zero task-failure rates where heuristics collapse.
*Relevance:* demonstrates that eviction quality is best judged by task success in a long-horizon loop, and that heuristic eviction fails there — both central to our bet. Differs in that our context is a streaming game state, not retrieved documents.

**DefensiveKV** — Taming the Fragility of KV Cache Eviction. Feng, Guo, Lv, Zhou, Xie. *arXiv 2025*. [arXiv 2510.13334](https://arxiv.org/abs/2510.13334). **[N]**
Argues the stability assumption behind eviction (important entries stay important) is fragile and mean-aggregation scoring fails in worst cases; proposes risk-aware aggregation, cutting quality loss 2.3–4.3x at 20% cache budget.
*Relevance:* gives the mechanism (non-stationary token importance) behind match-losing eviction, plus a strong recent baseline to benchmark inside the live loop.

**Hold Onto That Thought** — Assessing KV Cache Compression on Reasoning. Liu et al. *arXiv 2025*. [arXiv 2512.12008](https://arxiv.org/abs/2512.12008). **[N]**
Benchmarks KV compression on long-reasoning tasks: no single strategy dominates for non-reasoning models, heavy-hitter tracking wins for reasoning traces, and low cache budgets can lengthen traces (raising total cost).
*Relevance:* reinforces that static-benchmark behaviour does not transfer to long-horizon generation, and the "small cache → longer outputs → higher cost" effect is exactly what a live-clock budget exposes. Useful baseline-selection guidance.

*Also relevant (verified, foundational, [P]):* OBCache (ICML 2026, [2510.07651](https://arxiv.org/abs/2510.07651), Diao co-author — our principled eviction baseline to carry into closed-loop scoring); H2O ([2306.14048](https://arxiv.org/abs/2306.14048)); StreamingLLM (ICLR 2024, [2309.17453](https://arxiv.org/abs/2309.17453)); SnapKV ([2404.14469](https://arxiv.org/abs/2404.14469), commonly cited as NeurIPS 2024 — see flag).

## 3. Vision-language-action models and language command interfaces

**★ π0 (pi-zero)** — A Vision-Language-Action Flow Model for General Robot Control. Physical Intelligence (Black, Brown, Darpinian et al.). *arXiv 2024*. [arXiv 2410.24164](https://arxiv.org/abs/2410.24164). **[P]**
A pretrained VLM backbone feeding a separate "action expert" that emits continuous actions via flow matching at up to 50 Hz — the flow head is what enables high-frequency control instead of slow autoregressive decoding.
*Relevance:* the canonical reference for our slow-strategic-brain / fast-executor split. Borrow the structure (heavy VLM reasoning feeding a lightweight high-rate action module) and adapt the fast head to emit in-game actions.

**Fast-in-Slow (FiS-VLA)** — A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning. Chen, Liu, Gu et al. *arXiv 2025*. [arXiv 2506.01953](https://arxiv.org/abs/2506.01953). **[N]**
A dual-system VLA where slow reasoning (System 2, low-frequency) and fast execution (System 1, ~117 Hz) share parameters in one model, via dual-aware co-training (diffusion plus autoregressive objectives).
*Relevance:* sharpens the brain/executor design space — the strongest recent argument that the slow and fast paths can share a backbone, an alternative to running two separate models for commander vs executors.

**OpenVLA** — An Open-Source Vision-Language-Action Model. Kim, Pertsch, Karamcheti et al. *arXiv 2024*. [arXiv 2406.09246](https://arxiv.org/abs/2406.09246). **[N]**
A 7B open VLA emitting actions as discrete text tokens autoregressively; beats the closed 55B RT-2-X by 16.5% with 7x fewer parameters, fully open and PEFT-finetunable.
*Relevance:* the practical, reproducible VLA baseline if we prototype a single-model "tokens-as-actions" executor before committing to a separate fast head. (Lineage anchor: RT-2, CoRL 2023, [2307.15818](https://arxiv.org/abs/2307.15818), origin of "actions as text tokens.")

**★ NL → StarCraft II grounding** — Grounding Natural Language Commands to StarCraft II Game States for Narration-Guided RL. Waytowich, Barton, Lawhern, Stump, Warnell. *SPIE 2019*. [arXiv 1906.02671](https://arxiv.org/abs/1906.02671). **[N]**
Learns a mutual-embedding network mapping natural-language command sequences into the same space as SC2 game states, so human narration can shape RL rewards in a complex RTS.
*Relevance:* the most direct peer-reviewed precedent for commanding RTS agents by natural language. We differ by using an LLM to execute commands as actions in real time rather than only grounding them into a reward — the "prior attempt, narrower scope" citation. (Tom Clancy's EndWar, 2008, is the design precedent but has no academic paper.) **[P]** for EndWar.

**CALVIN** — A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Manipulation. Mees, Hermann, Rosete-Beas, Burgard. *IEEE RA-L 2022*. [arXiv 2112.03227](https://arxiv.org/abs/2112.03227). **[N]**
A simulated benchmark where one agent executes chains of free-form human instructions from onboard sensors, evaluated zero-shot on novel instructions/environments; stresses long-horizon sequencing and unconstrained language.
*Relevance:* a methodological template for evaluating "a person issues language, the agent executes over a long horizon." Our benchmark (chained real-time commands scored by success/win rate) can mirror its sequential-instruction protocol in a game.

## 4. Game-state representation and world models

**★ Graph Tokenization** — Graph Tokenization for Bridging Graphs and Transformers. Guo, **Diao**, Yang, Shi. *ICLR 2026*. [arXiv 2603.11099](https://arxiv.org/abs/2603.11099) · [OpenReview](https://openreview.net/forum?id=jCctxI1BGF). **[P]**
Converts labelled graphs into discrete token sequences via reversible serialization plus BPE, where serialization is guided by global substructure statistics so frequent substructures merge into tokens; off-the-shelf Transformers then consume graphs directly, beating GNNs on 14 benchmarks.
*Relevance:* the anchor and Diao's own work. Game state is a typed entity graph, so this "serialize structure, learn a discrete vocabulary over recurring substructures" recipe is the most direct template for our game-state tokenizer.

**★ IRIS / Δ-IRIS** — Transformers are Sample-Efficient World Models (*ICLR 2023*, [2209.00588](https://arxiv.org/abs/2209.00588)); Efficient World Models with Context-Aware Tokenization (Δ-IRIS, *ICML 2024*, [2406.19320](https://arxiv.org/abs/2406.19320)). Micheli, Alonso, Fleuret. **[N]**
IRIS learns a world model as a discrete autoencoder (observation → tokens) plus an autoregressive Transformer over those tokens; Δ-IRIS makes tokenization context-aware by encoding deltas between timesteps, cutting tokens-per-step substantially at SOTA performance.
*Relevance:* the tightest fit to our thesis — it unifies a learned tokenizer and a Transformer world model with the explicit goal of fewer tokens per decision at equal performance. Δ-IRIS's delta-tokenization is a strong design candidate for compressing slowly-changing game state.

**VQ-VAE** — Neural Discrete Representation Learning. van den Oord, Vinyals, Kavukcuoglu. *NeurIPS 2017*. [arXiv 1711.00937](https://arxiv.org/abs/1711.00937). **[N]**
Introduces vector-quantized VAEs: a learned codebook yields compact discrete latents for images, video, and speech that an autoregressive model can predict.
*Relevance:* the foundational method for learning a compact discrete codebook from a non-text modality — the technique most game-state and world-model tokenizers (including IRIS) build on.

**★ WHAM / WHAMM** — World and Human Action Models towards gameplay ideation. Microsoft Research and Ninja Theory. *Nature 2025*. [Nature](https://www.nature.com/articles/s41586-025-08600-3) · [WHAMM real-time](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/). **[P]**
"Muse," the first World and Human Action Model, jointly generates game visuals and controller actions, producing consistent, editable gameplay sequences; the WHAMM variant models interactive environments in real time.
*Relevance:* the flagship game world model and the one that explicitly couples world and human action — the pairing we need (commands in, forecast out). The real-time WHAMM strand is directly on-point for the compute-budget framing.

**GameNGen** — Diffusion Models Are Real-Time Game Engines. Valevski, Leviathan, Arar, Fruchter. *ICLR 2025*. [arXiv 2408.14837](https://arxiv.org/abs/2408.14837). **[N]**
A diffusion model conditioned on past frames and user actions simulates DOOM interactively at >20 FPS on a single TPU, tracking game state over long trajectories.
*Relevance:* an action-conditioned, real-time learned simulator — the engine type behind a queryable "what-if" forecaster. We would borrow the action-conditioning plus real-time-budget framing; it is pixel-space/single-agent, whereas we want structured-state, multi-agent forecasting.

*Also relevant (verified):* DreamerV3 (Nature 2025, [2301.04104](https://arxiv.org/abs/2301.04104)) — the canonical RL world-model baseline; Genie 2 (DeepMind, 2024, [blog](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)) — large-scale foundation world model, blog only.

## 5. Crowd and real-time motion generation (the embodiment project)

**★ CrowdMoGen** — Zero-Shot Text-Driven Collective Motion Generation. Cao, Guo, Zhang, Xie, Gu, Liu. *IJCV 2025*. [arXiv 2407.06188](https://arxiv.org/abs/2407.06188). **[P]**
A two-stage zero-shot framework: an LLM-driven Crowd Scene Planner (groups individuals, assigns activities/trajectories from text) plus a transformer Collective Motion Generator that respects spatial constraints.
*Relevance:* the closest existing work to "an LLM commands a crowd" — its planner/generator split mirrors our command-to-motion decomposition. Its gap (verified): no real-time / inference-speed claims, which is exactly the budget angle we would fill.

**MotionLCM** — Real-time Controllable Motion Generation via Latent Consistency Model. Dai, Chen, Wang et al. *ECCV 2024*. [arXiv 2404.19759](https://arxiv.org/abs/2404.19759). **[P]**
Distills a motion latent diffusion model into a latent consistency model so text-to-motion runs in one or few steps (~30 ms range) at diffusion-level quality, with a motion ControlNet for spatial control.
*Relevance:* the canonical "diffusion-quality motion at real-time speed on one GPU" result — the baseline our per-character budget is measured against, and the distillation recipe we would build on.

**MotionPCM** — Real-Time Motion Synthesis with Phased Consistency Model. Jiang, Wei, Ni. *arXiv 2025*. [arXiv 2501.19083](https://arxiv.org/abs/2501.19083). **[N]**
Replaces latent-consistency distillation with a phased consistency model to fix quality loss at very low step counts; >30 FPS in a single step with a 38.9% FID improvement over prior real-time SOTA.
*Relevance:* a more recent upgrade to MotionLCM on exactly our metric (single-step real-time plus quality) — the strongest current candidate for the per-character generator under a hard budget.

**MotionStreamer** — Streaming Motion Generation via Diffusion-based Autoregressive Model in Causal Latent Space. Xiao, Lu, Pi et al. *ICCV 2025*. [arXiv 2503.15451](https://arxiv.org/abs/2503.15451). **[P]**
A diffusion-based autoregressive model in a continuous causal latent space, generating motion frame-by-frame from text/motion/hybrid prompts with low latency; supports multi-round, long-horizon composition.
*Relevance:* streaming, next-pose-from-history generation is exactly the inference mode a live commander needs (commands arrive mid-motion); its causal-latent design responds to new orders without regenerating from scratch.

**FloodDiffusion** — Tailored Diffusion Forcing for Streaming Motion Generation. Cai, Wu, Li, Zhou, Zheng, Liu. *arXiv 2025/2026*. [arXiv 2512.03520](https://arxiv.org/abs/2512.03520). **[N]**
Applies diffusion forcing to streaming motion under time-varying text prompts, with per-frame text-conditioning fusion; reports FID 0.057 on HumanML3D at real-time latency.
*Relevance:* the most on-point streaming work — it explicitly handles commands that change over time, the core interaction pattern of World Commander; its per-frame text-injection is directly applicable to mid-stream re-commanding.

**InterGen** — Diffusion-based Multi-human Motion Generation under Complex Interactions. Liang et al. *IJCV 2024*. [arXiv 2304.05684](https://arxiv.org/abs/2304.05684) · [project](https://tr3e.github.io/intergen-page/). **[N]** *(arXiv id to double-check)*
Diffusion model for two-person interactive motion from text via weight-sharing cooperative transformers with mutual attention; introduces the InterHuman dataset.
*Relevance:* the reference for interaction-aware multi-character motion (agents reacting to each other), relevant when commanded crowds must coordinate; its mutual-attention scheme goes beyond CrowdMoGen's independent-agent assumption.

---

## Verification notes

- **AVA / AVACraft** and **PORTAL** were arXiv preprints / an author PDF at search time; treat their venues as unconfirmed.
- **SnapKV** is widely cited as NeurIPS 2024, but the arXiv page does not state the venue; cite as arXiv 2024 unless the proceedings entry is confirmed.
- **InterGen**: title, authors (Liang et al.), IJCV 2024, and the InterHuman dataset are confirmed; the arXiv id 2304.05684 is from the project-page lineage and should be double-checked before citing.
- A candidate on discrete tokenization of tabular data (arXiv 2603.07448) surfaced but its authors/venue were not confirmed, so it is omitted here.
- Several 2026 arXiv ids (e.g. Graph Tokenization 2603.x, SideQuest 2602.x, the DOOM model 2604.x) are recent; they were resolved against their abstract pages during the search but post-date the assistant's training data, so re-confirm before formal citation.
