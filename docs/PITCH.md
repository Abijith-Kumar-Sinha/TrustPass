# TrustPass: Round 1 pitch (slide text)

Slide-by-slide text for the organisers' Canva template, followed by a 90-second demo-video script. 12 slides.

**Where the numbers come from.** Measured on 2026-10-06 with `demo.py` and the repo code (updated 2026-10-07 after the round-2 fixes), on simulated IBM devices: FakeBrisbane (127-qubit Eagle, ECR gates) and FakeTorino (133-qubit Heron, CZ gates), transpiler seed 7. The lock draws fresh OS randomness on every run, so numbers move a little from run to run. Ranges cover 4 runs per demo on FakeBrisbane. Quote the ranges as they are; do not round them in our favour. The web UI's snapshot (`web/snapshot.json`) is one more set of real runs; its numbers sit inside these ranges.

**Check before presenting.** Two facts on slides 2 and 11 are general knowledge, not from our README or our runs: the National Quantum Mission budget (₹6,003.65 crore, 2023-24 to 2030-31) and QpiAI-Indus being a 25-qubit machine reached through QpiAI's cloud stack. Check both against an official source, or drop them.

---

## Slide 1: Title

**TrustPass: zero-trust compilation for quantum circuits**

- Let a third party compile your quantum circuit without showing it your gate angles, and check what comes back before it runs.
- Q-HACK INDIA 2026 · Quantum Security & Cryptography track
- [Team name] · [College]

*Speaker note:* Compiling a quantum circuit now often means sending it to someone else's code. TrustPass lets you do that without trusting them.

---

## Slide 2: The problem

**Your compiler sees everything, and it is not always yours**

- The compile step is moving to other parties: partner circuit functions in IBM's Qiskit Functions Catalog, third-party transpiler plugins, and cloud-hosted compiler stacks such as QpiAI's for India's 25-qubit QpiAI-Indus.
- **Steal:** the circuit is the IP: a Grover oracle's marked item, a QAOA graph with its trained angles, a VQE ansatz with its trained weights.
- **Trojan:** add a gate that changes the answer: obvious, small enough to hide in hardware noise, or dormant until the circuit gets a non-zero input.
- **Sabotage:** return a circuit that really is equivalent, but parked on the worst qubits, so every equivalence checker says "fine" and the results just get worse.
- Today's check (run on |0…0⟩ and eyeball the histogram) misses 3 of our 4 attacks (2 to 3 on VQE). And the National Quantum Mission (₹6,003.65 crore, to 2031) is putting Indian users on shared cloud compile stacks.

*Speaker note:* Three attacks: steal it, change it, or quietly make it worse. The usual sanity check catches only the obvious one.

---

## Slide 3: Research gaps

**What exists, and what is missing**

| Work | Gap |
|------|-----|
| E-LoQ, Liu, John, Wang, IEEE HOST 2025 (arXiv:2412.17101) | Locking is judged on concealment only; nobody checks the circuit that comes back. |
| CLOAQ, Langford et al., ISCAS 2026 (arXiv:2602.23569) | Obfuscation was evaluated only with all-\|0⟩ inputs. |
| Zhang & Liu 2025 (arXiv:2511.04842) | A few input/output pairs break split compilation; new schemes need this evaluation. |
| Rahman, Haghparast, Mikkonen 2026 (arXiv:2608.05831) | Security metrics (TVD, DFC) are ad hoc and not comparable across papers. |
| John, Golla, Wang 2025 (arXiv:2502.08880) | Trojans can stay dormant until a specific input triggers them. |
| Dual-mode Trojan detection, Springer 2025 (doi:10.1007/978-981-95-4791-3_6) | Detection is a classifier on unitary-matrix features (91.6% accuracy), exponential in qubits. |
| Localized noise fingerprints, ACM 2025 (doi:10.1145/3733825.3765283) | Detecting fidelity tampering is new, and separate from locking. |

To our knowledge, no tool combines locking, formal verification and a fidelity audit in one pipeline.

*Speaker note:* Our response, row by row: verify what comes back; test on random inputs and prove for all inputs; oracle-guided attacks are Round 2; one fixed scorecard; dormant Trojan is one of our attacks; a formal proof instead of a classifier; the fidelity audit is in the same pipeline.

---

## Slide 4: Our solution

**Lock → untrusted compile → unlock → verify → score**

*Diagram:* three zones, left to right. **Your machine (trusted, green):** "Circuit" → "Lock" (a key icon stays here). Arrow labelled "locked circuit: angles are symbols" → **Third-party compiler (untrusted, red):** "Compile". Arrow labelled "compiled locked circuit" back to the trusted zone: "Unlock (bind key)" → "Verify: equivalence proof + fidelity audit" → "Score + verdict". Arrow labelled "ACCEPT only" → **Hardware provider (grey):** "Run".

- **Lock:** every gate angle becomes a symbol; the values (the key) never leave your machine.
- **Verify integrity:** MQT QCEC proves the returned circuit does the same thing as yours on every input, and we check every measured output still lands on the right qubit.
- **Verify quality:** a fidelity audit compares the returned circuit's estimated success probability (ESP, from the device's calibration data) with a free local compile, and flags anything below 0.90 of it.
- **One verdict:** ACCEPT only if both checks pass, plus a confidentiality / integrity / quality scorecard.

*Speaker note:* Threat model: the compiler is untrusted, your machine is trusted, and you submit the final circuit to the hardware provider yourself, so the compiler never sees your results.

---

## Slide 5: How the lock works

**Hide the angles, flatten the skeleton**

- Each run of single-qubit gates becomes one block, rz(k1) · sx · rz(k2) · sx · rz(k3). The k's are symbols; their values are the key. Grover: 153 key angles, 0 numeric angles left.
- Only CX gates stay visible, so we add decoy CX pairs (they cancel out) until every qubit pair has the same CX count, and we lock them like real gates. Decoy pairs needed: Grover 0, QAOA 1, VQE 3.
- Every CX gets a random direction. The H gates that flip it are folded into the keyed blocks, so this costs nothing.
- Nothing else leaves: no circuit name, no metadata, global phase set to 0, decoy positions from OS randomness.
- Unlock = put the key values into the compiled circuit. Compilers already handle symbolic parameters, so an honest compiler works unchanged.

*Speaker note:* The compiler gets a valid circuit it can optimise and route, but every angle is a blank and every pair of qubits looks equally connected.

---

## Slide 6: The detection matrix

**No single check catches everything. Together they catch all four attacks.**

| Untrusted compiler | Naive \|0⟩ test | QCEC equivalence | Fidelity audit | Verdict |
|---|---|---|---|---|
| Honest | pass | pass | pass | **ACCEPT** |
| Trojan, visible (X before measurement) | CAUGHT | CAUGHT | pass | **REJECT** |
| Trojan, hidden in noise (rz 0.35 mid-circuit) | pass* | CAUGHT | pass | **REJECT** |
| Trojan, dormant (CX, no-op on \|0…0⟩) | pass | CAUGHT | pass | **REJECT** |
| Saboteur (worst qubits + self-cancelling gates) | pass | pass | CAUGHT | **REJECT** |

- Same pattern on all three demos (Grover, QAOA, VQE), on both FakeBrisbane (ECR) and FakeTorino (CZ).
- 20 runs, each with a fresh random lock: honest accepted 20/20, attacks rejected 80/80.
- QCEC passes the saboteur, because it really is equivalent. Only the fidelity audit catches it.
- One QCEC check took under 0.5 s on every circuit we ran.

\* On VQE the naive test's distance is 0.09-0.11 against its 0.10 tolerance, so it catches this Trojan in some runs.

*Speaker note:* Left column is what people do today; it catches only the obvious Trojan. The proof catches every Trojan; the audit catches the one attack that is equivalent by design.

---

## Slide 7: Saboteur evidence

**Equivalent, and quietly worse**

- The saboteur compiles onto a connected group of qubits at the device's 90th error percentile, skips broken ones so the output still looks plausible, and adds 2 self-cancelling two-qubit gate pairs. The naive test passes and QCEC says "equivalent".

  | FakeBrisbane | ESP: saboteur vs honest (ratio) | Noisy-sim fidelity: saboteur vs honest |
  |---|---|---|
  | Grover | 0.38-0.39 vs 0.71 (0.54-0.55) | 0.34-0.35 vs 0.71-0.72 |
  | QAOA | 0.60-0.61 vs 0.82-0.83 (0.73-0.74) | 0.81-0.82 vs 0.90-0.93 |
  | VQE | 0.53-0.56 vs 0.81-0.83 (0.65-0.69) | 0.81-0.82 vs 0.92-0.94 |

- Its qubits have 6.0% readout error (Grover) and 5.1% (QAOA, VQE), against a device median of 2.0%.
- The audit flags any ratio below 0.90. The noisy simulation agrees on all three demos, but it is evidence only; the verdict uses ESP from calibration data.

*Speaker note:* ESP is the product of (1 − error) over every gate and measurement. Our stand-in honest compiler is the same call as the local baseline, so honest scores exactly 1.0 by construction; a better third-party compiler would score above 1.

---

## Slide 8: Confidentiality, and what it costs

**What the compiler can still learn, and what locking costs**

- **What the compiler sees:** no gate angles, no name or metadata, every qubit pair with the same CX count.
- **The view test (the check that can fail):** lock the same circuit with every possible secret, holding the lock's randomness fixed. Grover: 8 marked items give 8 different circuits before locking and 1 identical compiler view after. VQE: 8 weight sets, 1 view. QAOA angles: 1 view. The test correctly fails for QAOA graphs, whose structure is the secret.
- **QAOA graph:** hidden statistically. Decoy pairs land at uniform positions and commuting `rzz` gates are shuffled, so the order of qubit-pair blocks is a uniform permutation: over 800 locks, pair positions were uniform (p = 0.62-0.93) and no different between graphs (p = 0.69). Earlier versions leaked 35-65% (round 1) and 40-45% to an exact Bayes attacker (round 2); chance is 1.6%.
- **Key guessing is only a sanity check:** a wrong key's output is no closer to the truth than a random state (indistinguishability 0.98-1.00), but that stays true for any lock, so we do not present it as evidence of secrecy.
- **Cost** (honest compile on FakeBrisbane, plain → locked):

  | | Two-qubit gates | Depth |
  |---|---|---|
  | Grover | 39 → 45 | 174 → 371-387 |
  | QAOA | 16 → 18-21 | 85 → 128-155 |
  | VQE | 6 → 18-21 | 30 → 131-158 |

*Speaker note:* We are honest about both sides. Grover's cost dropped from 53 to 45 two-qubit gates after the fixes; VQE pays most because its 6 qubit pairs all need padding to the same count. If a judge asks how we know the compiler learns nothing: the view test, and two rounds of attackers trying to read the secret off the locked circuit.

---

## Slide 9: We red-teamed ourselves

**Two rounds of attackers on our own prototype: 14 findings, each fixed or documented**

| What we broke | Fix |
|---|---|
| The lock shipped the circuit's name and metadata, which contained the secret in plain text | Both stripped |
| Global phase leaked 1 bit of the Grover secret (its parity) | Phase sent as 0 (it is unobservable anyway) |
| Decoys were seeded from the public seed, so they could be replayed (100% QAOA graph recovery) | The lock always uses OS randomness |
| Counting CX-block-CX "sandwiches" recovered the QAOA graph (35-65%, chance 1.6%) | Every qubit pair padded to the same CX count, random CX directions (now 3.3-3.8%) |
| A dropped or re-routed measurement passed QCEC (unmeasured qubits are "don't care") | Check the output-to-qubit map before QCEC |
| A single delay or reset crashed QCEC (denial of service) | Fail closed: anything unverifiable is REJECT |
| QCEC sometimes gave up with "no information" at random | Unstable checker turned off; honest passes 5/5 in a row in tests |
| Round 2: QCEC occasionally hung forever under load | Sequential checking with a 30 s timeout: slow means REJECT, never a hang |
| Round 2: decoy positions still leaked the QAOA graph to an exact Bayes attacker (40-45%) | Decoys at uniform boundaries, commuting gates shuffled: pair order now uniform |
| Round 2: an odd CX gap could not be padded and leaked a Bernstein-Vazirani secret | The lock refuses such circuits instead of leaking |
| Round 2: our key-guessing metric could not detect leaks at all | Replaced as evidence by the view test, which can fail |

- 9 automated tests cover these; all pass in about 10 s. Every finding was re-run by a separate agent before we acted on it; three smaller ones are documented as limits (lone-CX skeletons can be peeled, padding reveals the busiest pair's count, scheduled compiles are rejected).

*Speaker note:* We attacked our own tool the way a malicious compiler would. Each line is an attack that worked against an earlier version and the change that stopped it.

---

## Slide 10: Limits and Round-2 roadmap

**What is not done yet, and the plan for each**

- **Structural attackers tested; I/O attackers out of scope.** An attacker who sees input/output pairs of the unlocked circuit is out of scope (Grover's output is its secret). → **Oracle-guided attack suite** (Zhang & Liu style, plus angle fitting) as the real confidentiality measure.
- **Wrapped around our own stand-in compilers.** → **Package as a Qiskit transpiler plugin** that wraps lock, unlock and verify around any third-party plugin or Qiskit Function call.
- **Simulated devices only; ESP trusts calibration data** (ignores crosstalk and idle time). → **Real IBM hardware runs** with `demo.py --ibm`: compare ESP's prediction with measured fidelity for honest vs sabotaged compiles.
- **Locking costs gates; QAOA graphs are hidden statistically, and lone-CX skeletons can be peeled.** → **Routing-aware, commutation-aware decoys** placed on real coupling-map edges, plus a 3-CX identity gadget for odd gaps.
- **Fail-closed rejects honest scheduled compiles** (dynamical decoupling adds delays QCEC cannot read). → **Delay-aware audit** that strips and checks idle periods separately.

*Speaker note:* TrustPass assumes the compiler is not also the party that runs the circuit; if one party does both, we still check integrity and fidelity but cannot keep the circuit secret.

---

## Slide 11: Impact

**Who uses this**

- **Pharma and materials teams:** a VQE ansatz with trained weights is months of chemistry work. Send it to a partner's compile or error-suppression service without handing it over.
- **Finance teams:** a QAOA instance (the graph and its tuned angles) stays private, and a Trojan that quietly changes the answer gets rejected before it runs.
- **India's quantum cloud:** machines built under the National Quantum Mission, such as QpiAI-Indus, will be reached through shared compile stacks. TrustPass lets users from any lab or company use them without trusting the stack.
- **Compiler vendors:** an equivalence proof plus an ESP ratio of at least 0.90 is a receipt a customer can check, showing that the compile was honest.
- **Runs today on a laptop:** Python on Qiskit and the open-source MQT QCEC; a full run with evidence takes about 6 s and the five-compiler detection matrix 1-2 s.

*Speaker note:* Anyone who sends a circuit they care about to code they did not write.

---

## Slide 12: Team

**Team [name]**

| Name | Role |
|------|------|
| [Name] | [Role] |
| [Name] | [Role] |
| [Name] | [Role] |

- GitHub: [repo URL]

*Speaker note:* [One line per person on what they built.]

---

## 90-second demo video script

Setup before recording: `python server.py`, open http://localhost:8600 in Chrome, full screen (F11) at 1920×1080, so the panel fills the frame. The page opens on Grover / Saboteur / FakeBrisbane. Each turn of a knob runs the real pipeline live (about 6 s: the chase light runs through LOCK → SCORE while it measures); trim those waits in the edit if you need the time. For a run with no waiting at all, serve the static snapshot instead (`python -m http.server` in the repo, then open `index.html`): same real pipeline, precomputed. Exact live numbers vary a little run to run because the lock is random; say "about".

| Time | Screen / action | Voice-over |
|---|---|---|
| 0:00-0:08 | The whole front panel, red REJECT lamp lit. | "Compiling a quantum circuit often means sending it to someone else's code. TrustPass lets you do that without trusting them." |
| 0:08-0:20 | Point at the display header "What the compiler sees: 153 key angles, 0 numeric". Scroll to Inspect, press YOUR CIRCUIT, then WHAT THE COMPILER SEES; point at "8 different secrets → 1 identical view". | "This Grover circuit's secret is the marked item. Before it leaves the laptop we lock it: every angle becomes a key symbol that stays here. Lock all eight possible secrets and the compiler sees the exact same circuit every time." |
| 0:20-0:30 | Scroll back up, turn SOURCE to HONEST. Chase light, three PASS, green ACCEPT. | "An honest compile comes back, we unlock it locally, prove it is equivalent, and check it is as good as a free compile. Accept." |
| 0:30-0:42 | Turn SOURCE to TROJAN DORMANT. CH1 still PASS, CH2 FAIL, red REJECT. | "Now a Trojan that does nothing on the all-zero input. The histogram test everyone uses passes it. The equivalence proof covers every input and rejects it." |
| 0:42-0:58 | Turn SOURCE to SABOTEUR. CH1 PASS, CH2 PASS, CH3 FAIL (ESP about 0.39 vs 0.71); read the caption under the lamp. Scroll to the CH3 histogram: the right answer 101 drops from about 0.66 on an honest compile to about 0.31. | "The hardest one: a saboteur that really is equivalent, so the proof passes, but it parked the circuit on bad qubits. Its success probability is about half an honest compile's, and the audit rejects it." |
| 0:58-1:10 | Detection matrix: point at the lamps and the counters NAIVE 1/4, TRUSTPASS 4/4. Flip BACKEND to TORINO and CIRCUIT to QAOA; the pattern holds. | "All five compilers at once. Today's check catches one attack in four. TrustPass catches all four, on all three circuits and two IBM device models." |
| 1:10-1:22 | Scroll to the rating plate: point at "Red-teamed" and "Out of scope". | "We attacked our own tool in two rounds and fixed or documented all fourteen findings, and we say plainly what it does not cover." |
| 1:22-1:30 | Back to the top of the panel, or the GitHub page. | "Next: oracle-guided attacks, a Qiskit transpiler plugin, and real IBM hardware runs. TrustPass: compile anywhere, verify before you run." |
