# VR Exposure Therapy

This project is a browser-based 360° exposure-therapy experience built with A-Frame. The final app is implemented in [phobia.html](phobia.html), and it is designed around a very specific therapeutic flow: choose a phobia, move into a mild or harsh exposure scene, and then navigate to a calm place when needed.

## What the app does

The current app includes:

- 1 Home screen
- 4 phobia overview pages
- 8 exposure scenes total (2 per phobia: mild + harsh)
- 2 shared calming scenes (Jungle and Beach) used across all phobias
- full scene switching logic for each phobia and calm return path
- support for 360° photo and 360° video backgrounds
- both mouse/touch interaction and gaze-dwell for controller-free use
- an ambient music toggle for scenes that include looping audio

The phobia list in the current code is:

- Kenophobia
- Acrophobia
- Claustrophobia
- Mysophobia

The scene flow is intentionally simple and stable:

- Home → choose a phobia
- Phobia page → choose a scene or a calm place
- Scene → return to Home, the phobia page, or a calm place
- Calm scene → return to the phobia page the user came from

## Project structure

```text
phobia.html          Final exposure-therapy experience
serve.py             Minimal local HTTP server
start-share.sh       Starts the local server and temporary tunnel
requirements.txt     Python requirements for local serving
aframe/              A-Frame runtime folder
Images/              360° image scenes
Videos/              360° video scenes
Sounds/              Ambient audio assets
3DModels/            3D model assets such as the music icon
documentation/       Conceptual and technical docs for the project
README.md            Project summary
HOW_TO_RUN.md        Setup and launch instructions
EXPORTED_FILES.md    Exported repo file inventory and notes
```

## Why this project exists

This project is not a generic VR demo. It is a treatment-oriented 360° scene system where the user is guided through intentionally chosen triggers and calming spaces. The scenario tree in [phobia.html](phobia.html) is built to support exposure-style progression rather than exploratory free roaming.

## Quick start

1. Make sure the required assets are present:
   - `aframe/aframe-v1.7.1.min.js`
   - media files under `Images/` and `Videos/`
   - optional ambient files under `Sounds/`
   - model asset under `3DModels/`
2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Start the local server:
   ```bash
   python3 serve.py 5500
   ```
4. Open the app in a browser:
   ```text
   http://localhost:5500/phobia.html
   ```
5. To test on a phone on the same Wi‑Fi network, use the computer's local IP instead of `localhost`:
   ```text
   http://192.168.1.42:5500/phobia.html
   ```

## Input and controls

The final app supports:

- desktop mouse click
- mobile touch tap
- gaze-dwell activation for controller-free VR use

The center reticle is a key part of the experience. It remains fixed in the center of the screen and triggers a button after a dwell time, which makes the experience usable in a Cardboard-style viewer without a controller.

## External sharing

To expose the app for temporary testing on another device, use:

```bash
./start-share.sh
```

This starts the local server and creates a temporary network tunnel for remote testing.

## Documentation set

The repository includes a small documentation library that explains the project concept and how the experience is built:

- [documentation/01-concepts-vr-ar-web.md](documentation/01-concepts-vr-ar-web.md)
- [documentation/02-html-css-js.md](documentation/02-html-css-js.md)
- [documentation/03-aframe-and-webxr.md](documentation/03-aframe-and-webxr.md)
- [documentation/04-media-in-scenes.md](documentation/04-media-in-scenes.md)
- [documentation/05-sharing-local-network.md](documentation/05-sharing-local-network.md)
- [documentation/06-sharing-public-temporary-and-static.md](documentation/06-sharing-public-temporary-and-static.md)

Use [HOW_TO_RUN.md](HOW_TO_RUN.md) for setup details and [EXPORTED_FILES.md](EXPORTED_FILES.md) for project inventory notes.
