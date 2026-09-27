# PJT Park Hill — 30-second promo

`pjt-park-hill-promo.mp4`: 1920×1080, 30 fps, H.264 + AAC stereo, exactly 30.0 s.
`poster.png` is the end-card still, for use as a thumbnail.

## Storyboard

| Time | Scene | Sound |
|---|---|---|
| 0.0–3.3 | Cold open: *Capital. Counsel. Conviction.* over a gold rule | Drone, one bell per word, riser |
| 3.3–8.3 | **PJT Partners** wordmark, then its three businesses. Park Hill is highlighted | Impact, pulse and kick come in |
| 8.3–10.3 | **PJT Park Hill**, "Since 2005" | Impact, full groove |
| 10.3–12.9 | **$565B+** raised across 540+ primary funds, with a growth line drawing behind it | Counter ticks |
| 12.9–15.4 | Secondaries: **$140B+** LP portfolio sales, **$155B+** GP-led | Counter ticks |
| 15.4–18.5 | **5,500+** investor relationships as a network of dots; strategies scroll past | Counter ticks |
| 18.5–24.6 | Dot-matrix globe turns from New York to London to **Hong Kong** to Tokyo, with arcs between them | Bells on each city pin, big riser |
| 24.6–30.0 | End card: **PJT Park Hill** / *Raise with conviction.* / pjtpartners.com, plus the regulatory line | Final impact, D-major resolve, fade out |

## Before external use

- **Check the figures.** pjtpartners.com was unreachable from the build environment, so the Park Hill numbers ($565B+, 540+ funds, 5,500+ investors, $140B+ / $155B+ secondaries) come from secondary web sources quoting the firm. Confirm them against the current site or pitch book.
- **Compliance.** PJT Partners LP is a FINRA member, so marketing communications typically need review and approval before use.
- The wordmarks are set in Playfair Display, not the official PJT logo. Swap in the brand-approved logo files if you have them.
- The music is synthesized from code (`score.py`), so there are no third-party licensing issues.

## Rebuild

```bash
npm install                       # world-atlas, d3-geo, topojson-client (globe data)
FFMPEG=/path/to/ffmpeg node render.js preview 5 12 27   # stills -> stills/
FFMPEG=/path/to/ffmpeg node render.js full               # -> video_silent.mp4
pip install numpy scipy && python3 score.py              # -> score.wav
ffmpeg -i video_silent.mp4 -i score.wav -af loudnorm=I=-14:TP=-1.5:LRA=7 \
  -c:v copy -c:a aac -b:a 256k -shortest pjt-park-hill-promo.mp4
```

Every frame is a pure function of time (`window.renderAt(frame)` in `promo.html`), so renders are deterministic. Edit copy or timings there, then re-run.
