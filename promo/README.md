# PJT Park Hill — 30-second promo

`pjt-park-hill-promo.mp4`: 1920×1080, 30 fps, H.264 + AAC stereo, exactly 30.0 s, -14 LUFS.
`poster.png` is the end-card still, for use as a thumbnail.

The visual language is taken from pjtpartners.com: white pages, light grotesk headlines (Inter Tight 300 stands in for the house face), the indigo-to-sky hero gradient, quadrant gradient tiles (teal = Strategic Advisory, green = Restructuring), bracket-corner labels, ↳ arrows, and the site's own office photography (`v2/*.png`, cropped from site screenshots). The PJT monogram is a vector trace of the site header mark (`logo()` in `promo.html`).

## Storyboard

| Time | Scene | Sound |
|---|---|---|
| 0.0–3.3 | Site-style hero: gradient panels wipe in over the hallway photo, the monogram draws on, and the line "PJT is a next-generation global investment bank where advice is the main event" appears | Drone, bells, riser |
| 3.3–8.3 | *One Firm. Many Capabilities.* Three gradient tiles appear. Park Hill stays lit while the other two fade, then its tile expands to fill the frame | Impact, pulse and kick come in |
| 8.3–10.3 | **PJT Park Hill**, "Since 2005", with the violet tile beside the painting photo | Impact, full groove |
| 10.3–12.9 | **$565B+** raised across 540+ primary funds, next to the hallway photo | Counter ticks |
| 12.9–15.4 | Secondaries: **$140B+** LP portfolio sales, **$155B+** GP-led, next to the lounge photo | Counter ticks |
| 15.4–18.5 | **5,500+** investor relationships as a network of dots on the hero gradient; strategies scroll past with ↳ arrows | Counter ticks |
| 18.5–24.6 | *One firm. Every market.* Dot-matrix globe turns from New York to London to **Hong Kong** to Tokyo | Bells on each city pin, riser |
| 24.6–30.0 | End card: PJT mark \| Park Hill lockup, "Where advice is the main event.", bracketed pjtpartners.com, regulatory line | Final impact, D-major resolve |

## Before external use

- **Check the figures.** The Park Hill numbers come from secondary web sources quoting the firm. Confirm them against the Park Hill page or the current pitch book.
- **Compliance.** PJT Partners LP is a FINRA member, so marketing communications typically need review and approval before use.
- **Logo and typeface.** Swap in the official logo files and the house typeface if brand guidelines require them. The logo is one function (`logo()`) and the fonts are two constants (`DISPLAY`, `SANS`).
- **Photos.** The photography comes from pjtpartners.com. Confirm internal usage rights with marketing.
- **Music.** The score is synthesized from code (`score.py`), so there are no third-party licensing issues.

## Rebuild

```bash
npm install                       # world-atlas, d3-geo, topojson-client (globe data)
FFMPEG=/path/to/ffmpeg node render.js preview 5 12 27   # stills -> stills/
FFMPEG=/path/to/ffmpeg node render.js full               # -> video_silent.mp4
pip install numpy scipy && python3 score.py              # -> score.wav
ffmpeg -i video_silent.mp4 -i score.wav -af "volume=-1.3dB,alimiter=limit=0.84:level=false" \
  -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart pjt-park-hill-promo.mp4
```

Every frame is a pure function of time (`window.renderAt(frame)` in `promo.html`), so renders are deterministic. Edit copy or timings there, then re-run.
