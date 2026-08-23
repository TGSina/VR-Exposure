# Developer documentation — VR Exposure Therapy

This document covers the exposure-therapy project only (`phobia.html`),
from its origin to its current state, for whoever picks this codebase
up next (including future-you).

## 1. Background / history

- The repo started as a **VR Tour** project: plain `.html` files
  wired up in VS Code, using A-Frame (`aframe-v1.7.1.min.js`),
  served locally with the VS Code **Live Server** extension (Ritwick
  Dey), and optionally tunneled to the public internet with
  `serve.py` (a tiny Python HTTP server) + `ngrok`, driven by
  `start-share.sh`.
- That tour project has three files: `resolution.html` (an image
  quality test page, not a real tour), and `index.html` /
  `index2.html` (two versions of the actual tour — connecting rooms
  of a place via clickable hotspots so the user can move between
  points on a map). This document does not cover those files further.
- The **VR Exposure Therapy** idea reused the same stack and the same
  media conventions, but is a different UX: instead of touring a
  place, it walks a user through phobia-related scenes with a
  calming "safe space" they can retreat to. This became `phobia.html`
  in the same repo.
- Media conventions carried over from the tour project:
  - Images/video are **equirectangular / spherical 360°** captures.
  - Short **sound effects** (not music) accompany some scenes.
  - A simple on/off 3D "music/sound" model existed in the tour
    project for toggling sound in a scene.
- Testing has always been cross-device: desktop browser (Firefox /
  Chrome), phone browser (Firefox / Chrome), and phone-in-a-Cardboard-
  style VR box via Chrome's VR mode.

## 2. What this pass changed

The previous `phobia.html` had a working data model and gaze/click
plumbing, but the actual page/scene graph didn't match the intended
exposure-therapy flow, and a few things made it unreliable in VR.
This pass:

1. **Rebuilt the navigation to match the specified flow exactly**
   (see §3) — home → phobia page → phobia scene ⇄ calm scene, with
   the right button counts at each level.
2. **Fixed camera controls.** `wasd-controls` was removed from the
   camera. This experience never needs locomotion (it's look-around
   360° media, not a walking tour), and leaving `wasd-controls`
   enabled meant the camera entity could drift away from the rig
   origin — which quietly breaks the corner-button anchoring
   described below. Now only `look-controls` remains, and
   `pointerLockEnabled` was set to `false` (see §4).
3. **Left the corner ("side") buttons anchored to `cameraRig`,
   not to the camera entity** — this was already the previous
   behavior, and it's kept deliberately. See §4 for why.
4. **Removed the background sound-effect loop** and its autoplay/
   unmute-overlay machinery (per request). See §5.
5. **Replaced all real media references with two placeholders**,
   `Images/sample.jpg` and `Videos/sample.mp4`, reused across every
   scene. See §6 for how to swap in real content.
6. Added a small always-visible scene label (top-right) and a
   persistent controls hint (top-left) to make manual testing of the
   navigation easier; both are plain 2D DOM overlays, not part of the
   A-Frame scene.

## 3. Navigation / scene graph (current spec)

```
Home
 ├─ 4 big buttons → one per phobia → Phobia Page
 └─ (no corner buttons — nothing to go "back" to)

Phobia Page (×4: one per phobia)
 ├─ 4 big buttons:
 │    Mild scene, Harsh scene, Calm place 1, Calm place 2
 └─ 1 corner button: Home

Phobia Scene (×8: mild + harsh × 4 phobias)
 └─ 4 corner buttons: Home · This phobia's page · Calm 1 · Calm 2

Calm Scene (×2: shared by all phobias)
 └─ 1 corner button: "Back to <the phobia page the user came from>"
```

The calm scenes are shared: a user can arrive at `calm-garden` from
any of the 4 phobias, so `state.returnToPhobia` is tracked in JS and
used to build the single "back" button's label/target correctly.

All of this lives in `PHOBIAS` and `CALM_PLACES` in the `<script>`
block of `phobia.html`, plus four render functions: `renderHome()`,
`renderPhobiaPage(phobiaId)`, `renderPhobiaScene(phobiaId, intensity)`,
`renderCalmScene(calmId, fromPhobiaId)`. Each render function fully
tears down the previous scene's buttons (`clearHotspots()` +
`clearCornerButtons()`) and rebuilds from scratch — there's no
diffing, which keeps the logic simple at this scale (14 scenes).

## 4. Input handling: mouse, touch, and VR gaze

Every button (big or corner) is an `<a-plane class="clickable">` with
three listeners:

- `click` — fires for both **mouse clicks** and **touch taps**,
  because A-Frame's cursor components translate both input types into
  the same DOM-like `click` event on the intersected entity.
- `mouseenter` / `mouseleave` — used to drive a **gaze-dwell** timer
  (`startGaze` / `cancelGaze` in `phobia.html`): when the camera-based
  raycaster's reticle rests on a button for `GAZE_TIME_MS` (1400ms),
  a ring (`#gazeLoader`) fills up and the button fires, exactly like a
  click. This is what makes buttons usable with **no controller at
  all** — just looking at them — which is required for a phone
  dropped into a Cardboard-style box with no touchscreen access and
  no buttons.

Two cursors exist on the camera:

- `#cameraCursor` (`rayOrigin="camera"`) — always raycasts straight
  ahead from screen-center; this is what gaze-dwell uses.
- `#mouseCursor` (`rayOrigin="mouse"`) — raycasts from the actual
  mouse/touch pointer position; this is what makes plain
  click/tap work without needing to first center the item on screen.

### Why corner buttons are anchored to `cameraRig`, not to the camera

It's tempting to make the small corner buttons children of the
`#camera` entity itself, so they behave like a fixed 2D HUD (always
in the bottom corner of the screen no matter which way you look).
**Don't do this** — it silently breaks gaze selection. The gaze
reticle is, by definition, always at screen-center (`rayOrigin=
"camera"`, pointing straight ahead). If a button is rigidly attached
to the camera at an off-center offset, turning your head moves the
button by exactly the same amount as it moves the reticle — the two
can never meet, and the button becomes unselectable by gaze (though
it would still be clickable by mouse, so this bug is easy to miss
during desktop-only testing).

Instead, corner buttons are children of `#corner-container`, which
sits in world space near the rig's origin (not rotating with the
camera). Practically, they behave like small physical objects placed
just below and to the side of where the user is facing **when the
scene loads**. The user turns their head slightly down-left/right to
find them, same as any other object in the room, and the center
gaze reticle can then land on them normally. This is also why
`wasd-controls` was removed (see §2) — without it, the rig never
drifts from `0 0 0`, so these positions stay consistent scene to
scene.

If you later add a real controller (e.g. a Bluetooth Cardboard
trigger or WebXR controller input), this constraint relaxes and a
camera-anchored HUD becomes viable again.

### Hardware volume buttons

The prompt that drove this pass asked whether the page could use the
phone's physical volume up/down buttons as a "confirm" input in VR
mode. Short answer: **not reliably, and not through any standard web
API.** Regular browsers intentionally do not forward hardware
volume-key presses to web pages — the OS reserves them for system
volume, for good UX/security reasons (a website silently rebinding
your volume buttons would be a bad experience). There's no
`VolumeButton` DOM event, and the `Media Session API` only lets a page
respond to OS-level *media transport* controls (play/pause/seek) on
some platforms — not repurpose volume keys for arbitrary actions.

`phobia.html` includes a **disabled-by-default**, best-effort
`keydown` listener for `AudioVolumeUp` (`ENABLE_EXPERIMENTAL_VOLUME_KEYS`
in the script) in case you want to try it on a specific device/browser
during testing, but do not design the UX around it working. Gaze-dwell
is the supported, cross-device solution for controller-less VR input,
and it's already fully implemented.

## 5. Sound effects (currently disabled)

The previous version had a single looping background audio element
(`#bg-audio`) with autoplay-unlock overlay logic (browsers block
autoplaying audio with sound until a user gesture). That has been
**removed entirely** for this pass, per request.

The longer-term intent (from the original project notes) is **short,
per-scene sound effects**, not a single global loop — e.g. a scene-
specific ambience or a one-shot cue, possibly togglable via the
on/off "music" 3D model used in the tour project. When you're ready
to re-add this:

1. Add a `sound` field to the relevant entries in `PHOBIAS` /
   `CALM_PLACES` (e.g. `sound: 'Sounds/spider-ambience.mp3'`).
2. In `setBackgroundFromScene()` (or a sibling function), create/
   reuse an `<audio>` element per scene id, respecting the same
   "must be triggered by a user gesture at least once" browser rule
   the old overlay worked around.
3. Consider A-Frame's built-in `sound` component on an entity instead
   of a raw `<audio>` tag if you want the effect to be positional
   (louder as you look toward its source) — appropriate for the
   on/off 3D sound-toggle model mentioned in the original notes.

## 6. Adding real content

Right now every scene points at one of two placeholders declared in
`<a-assets>`:

```html
<img id="sampleImg" src="Images/sample.jpg" />
<video id="sampleVideo" src="Videos/sample.mp4" ... />
```

To add real media for, say, Arachnophobia's mild scene:

1. Put the real file in `Images/` (or `Videos/`), e.g.
   `Images/arachnophobia-mild.jpg`.
2. Add a new asset tag in `<a-assets>`:
   `<img id="arachnophobiaMildImg" src="Images/arachnophobia-mild.jpg" crossorigin="anonymous" />`
3. In the `PHOBIAS.arachnophobia.mild` entry, change
   `asset: 'sampleImg'` to `asset: 'arachnophobiaMildImg'`.
4. Repeat per scene. Home-page and phobia-page backgrounds are set
   directly with `{ type: 'image', asset: 'sampleImg' }` literals
   inside `renderHome()` / `renderPhobiaPage()` — swap those the same
   way once you have dedicated backgrounds for them (they don't need
   to reuse a `PHOBIAS`/`CALM_PLACES` entry).
5. Update the `info` / `name` strings in `PHOBIAS` and `CALM_PLACES`,
   and the two `TODO:` text blocks in `renderHome()`, with real copy.

Videos must be equirectangular 360° footage, ideally H.264 `.mp4` for
broadest mobile-browser compatibility. Autoplay-with-sound is
unreliable on mobile, which is why `setBackgroundFromScene()` mutes
video scenes before calling `.play()` — decide deliberately if/how
you want sound on video scenes once real content is in.

## 7. Testing workflow

Same as the original project:

- Desktop: Firefox and Chrome, plain click-and-drag to look around,
  click buttons directly.
- Phone: Firefox and Chrome, touch-drag to look around, tap buttons.
- Phone in a Cardboard-style VR box: open the page in Chrome, tap the
  VR-goggles button A-Frame adds automatically (bottom-right), then
  insert the phone — navigate purely by gaze-dwell.

For testing off your local network, run `./start-share.sh` (wraps
`serve.py` + `ngrok`) and open the printed `https://*.ngrok-free.app`
URL on the phone.

## 8. Known limitations / next steps

- No real media, no final copy — see §6.
- Sound effects are disabled — see §5.
- No analytics/logging of which scenes a user visits or how long they
  linger (worth considering for a therapy tool, but out of scope for
  this template pass).
- No WebXR controller support (Cardboard-class only, gaze input).
- No accessibility pass yet (captions for video, larger hit-targets,
  a way to skip/exit at any time, content warnings before harsh
  scenes) — worth doing before this is used with real participants.