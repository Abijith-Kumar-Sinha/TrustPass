---
version: 1
slug: "web-index-html"
primary_target: "web/index.html"
related_targets: ["web/app.js","web/style.css"]
---

## Scope

TrustPass web UI (`web/index.html` + `web/app.js` + `web/style.css`, served by `server.py`; static snapshot fallback `web/snapshot.json`). Mode: Persuade. Primary viewing: a 1920x1080 screen recording for the Round-1 demo video; also opened from a GitHub Pages link by judges.

## Audience, job, proof

Q-HACK INDIA judges (IBM/Qiskit engineers, faculty). In seconds they must see: the untrusted compiler's attack fools today's checks, then TrustPass catches it (naive 1/4, TrustPass 4/4). Proof is real pipeline output only, every number tagged with backend, seed and run. Constraints: no invented numbers; honest about the cost of locking and out-of-scope attackers.

## Direction contract

THESIS: TrustPass is a bench instrument you put a circuit on, not a dashboard you read. It refuses the category default (dark sidebar, metric cards, violet glow) and the glow-on-black oscilloscope cliché.

OWN-WORLD: Warm-grey powder-coated chassis owns the whole page with corner screws; one dark slate bezel holds a graticule LCD; silkscreened condensed caps legends; channel colors yellow CH1, cyan CH2, magenta CH3; indicator green and alarm red only on lamps and FAIL/REJECT; backlit rectangular keys; real knobs, lever toggle, round lamps, segment counters.

STORY: Visitor turns SOURCE to a compiler, sees what the compiler saw (key symbols only), watches three channels judge the returned circuit, and the REJECT lamp light; the lamp matrix and 1/4 vs 4/4 counters carry attack-then-defend.

FIRST VIEWPORT: Approved comp-4. Wordmark + model line + provenance top; five joined pipeline keys full width; graticule display left 52% (locked circuit traces); control column 20% (SOURCE knob, CIRCUIT knob, BACKEND lever); detection matrix 28% (5x3 lamps, two counters); bottom band CH1/CH2/CH3 readouts, REJECT lamp, reason caption.

FORM: Lab bench analyzer front panel, candidate 4 of 7, seed e259c9ec. Raises: pipeline chase light (drum machine), run ledger (minihompy), URL-addressed state (teletext), provenance tags (bazaar), lining tabular numerals (accretion). Signature interaction: turning SOURCE re-acquires: chase light runs LOCK to SCORE, traces sweep, channels and lamps settle.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Approved comp

`.impeccable/mocks/comp-4.png` (combination of comp-1 + comp-2 lamp matrix, approved by the user 2026-10-07).

## Unresolved

Below-the-fold sections (evidence histograms, "what came back" view, run ledger, honest limits) inherit the system; the comp does not show them.
