# CURRENT-LOOK.md — your existing video (baseline for the walkthrough)

File: `final_scholarship_full.mp4` — H.264 1080×1920, 30 fps, AAC, 99.8 s. Arabic (Iraqi dialect), scholarship information, presenter in a bookshop-style set. Same method as `EDIT-STYLE.md` (ffmpeg scene detection, phase-correlation scale search, pixel sampling). No transcript (Whisper model download is blocked); text below is read from the cards.

## Structure
| Time (s) | What |
|---|---|
| 0.0–0.8 | Presenter, no graphics |
| 0.8–1.9 | Title card "مئة منحة دراسية مجانية!" (navy box, gold + white text, bottom) |
| ≈ 2.0–6.3 | Subtitle strip "منحة جامعة النور • 2026 – 2027" (navy, gold text) |
| 6.37–95.3 | **14 info cards**: 1 deadline calendar ("نهاية التقديم", red header, big "24"), 8 conditions ("الشروط العامة", navy header, "n / 8" counter), 4 minimum-score cards ("الحد الأدنى لمعدلات التنافس", red header, 3 rows with % pills), 1 closing card |
| 95.3–99.8 | Presenter alone; last ≈ 2.5 s carries a sustained low tone (outro) |

## Cards (the main graphic)
| Property | Value |
|---|---|
| Duration | **exactly 6.0 s each** (6.00–6.03), regardless of speech |
| Gap between cards | **0.33–0.37 s** (≈ 10 frames) with nothing on screen |
| Coverage | **84 %** of the video |
| Entry / exit | **None: hard on/off** (no fade, slide or scale) |
| Size / position | ≈ 92.6 % of width (centred), ≈ 24 % of height, bottom edge ≈ 96 % → ≈ 1000×460 px at 1080×1920, top at ≈ 72 % |
| Header | ≈ 5 % of height (≈ 100 px): navy **#0C2555** for rules, red **#D12234** for deadline/scores; gold text |
| Counter pill | gold **#FDB012** ("1 / 8"), rounded, left of the header |
| Body | white **#F2F2F2**, dark-navy text (**#082657**), ≈ 40 px corner radius, centred 1–3 lines |
| Score rows | light blue-grey **#EDF3F9** rows, gold % pill on the left, college name on the right |
| Font | Looks like **DejaVu Sans Bold** (the system fallback). Not a designed font |
| Text size | ≈ 40–44 px body (est.) |

## Cuts, camera, pacing
| Metric | Value |
|---|---|
| Camera/jump cuts (excluding card edges) | **≈ 19–20** at 3.93, 5.87, 9.67, 14.07, 17.27, 22.27, 27.27, 34.27, 37.47, 40.67, 45.67, 50.07, 61.47, 65.87, 72.87, 81.07, 84.27, 88.67, 93.07 |
| Average shot length | **≈ 4.8 s** (range 1.9–11.4 s) |
| Cut type | Instant jump cuts with a **scale change**. Scale ratios repeat in three levels: **≈ 1.10×, ≈ 1.25×, and back to 1.0× (0.80–0.84 reciprocal)** → crop levels of about 100 % / 110 % / 125 % |
| Slow push inside a shot | **None** (drift 0.96–1.0; two outliers 1.08 and 1.24 sit next to cut boundaries) |
| Shake | None |
| Transitions | Hard cuts only. No wipes, no flashes |

## Captions
**None.** There are no burned-in speech captions; all text is in the cards. (This is the biggest difference from the reference.)

## Branding
Constant white pill badge, top, "مكتب القيثارة" + round logo: ≈ 400×100 px at 1080 (≈ 37 % of width), top-right, y ≈ 2–7 % of height. No intro logo, no end card.

## Grade and look
| Property | Value |
|---|---|
| Mean RGB | (164, 157, 159): **neutral, no warm bias** |
| Mean luma | 159 / 255 (**bright, high-key**) |
| Mean saturation | 25 % |
| Set | Pink shelves with blue/black/yellow binders (busy, saturated pastels); presenter in a black shirt |
| Effects | No vignette, glow, grain or flashes seen |

## Sound
| Property | Value |
|---|---|
| Loudness | **−13.5 LUFS**, LRA 2.1 LU (compressed, close to the reference's −13.9) |
| Content | Continuous wide-band speech; no music bed visible in the spectrogram; no silence gaps > 0.3 s below −38 dB |
| SFX | None detected (cards and cuts have no matching transient I can separate from speech) |
| Outro | Last ≈ 2.5 s: sustained low-frequency tone |

## Quick comparison with the reference
| | Reference | Yours |
|---|---|---|
| Avg shot | 3.4 s | ≈ 4.8 s |
| Headline/card change | headline every ≈ 3.7 s, 0.3–0.5 s fade | card every 6.0 s + 0.35 s gap, hard cut |
| Captions | glass pill, word-by-word highlight | none |
| Palette | gold on burgundy-black | navy / gold / red / white |
| Grade | warm, low-key, vignette | neutral, bright, no vignette |
| Transitions | jump cuts + 3D shard wipes | jump cuts only |
| Branding | full frame + end card | small top badge only |
| Font | Cairo-like heavy Arabic | DejaVu Sans Bold fallback |
