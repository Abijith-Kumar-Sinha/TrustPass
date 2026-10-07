# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Hand-built single page (HTML/CSS/JS, no framework) plus a tiny Python API that runs the real TrustPass pipeline (`pipeline.py`). A hosted snapshot (GitHub Pages) serves results precomputed by the same pipeline, clearly labelled as a snapshot; the live version runs locally for the demo video and the in-person finale. (User decision, 2026-10-07.)

## Users

- Hackathon judges at Q-HACK INDIA 2026 (IBM Qiskit Fall Fest, Ramaiah Institute of Technology; likely IBM/Qiskit engineers and faculty). They watch a demo video in Round 1 and a live demo at the finale, and may open the hosted link. They know quantum computing well; they need to grasp the threat and the result in seconds.
- The team (3rd-sem CSE/cyber students) presenting it live.

## Product Purpose

TrustPass is zero-trust quantum compilation. A circuit is locked (every single-qubit angle becomes a key symbol, decoy CX pairs pad every qubit pair to the same count), compiled by an untrusted third party, unlocked locally, then verified: formal equivalence (MQT QCEC) plus an output-map check catches Trojans; a fidelity audit (estimated success probability from device calibration vs a free honest compile) catches sabotage that is logically equivalent. Success = judges see that today's practice (eyeballing a histogram) catches 1 of 4 attacks while TrustPass catches all 4.

## Positioning

To our knowledge, the only pipeline that combines circuit locking, formal functional verification and a fidelity-sabotage audit, and that red-teamed itself (15 findings across two rounds and a final review, each verified and fixed, measured or documented).

## Operating Context

- Demo flow: pick a victim circuit (Grover marked item, QAOA graph + angles, VQE weights), pick an untrusted compiler (honest, Trojan visible / hidden in noise / dormant, saboteur), see what leaves the machine, the verdict, the evidence, and a 5×3 detection matrix.
- Backends are simulated IBM devices with real calibration data (FakeBrisbane 127q, FakeTorino 133q).
- Real IBM hardware run exists only via `demo.py --ibm` with the user's own saved token.

## Capabilities and Constraints

- Pipeline runs in ~1–15 s per run; detection matrix ~1–2 s.
- Known limits that must be stated, not hidden: locking adds 2-qubit gates (Grover 39 → 45); QAOA's graph is hidden statistically, not exactly; lone-CX skeletons can be peeled; circuits with odd per-pair CX gaps are refused; scheduled compiles with delays are rejected (fail-closed); attackers who see execution results are out of scope.
- Name "TrustPass" is the working name used throughout.

## Evidence on Hand

- Real outputs from `pipeline.run` / `detection_matrix` (FakeBrisbane, seed 7): saboteur ESP 0.385 vs 0.712 baseline; noisy-sim fidelity 0.35 vs 0.72; Grover locked view identical across all 8 marked items.
- Red-team findings and fixes (two rounds) in README / Obsidian.
- No users, customers, testimonials or benchmarks exist; never fabricate them.

## Product Principles

- Show, don't claim: every number on screen comes from a real pipeline run.
- Attack, then defend: the story is the attack succeeding against naive checks, then being caught.
- Honest about cost and limits: the cost of locking and the out-of-scope attacker are part of the story.
- Seconds to understand: a judge should grasp threat, verdict and why within one screen.
