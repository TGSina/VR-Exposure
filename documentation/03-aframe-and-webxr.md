# 3. A-Frame and WebXR in this project

The app uses A-Frame as the main scene framework. A-Frame is useful here because it lets the project define immersive 3D and 360° content using HTML-like tags instead of writing a full low-level WebGL or Three.js scene by hand.

## What is used in the app

The current implementation uses A-Frame elements such as:

- `<a-scene>`
- `<a-sky>`
- `<a-videosphere>`
- `<a-camera>`
- `<a-entity>`
- text and geometry components for buttons

The user experience is built around a fixed camera and a look-around orientation rather than locomotion. This matches the intended therapy flow: the user is not moving through a map, but experiencing one scene at a time.

## Why there is no walk-through model

The final app is designed to be a look-around 360° environment, not a walking simulation. The camera remains near the origin, and the user turns their head or drags the view to inspect the surroundings. This is the right choice for a simple exposure environment and is a key design constraint of the app.

## Gaze interaction and controller-free VR

The app includes a dwell timer and reticle-based selection. The logic is central to the final project: a user can focus on a button in the center of the screen and hold it long enough for the action to fire. That makes the experience usable without a controller, which is especially important for a phone placed into a Cardboard-style viewer.

## Why corner buttons are placed in world space

The small navigation buttons are not attached directly to the camera. They are positioned in the scene and kept relative to the camera rig so the reticle can meet them naturally during gaze selection. This is a practical project decision that avoids the subtle bug where the button moves with the camera and can never be selected by gaze.

## WebXR relation

The app is browser-based and VR-capable, but it is not built as a custom full controller-driven WebXR game. The project uses the browser environment in a lighter way: immersive scene viewing, look-around interaction, and simple gaze-based UI selection. That is a better fit for this project than a full game-like controller implementation.
