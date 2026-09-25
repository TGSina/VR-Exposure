# Exported project files

This repository contains the final VR Exposure Therapy project and its associated documentation. The app logic is concentrated in [phobia.html](phobia.html), while the supporting files explain the project flow and setup process.

## Project file map

```text
README.md
HOW_TO_RUN.md
EXPORTED_FILES.md
requirements.txt
serve.py
start-share.sh
phobia.html
aframe/
  aframe-v1.7.1.min.js
Images/
Videos/
Sounds/
3DModels/
documentation/
  01-concepts-vr-ar-web.md
  02-html-css-js.md
  03-aframe-and-webxr.md
  04-media-in-scenes.md
  05-sharing-local-network.md
  06-sharing-public-temporary-and-static.md
```

## What matters for the final app

- [phobia.html](phobia.html) holds the actual app logic, scene data, UI generation, and media switching.
- [aframe/](aframe/) provides the A-Frame runtime used by the scene.
- [Images/](Images/) and [Videos/](Videos/) hold the 360° visual content.
- [Sounds/](Sounds/) holds optional audio tracks used by scenes with music.
- [3DModels/](3DModels/) holds 3D assets used in the scene, such as the music model.

## Current scene model

The project currently contains four phobia groups:

```text
Kenophobia
Acrophobia
Claustrophobia
Mysophobia
```

Each phobia has:

- a mild scene
- a harsh scene
- two calming-space destinations: Jungle and Beach

This is the actual therapeutic structure of the app, not a generic template or lab demo.

## Notes about assets

Large media files may not always be carried in a stripped-down export. If the app does not load content properly, restore the original media folders before running the project.
