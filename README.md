# VR Exposure Therapy — Template

A browser-based 360°/VR exposure-therapy simulator built with
[A-Frame](https://aframe.io) (`aframe-v1.7.1.min.js`), plain HTML/JS
(no build step), served locally with a small Python HTTP server and
optionally exposed to the internet with `ngrok`.

This repo also contains an earlier, related but separate project — a
plain **VR Tour** of a physical place (`index.html` / `index2.html` /
`resolution.html`) — which is not covered by this README. This README
and the two docs in `docs/` describe **only `phobia.html`**, the VR
Exposure Therapy simulator.

## What's in this template right now

`phobia.html` is a working, testable **navigation skeleton**:

- 1 Home scene
- 4 phobia overview pages (Arachnophobia, Acrophobia, Claustrophobia,
  Ophidiophobia)
- 8 phobia scenes (1 mild + 1 harsh per phobia)
- 2 calming-place scenes, shared by all 4 phobias

Every scene currently uses the same two placeholder assets:

- `Images/sample.jpg` — for every image-based scene
- `Videos/sample.mp4` — for every video-based scene (used for the
  4 "harsh" scenes, to prove out the 360° video code path)

There is **no real content yet** — no per-phobia photos/videos, no
final copy, no sound effects. That is intentional: the goal of this
pass was to get the page structure, navigation, and input handling
(mouse / touch / VR gaze) solid first, so real content can be dropped
in afterward without touching the navigation logic.

The background sound-effect loop from the previous version has been
removed for now (see `docs/DEVELOPER.md`).

## Quick start

1. Put `aframe-v1.7.1.min.js` in an `aframe/` folder next to
   `phobia.html`.
2. Put a placeholder 360° image at `Images/sample.jpg` and a
   placeholder 360° video at `Videos/sample.mp4`.
3. Serve the folder — either:
   - VS Code **Live Server** extension (right-click `phobia.html` →
     "Open with Live Server"), or
   - `python3 serve.py 5500` (included in this repo) then open
     `http://localhost:5500/phobia.html`.
4. To test on your phone over the internet, run `./start-share.sh`
   (starts `serve.py` + `ngrok` together) and open the `ngrok` URL on
   your phone.
5. On phone: open the URL, tap the VR goggles icon (bottom-right,
   provided automatically by A-Frame) to enter VR mode, then put the
   phone in your Cardboard-style viewer.

See `docs/USER_GUIDE.md` for how to actually navigate the experience,
and `docs/DEVELOPER.md` for the full technical history and how to add
real content.

## Repo layout (exposure-therapy parts only)

```
phobia.html          the VR Exposure Therapy app (this template)
serve.py             minimal local HTTP server
start-share.sh        serve.py + ngrok, for testing on a real phone off-LAN
aframe/               aframe-v1.7.1.min.js goes here (not included)
Images/                360° images go here (not included)
Videos/                360° videos go here (not included)
Sounds/                reserved for future per-scene sound effects (not included)
docs/
  DEVELOPER.md         full technical writeup, from 0 to current state
  USER_GUIDE.md        how to use / navigate the app
```

## Status / next steps

This is a **template pass only** — see the "Next steps" section at
the end of `docs/DEVELOPER.md` for the concrete list of what's left
(real media per scene, sound effects, final copy, any additional
polish).
