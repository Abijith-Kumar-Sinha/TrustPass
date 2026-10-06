---
name: TrustPass
description: TP-1 zero-trust quantum compilation analyzer, built as a bench instrument front panel.
colors:
  chassis: "#cccac7"
  panel-face: "#d6d5d2"
  rule: "#9f9d98"
  ink: "#1d2126"
  bezel: "#3b4044"
  screen: "#1a2125"
  seg-bg: "#171d21"
  grid: "#263038"
  grid-major: "#34404a"
  screen-text: "#8fd2ea"
  ch1: "#f2cf1d"
  ch2: "#42daea"
  ch3: "#d86aa0"
  tab1: "#f2cf1d"
  tab2: "#3fc3e6"
  tab3: "#c4407f"
  key-edge: "#7f7e7a"
  lit: "#f9ce71"
  pass: "#1d8a3b"
  fail: "#c81e1e"
typography:
  display:
    fontFamily: "Kufam, sans-serif"
    fontSize: "calc(45 * var(--u))"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.005em"
  headline:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(24 * var(--u))"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.005em"
  title:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(26 * var(--u))"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.03em"
  body:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(19 * var(--u))"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(16 * var(--u))"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.03em"
  legend:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(14 * var(--u))"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  readout-numeral:
    fontFamily: "Inria Sans, system-ui, sans-serif"
    fontSize: "calc(44 * var(--u))"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.01em"
    fontFeature: "\"lnum\", \"tnum\""
  segment:
    fontFamily: "DSEG7, monospace"
    fontSize: "calc(32 * var(--u))"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.04em"
rounded:
  plate: "calc(3 * var(--u))"
  key: "calc(4 * var(--u))"
  lamp-button: "calc(5 * var(--u))"
  counter: "calc(6 * var(--u))"
  bezel: "calc(10 * var(--u))"
  round: "50%"
spacing:
  xs: "calc(10 * var(--u))"
  sm: "calc(12 * var(--u))"
  md: "calc(16 * var(--u))"
  lg: "calc(24 * var(--u))"
  xl: "calc(28 * var(--u))"
components:
  pipeline-key:
    backgroundColor: "#c7c6c2"
    textColor: "#15181c"
    typography: "{typography.headline}"
    rounded: "{rounded.key}"
    height: "calc(62 * var(--u))"
  pipeline-key-lit:
    backgroundColor: "{colors.lit}"
    textColor: "#2e2203"
  soft-key:
    backgroundColor: "#bab9b5"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.key}"
    padding: "calc(10 * var(--u)) calc(18 * var(--u))"
  soft-key-selected:
    backgroundColor: "{colors.lit}"
  display-screen:
    backgroundColor: "{colors.screen}"
    textColor: "{colors.screen-text}"
    rounded: "{rounded.bezel}"
  channel-readout:
    backgroundColor: "{colors.panel-face}"
    textColor: "{colors.ink}"
    rounded: "{rounded.plate}"
    height: "calc(120 * var(--u))"
  segment-counter:
    backgroundColor: "{colors.seg-bg}"
    textColor: "{colors.ch1}"
    typography: "{typography.segment}"
    rounded: "{rounded.counter}"
    height: "calc(66 * var(--u))"
  rating-plate:
    backgroundColor: "{colors.panel-face}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.plate}"
    padding: "calc(24 * var(--u)) calc(28 * var(--u))"
  ledger-tape:
    backgroundColor: "{colors.seg-bg}"
    textColor: "#cfd6da"
    rounded: "{rounded.key}"
    padding: "calc(12 * var(--u))"
---

# Design System: TrustPass

## Overview

**Creative North Star: "The Bench Analyzer"**

The page is a lab instrument's front panel. You set a circuit on it; you don't read a dashboard. A warm-grey powder-coated chassis (a tiled raster plate over the chassis colour) covers the whole viewport, with screws in the corners. One dark slate bezel holds a graticule screen. Around it sit physical controls: backlit rectangular keys on a rail, raster knobs with silkscreened detent legends, a lever toggle, a matrix of round lamps, and segment counters. Each control works. Turning a knob re-acquires the measurement.

The panel is drawn in comp coordinates. On desktop every length is a multiple of `--u` (panel width / 1536, as container query units), so the approved 16:9 comp holds at any size. Below the panel, bench units use the same chassis, rules, plates and screens to carry the evidence, inspection views, ledger and rating plate. Colour is rationed by function. Channel colours (yellow CH1, cyan CH2, magenta CH3) identify signals. Indicator green and alarm red appear only on lamps, PASS/FAIL readings and the verdict. Amber appears only as backlight.

The world rejects the category default (dark sidebar, metric cards, violet glow) and the glow-on-black oscilloscope cliché. Its depth comes from physical parts lit from above, never from bloom.

**Key Characteristics:**
- Light warm-grey chassis surface, with exactly one family of dark screens set into it.
- Every length in comp units (`calc(n * var(--u))`); there are no loose px or rem values in the panel.
- Silkscreened uppercase legends in Inria Sans; Kufam only on the wordmark; DSEG7 only inside segment counters.
- Raster plates (knobs, lever, lamps, screws, chassis) carry embedded provenance; code draws the keys, bezels, readouts and verdict lamp.
- A single orchestrated acquisition motion, which reduced-motion turns off.

## Colors

The palette is a powder-coat grey instrument with phosphor-coloured signals on a slate screen, and indicator colours kept behind glass.

### Primary
- **Channel Yellow** (ch1): CH1 trace, the CH1 colour tab, the naive counter's segment digits, and the first qubit wire.
- **Phosphor Cyan** (ch2): CH2 trace and the honest-compile series in histograms.
- **Trace Magenta** (ch3): CH3 trace and the returned-circuit series in histograms.

### Secondary
- **Tab Yellow / Tab Cyan / Tab Magenta** (tab1, tab2, tab3): these are printed ink versions of the channel colours, used on the readout tabs where they sit on the light panel face. Tab Magenta takes white tab text. Tab Cyan is also the focus-ring colour.
- **Backlight Amber** (lit): the lit pipeline key (inside a radial gradient), the selected soft-key, the pip of the selected detent or current matrix row, and text selection.

### Tertiary
- **Indicator Green** (pass) and **Alarm Red** (fail): PASS/FAIL readings and good/bad spec values only. The verdict lamp and the raster lamps carry their own illuminated reds and greens inside their gradients and plates.

### Neutral
- **Powder-Coat Chassis** (chassis): the page surface, under the tiled chassis plate. Group-box titles knock out the rule against it.
- **Panel Face** (panel-face): readout plates, spec sheets and the rating plate.
- **Silkscreen Rule** (rule): the matrix group-box border and counter divider.
- **Legend Ink** (ink): all legends and body text on the chassis.
- **Slate Bezel** (bezel): the frame around every screen.
- **Screen Slate** (screen): the display and bench-unit screens.
- **Counter Black** (seg-bg): segment counter wells and the ledger tape.
- **Graticule Minor / Major** (grid, grid-major): screen grid lines, with every fourth line major.
- **Screen Legend** (screen-text): titles and footers printed on the screen glass.
- **Key Edge** (key-edge): soft-key borders.

### Named Rules
**The Lamp-Only Rule.** Green and red mean a measurement result. They appear on lamps, PASS/FAIL, the verdict and good/bad values, and nowhere decorative.

**The Signal Identity Rule.** Each channel colour belongs to one channel everywhere: the trace, the tab, the histogram series and the counter. Never reassign a channel colour to decoration.

## Typography

**Display Font:** Kufam 700 (with sans-serif), used on the wordmark only
**Body Font:** Inria Sans 400/700 (with system-ui, sans-serif)
**Label/Mono Font:** DSEG7 700, used in segment counters only

**Character:** Inria Sans reads as panel silkscreen. Legends are uppercase and tightly tracked, between -0.04em and 0.04em depending on how full the field is. Kufam's squared geometry stamps the maker's name. DSEG7 is the instrument's own readout.

### Hierarchy
- **Display** (700, 45u, 1.3): the TrustPass wordmark, top left.
- **Headline** (700, 24u, uppercase): the model line, pipeline keys, and screen titles.
- **Title** (700, 26u, uppercase, 0.03em): bench-unit headings. The matrix group-box title is 22u.
- **Body** (400, 18-19u, 1.36-1.45): the verdict reason caption and rating-plate prose, with a 75ch maximum.
- **Label** (700, 15.5-17.5u, uppercase, 0.03em): control labels, counter captions, spec terms, readout headers and soft-keys.
- **Legend** (700, 14u, uppercase): knob detent legends.
- **Readout numeral** (400, 44u, lining tabular): channel values. Status words (PASS/FAIL) are 700 at 32u.
- **Segment** (DSEG7 700, 32u): counters, drawn over a 3%-white ghost layer of all-lit segments.

### Named Rules
**The Tabular Numerals Rule.** Every live number (provenance, readouts, specs) uses `lining-nums tabular-nums`, so values don't jitter while the panel re-acquires.

**The One-Face-Per-Job Rule.** Kufam is for the wordmark only and DSEG7 is for counters only. Everything else is Inria Sans.

## Layout

The desktop panel is an absolute-positioned 16:9 front panel inside a container query (`.page` width is min(100vw, 100svh × 16/9)). Modules sit at comp coordinates in units of `--u` = 100cqw / 1536. The first viewport follows the approved comp: wordmark, model line and provenance across the top; five joined pipeline keys at full width; the display at about 52% on the left; the control column at about 20%; the detection matrix at about 28%; and a bottom band of CH1/CH2/CH3 readouts, the verdict lamp and the reason caption.

At 760px and below, `--u` becomes 100cqw / 640 and the modules restack in a single column. The order is head, pipeline (wrapped keys, rail hidden), verdict, reason, display (aspect 806/515), controls, readouts (stacked), then matrix. The lower screws are hidden.

The bench below is a two-column grid. Every current unit spans both columns. Each unit is headed by a 2u ink rule. Unit bodies are a screen plus a 380u spec sheet, which collapses to one column on phones. Spacing runs on 10 / 12 / 16 / 24 / 28u steps.

## Elevation & Depth

The panel is physically layered and lit from above. Raised parts (keys, soft-keys, the verdict housing, readout plates) carry a top inner highlight and a fixed downward drop shadow. Recessed parts (screens, counter wells, the ledger tape) carry inset darkening. Raster parts get their shadow from `filter: drop-shadow` on a wrapper that does not rotate, so the light stays put while a knob or lever turns.

### Shadow Vocabulary
- **Key lift** (`inset 0 0 0 1.5u rgba(255,255,255,.45), inset 0 -4u 0 rgba(0,0,0,.16), 0 3u 4u rgba(0,0,0,.25)`): pipeline keys.
- **Bezel set** (`inset 0 2u 0 rgba(255,255,255,.12), inset 0 0 0 2u #24282b, 0 4u 10u rgba(0,0,0,.35)`): the display bezel.
- **Screen well** (`inset 0 0 30u rgba(0,0,0,.6)`): screen glass vignette, the only zero-offset blur in the system.
- **Counter well** (`inset 0 2u 6u rgba(0,0,0,.6)`): segment counters and the tape (8u blur).
- **Plate rest** (`inset 0 1u 0 rgba(255,255,255,.6), 0 1u 2u rgba(0,0,0,.15)`): readout plates.
- **Knob drop** (`drop-shadow(0 4u 4u rgba(0,0,0,.42))`), **lever drop** (`0 3u 3u .4`), **lamp drop** (`0 1.5u 1.5u .45`): raster parts, applied on wrappers.

### Named Rules
**The Fixed Light Rule.** Shadows always fall downward and never rotate with a part. Put the drop shadow on the non-rotating wrapper.

**The No-Bloom Rule.** Nothing glows outward. Lit things are lit by gradient and highlight inside their own shape. Outward zero-offset blurred glows are not part of this world.

## Shapes

Shapes are small-radiused machined rectangles: plates at 3u, keys/screens/tape at 4u, the verdict at 5u, counters at 6u and bezels at 10u. Knobs, lamps and pips are round. Borders are thin silkscreen or edge lines of 1.5-2u. The matrix is a group box whose title knocks out the top rule. The pipeline is one rail (a 10u bar with a dark top edge and a light bottom edge) with keys sitting on it.

## Components

### Pipeline keys
Backlit rectangular keys on a single rail, with widths fixed per stage. At rest each is a grey gradient key with a 2u dark border. When lit it gets an amber radial backlight with darker amber edges. During acquisition a chase light steps through the keys every 170ms, from LOCK to SCORE, and then settles on VERIFY.

### Soft-keys
Bench tabs with the same key build at a smaller size. The selected key uses an amber gradient. Hover is `brightness(1.05)`.

### Graticule display
A slate bezel around the screen glass. SVG traces use one wire per qubit in channel/wire colours. Keyed gates are hatched pulses (45° channel-colour hatching on a dark fill), CX connectors are near-white (#eef2f4), and the graticule is minor and major lines with axis ticks at column centres. Screen titles and footers are printed in screen-text. A 3u cyan sweep line reveals the traces left to right.

### Knobs and lever
Raster knobs rotate to detents. Detent legends are buttons with a 6u dark pip, and the selected detent's pip turns amber with a 1.5u brown ring. The lever image rotates ±32° and the inactive side's legend dims. Knobs are role=slider and the lever is role=switch.

### Lamp matrix and counters
Raster green (pass) and red (caught) lamps sit in a compiler × check grid. They desaturate and dim while acquiring, then settle with a 45ms stagger. An amber pip marks the current row. Below the lamps, two DSEG7 counters show the naive count in yellow and the TrustPass count in green (#5ee07a).

### Channel readouts
Panel-face plates with a full-height colour tab, an uppercase header, a big lining numeral and a ruled PASS/FAIL cell. Values fade to 25% while measuring.

### Verdict lamp
A square illuminated button drawn in code. A grey housing holds a red radial REJECT face or a green radial ACCEPT face, each with an inner top highlight and bottom shading. It goes dark (#4a3c3c) while measuring.

### Bench units
Units are headed by an ink rule. They hold an evidence histogram screen with a spec sheet, inspect soft-keys over a scrolling wide screen, the acquisition ledger tape (dark cards with red/green verdict headings), and the rating plate.

## Do's and Don'ts

### Do:
- **Do** size every panel length as `calc(n * var(--u))` so the comp holds at every 16:9 width.
- **Do** keep green and red for results only (lamps, PASS/FAIL, verdict, good/bad values).
- **Do** put drop shadows on non-rotating wrappers, falling downward.
- **Do** run one orchestrated acquisition (chase, then sweep reveal, then staggered lamp settle, then verdict) and disable all of it under `prefers-reduced-motion`.
- **Do** carry embedded provenance in every shipped raster plate.
- **Do** use the tab colours on light faces and the channel colours on the screen.

### Don't:
- **Don't** use outward zero-offset glows or bloom on lamps, keys or traces.
- **Don't** use a dark page background, metric cards or violet glow. The chassis is light and the dark lives only behind glass.
- **Don't** use Kufam or DSEG7 outside the wordmark and counters.
- **Don't** reassign a channel colour to a different signal or to decoration.
