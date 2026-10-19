# EDIT-STYLE.md — Reference video analysis

Reference file: `WhatsApp_Video_2026-10-19_at_10.18.10_PM.mp4`
Container: H.264 478×850 (9:16-ish), 30 fps, AAC 44.1 kHz stereo, 51.2 s, 9.1 MB.

## 0. What this video actually is (read first)

It is **not a normal talking-head Reel**. It is a **before/after showcase reel from an editor's portfolio** ("ALHUSAM VISUALS"), in Egyptian-dialect Arabic, about nutrition (healthy weight gain). The layout is a branded 478×850 canvas that contains two videos:

| Element | Position on the 478×850 canvas | Size |
|---|---|---|
| **"After"** panel (the edited video — **this is the style I analysed**) | x 177–443, y 222–692 | 266×470 (= 9:16) |
| **"Before"** panel (raw green-screen S-LOG3 footage) | x 35–168, y 458–693 | 133×235 (= 9:16) |
| Logo emblem + letter-spaced wordmark | centred, y ≈ 60–140 | emblem ≈ 56 px |
| HUD text (TIMECODE / FORMAT 4K · 25 FPS / PIPELINE S-LOG3 → 709) | x 35, y 232–340 | monospace, tiny, ticking timecode |
| Arabic tagline "لا يليق بك إلا التميز" | centred, y ≈ 740 | ≈ 18 px tall |
| Handle "@alhusam.visuals" + Instagram glyph | centred, y ≈ 767 | ≈ 9 px tall |

Everything below describes the **After panel**. To convert panel pixels to a real 1080×1920 video, multiply by **4.06** (1080 / 266). I give both: `src px` (measured in the 266×470 panel) and `@1080` (converted).

**Resolution caveat:** the file is a 478-wide WhatsApp re-encode, so fonts, glow radius and small sizes are read by eye from very small pixels. Where I could not measure something, I say so.

Evidence images used: `edit-style-evidence/` (contact sheets, cut strips, caption zoom, spectrogram).

---

## 1. Cuts and pacing (measured)

Method: ffmpeg scene detection on the After-panel crop (`crop=266:470:177:222`) at thresholds 0.06 / 0.10 / 0.18 / 0.30, plus a frame-difference trace at 30 fps.

**Cut times (s):** 3.07 · 5.17 · 9.50 · 14.30 · **19.23 (shard wipe)** · 21.93 · 25.07 · **28.43 (shard wipe)** · 32.53 · 36.03 · 40.23 · 42.73
Programme runs 0.5 s → 44.6 s, then an end card (44.6–51.2 s).

| Metric | Value |
|---|---|
| Hard cuts / wipes in the programme | 12 (10 straight jump cuts + 2 hidden behind shard wipes) |
| Shot lengths (s) | 2.57, 2.10, 4.33, 4.80, 4.93, 2.70, 3.14, 3.36, 4.10, 3.50, 4.20, 2.50, 1.87 |
| **Average shot length** | **3.4 s** (median 3.5 s, range 2.1–4.9 s; the 1.87 s is the last shot) |
| Cut rate | ≈ 16 cuts / minute |
| New headline | 12 in 44 s → one every ≈ 3.7 s |
| Caption change | roughly every 1.5–2.5 s |
| "Something new on screen" (cut, headline, graphic or caption change) | roughly every **1.0–1.8 s** (estimate: events overlap, so this is approximate) |

Rhythm rule observed: **a cut and a new headline usually land together**, a graphic (search card, counter, icon row) fills the 3–5 s in between, and captions run underneath all the time. Nothing sits still for more than ≈ 2.5 s.

## 2. Captions (the small lower pill)

Zoomed to 800 px wide at 30 fps (`capHi`, `capChg`).

| Property | Reference value |
|---|---|
| Container | **Frosted-glass pill**, fully rounded ends: ≈ 200×26 src px (75 % of panel width) → **≈ 812×105 px @1080** |
| Pill fill | Dark translucent glass, ≈ 35–45 % black with background blur (blur radius not measurable) |
| Pill border | ≈ 1 px light line, ≈ 30–40 % white |
| Position | Horizontally centred. Pill centre ≈ **73.5 % down the panel** (bottom edge ≈ 76 %), so it sits over the chest/hands, not at the bottom edge |
| Text colour | Off-white **≈ #EDE5DC** (measured) |
| Highlight colour | Warm yellow-gold **≈ #E3BC57** (measured; the real value is probably slightly more saturated, ≈ #F2C94C) |
| Outline / shadow | **None visible.** Legibility comes from the glass pill |
| Font | Rounded geometric Arabic sans, medium/semibold weight. **Closest free: Cairo SemiBold** (alt: Tajawal Medium). Identified by eye only |
| Size | Alef height ≈ 14–16 src px → font size ≈ **58 px @1080** (≈ 3 % of height) |
| Words per line | **2–4 words, 1 line**, max ≈ 22 characters. Example: "تاكل حلويات ووجبات سريعة" |
| Highlight rule | **One word yellow at a time, moving with the voice** (karaoke). Each word stays ≈ 0.2–0.4 s. Other words stay white |
| Entry | Fade-in over ≈ 0.2–0.3 s (6–9 frames) with a small scale-up (≈ 90 → 100 %) and ≈ 5 src px (≈ 20 px @1080) upward settle |
| Exit | Fast fade, ≈ 0.1–0.2 s (not clearly measurable) |
| Caption length on screen | ≈ 1.5–2.5 s each |
| Trailing ellipsis | Some captions end with "..." when the sentence continues ("ممكن يزيد وزنك...") |

Not readable: exact Arabic font name; exact blur strength; whether the pill has a subtle inner gradient.

## 3. Headlines (big gold cards at the top)

| Property | Reference value |
|---|---|
| Position | Centred, **≈ 13 % down the panel** (text centre ≈ y 282 on the canvas), width **70–90 % of panel** |
| Size | Letter height ≈ 25–28 src px → font size ≈ **≈ 120 px @1080** (estimate) |
| Font | Extra-heavy rounded geometric Arabic display, **with stretched letters (tatweel/kashida)** on most headlines: "انتـــه!", "سـعـرات", "سمـــوذي", "ضعيــفة". **Closest free: Cairo Black (900)**; alt Tajawal ExtraBold |
| Colour | **Gold gradient**: bright **≈ #E4B348** at the top → darker **≈ #9D6B19** at the bottom |
| Glow | Soft warm outer glow, ≈ 8–12 px @1080 at ≈ 30–35 % (eyeballed, not measurable) |
| Entry | ≈ 0.3–0.5 s: fade up + slide-up reveal from a mask (the "ضعيفة" frame at 25.0 s shows it half-revealed from below) |
| Exit | Fade-out with slight blur ≈ 0.5 s. A new headline can cross-fade in over the old one (≈ 9.0–9.5 s) |
| Headline timeline | see §4 |

## 4. Motion graphics (every type), with times

Sampled at 2 fps plus 30 fps checks, so times are **±0.25 s** unless stated.

| # | Time (s) | Graphic | Type |
|---|---|---|---|
| 1 | 0.5–2.7 | "؟ نحافة" headline + paper card "زيادة الوزن" in the presenter's hand | headline + prop card |
| 2 | 3.0–4.9 | Gold neon line icons: donut, burger; **red strike-through** on both at ≈ 4.5 s (the only red in the video) | icon pair |
| 3 | 5.3–9.2 | "انتبه!" | headline |
| 4 | 9.5–14.2 | "الزيادة الصحية" | headline |
| 5 | 14.5–18.8 | "سعرات أكثر" | headline |
| 6 | ≈ 17.5–25.0 | **Search-bar glass card** "أكلت تبني جسمك صح" with a typed query ("بروتين، نشويات، ودهون صحية") and a blinking cursor, then 3 gold line icons (avocado, wheat, drumstick) | UI mock-up card |
| 7 | 25.2–28.3 | "ضعيفة" | headline |
| 8 | 26.5–28.3 | White label "تجبر نفسك" with a yellow icon | callout tag |
| 9 | 28.7–32.3 | "سموذي" + cup icon at the left edge | headline + icon |
| 10 | ≈ 31.0–32.3 | Glass chip row with 4 small gold icons above the caption | icon row |
| 11 | 32.5–35.8 | "تزيد سعراتك" | headline |
| 12 | ≈ 33.5–35.0 | **Counter chip**: "+0 → +69 → +500 سعرة حرارية" (number counts up in gold) | counter |
| 13 | 36.0–39.8 | "تمارين المقاومة" + dumbbell icon | headline + icon |
| 14 | ≈ 38.5–40.0 | Yellow tag "عضلات ✓" (dark text on yellow) with a yellow underline | tag + underline |
| 15 | ≈ 40.0–40.5 | White tag "مو مجرد دهون" | tag |
| 16 | 40.3–42.3 | "مو رقم" | headline |
| 17 | ≈ 41.0–42.5 | **Counter chip** "48.0 → 52.3 → 73.6 kg" with a scale icon | counter |
| 18 | 43.0–44.6 | "الهدف" small label above "جسم أقوى" | headline |
| 19 | ≈ 45.5 | Tiny ✦ sparkle | sparkle |
| 20 | intermittent | **Instagram glyph + "@ALHUSAM.VISUALS" watermark** top-right of the After panel (and bottom-left of the Before panel); appears ≈ 1–5 s at a time | watermark |

Counts: **12 headlines**, ≈ 5 icon sets, 2 counters, 1 search card, 3 tags/callouts, 1 sparkle.
- **Not used:** arrows, lower-thirds with a name, progress bars, emoji, stickers.
- **Trigger in speech:** graphics appear on the topic word of the sentence (donut/burger when sweets and fast food are named; counters when numbers are named). I read this from the captions' meaning; without a transcript I cannot time it to the exact word.
- **Icon style:** thin gold outline icons with a soft glow, ≈ 22–30 src px (≈ 90–120 px @1080); containers are dark glass with a thin light border, the same recipe as the caption pill.
- **Background elements:** large glossy **3D gold "folded-paper" shards**, drifting at the panel edges throughout, and sparse gold dust particles; they come to the front and blur (depth of field) during the shard wipes.

## 5. Camera movement (measured, low confidence)

Method: phase-correlation scale search between frames either side of each cut, and between the start and end of each shot.

| Finding | Value |
|---|---|
| Type | **Jump-cut punch-ins / punch-outs on the same footage** (wide ↔ tight), no animated zoom |
| Size of the jump | Tight vs wide ratio **≈ 1.16–1.5×** (median ≈ 1.2×). Measured ratios per cut: 1.16, 1.04, 0.72, 1.06, 0.96, 1.0, 1.5, 1.26, 0.78, 1.2, 0.84, 1.06 (noisy: the correlation response was only 0.09–0.64, so treat as ±0.1) |
| Direction | Alternates in/out; roughly 6 in, 4 out, 2 near-equal |
| Easing | **None.** Every punch is an instant snap on a cut |
| Slow push inside a shot | **No.** Drift inside shots measured 0.98–1.04× (≈ 0–4 %, i.e. effectively static) |
| Shake | **None detected** (shifts ≤ 7 px within shots) |
| Vertical re-framing | Jump cuts also shift the person's vertical position by ≈ 40–55 src px (≈ 9–12 % of panel height), which is what makes the wide/tight pairs read as different "camera angles" |

## 6. Transitions

| Type | Where | Speed |
|---|---|---|
| **Hard jump cut** (with a size change) | 10 of 12 cuts | instant (1 frame) |
| **3D gold shard wipe**: big glossy shards sweep across and fill the frame, the cut hides at peak coverage, then they clear | 19.23 s, 28.43 s (≈ every 9 s, 2 total) | ≈ 0.3–0.35 s total (shards enter 19.10, cover 19.23, clear by ≈ 19.45) |
| **Cross-fade / fade-out into the end card** | ≈ 44.5–45.0 s (panel dissolves to the logo) | ≈ 0.5 s |
| **Intro fade-up from black** | 0.0–0.9 s (black 0–0.4 s, frame fades up blurred → sharp) | ≈ 0.5 s |
| Swap logo → Instagram glyph | ≈ 47.2 s | ≈ 0.3 s cross-fade |

## 7. Sound (partly measured; Whisper could not run)

**Transcription was NOT done.** `faster-whisper` installed, but the model download is blocked by the sandbox network (`huggingface.co` refused by the proxy, and `openaipublic.azureedge.net`/`alphacephei.com` too). To fix this, add `huggingface.co` to **Allowed domains** in the environment's Network settings and I'll rerun it. In the meantime the Arabic text above is **read from the burned-in captions** (not from audio) and any word may be misread.

What I could measure with ffmpeg + signal analysis:

| Property | Value |
|---|---|
| Loudness | **−13.9 LUFS integrated**, loudness range 2.1 LU (very compressed), overall RMS ≈ −16 to −18 dBFS |
| Content | Continuous speech-like signal 0.1–45.3 s (formant structure, 3–8 Hz syllabic modulation = 42 % of the envelope energy) |
| Band balance (mean dB) | sub-bass 30–120 Hz −45 · low-mid 120–500 Hz −21 · voice 500–3400 Hz −24 · air 3.4–9 kHz −48 |
| Steady tone | A constant narrow band near **1.1 kHz** runs through most of the video; I can't tell whether it's a music pad, hum or a voice artefact |
| Music | **Cannot be confirmed.** The spectrogram has no clear beat grid (the autocorrelation lag of 0.418 s ≈ 144 BPM is probably the speech syllable rate, not a track). If there is a music bed it is mixed so low it is buried under the voice |
| Impacts | Low-frequency hits at **≈ 0.1 s** (video start) and **≈ 44.0 s** (as the panel dissolves to the logo): an intro and an outro "boom" are likely |
| End-card sound | Audio goes silent 45.3–47.57 s, then a **single tonal chime ≈ 1.2 s at 47.57–48.74 s** timed to the Instagram glyph reveal, then silence to the end |
| SFX on cuts / zooms / graphics | **No evidence.** Level jumps at the 12 cut times (+6 to +34 dB in the 3.4–9.5 kHz band) are within the range of random moments in the same video (median +20, 90th percentile +32 dB), so I cannot say whooshes exist. The shard wipes do not show a separate low-frequency whoosh either |
| Typing / counter / icon "pops" | Not detectable |

## 8. Look, grade and effects (measured on the After panel, 8 sample frames)

| Property | Value |
|---|---|
| Mean colour (RGB) | ≈ (71–92, 52–71, 33–49): strong warm bias, R/B ≈ 1.75 |
| Saturation (mean HSV) | **54–62 %** |
| Luma percentiles (0–255) | p1 = 1–2 (**blacks crushed to ~0**), median 36–59 (low-key), p99 = 237–248 |
| Palette (k-means, share) | #1A0F06 38 % · #412F1A 28 % · #6F5D45 17 % · #BDA79C 8 % · #EEE8E0 5 % · #CE9946 4 % |
| Grade | Warm amber/gold, low-key, high contrast, deep brown shadows, skin kept natural, olive jacket muted |
| Background | Keyed green screen replaced with a **CG golden-lit lounge** (warm bokeh lights, shelves), slightly blurred |
| Vignette | Present and strong: corner/centre luma ratio 0.11–0.38 (part of it is the set's dark edges) |
| Glow | Soft bloom on gold text, icons and the shards |
| Flashes | White/gold flash only inside the shard wipes; **no stand-alone white flashes** |
| Grain / light leaks | **Not visible** (can't tell at this resolution and compression) |
| Outer frame colours | Deep burgundy-black gradient: **#110102** (top) → **#260405** (near the panel) with a soft red radial glow behind the panel |
| Gold accent | Headline gold **#E4B348 / #9D6B19**, caption highlight **#E3BC57** |
| Lone red | Strike-through on the donut/burger icons (≈ #D9362B, eyeballed) |

## 9. Signature elements (repeat in this video; would repeat across this editor's videos)

1. **Branded frame**: logo emblem + letter-spaced gold wordmark, "After" / "Before" labels in an italic serif, HUD readout (TIMECODE / FORMAT / PIPELINE), corner-bracket marks on the After panel.
2. **Before/After split**: raw S-LOG3 green-screen clip beside the finished edit.
3. **Gold-on-burgundy palette** with glossy **3D gold shards**.
4. **Stretched-letter (kashida) gold headlines**, one per ≈ 3.7 s.
5. **Frosted-glass pill captions** with a one-word yellow karaoke highlight.
6. **Glass UI cards** (search bar, counter chips) with thin gold line icons.
7. **Instagram watermark** that blinks in and out on the panel.
8. **End card**: panel dissolves → big logo + wordmark + tagline + handle (≈ 44.6–47.2 s) → Instagram glyph with a gradient (pink → purple → orange) that settles to white by ≈ 50.5 s, with a chime at 47.57 s.
9. **Tagline** "لا يليق بك إلا التميز" under the frame for the entire video.

## 10. What I could not read (do not treat as fact)

- Exact font names (closest free matches only).
- Audio transcript and word-level timing (Whisper blocked; see §7).
- Whether there is a music bed, and any SFX on cuts.
- Exact blur/glow radii, grain, light leaks.
- Exact entry/exit easing curves (I give durations, not curves).
- Whether the "زيادة الوزن" card in the presenter's hand (0.5–2.7 s) is a real prop or composited.
