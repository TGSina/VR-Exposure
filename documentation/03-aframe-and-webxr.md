# 3. What is A-Frame, what is WebXR, and how do they relate?

## First, WebXR — the foundation everything sits on

**WebXR Device API** is a standard built *into web browsers themselves* (like the `<video>` tag or `fetch()`), maintained by the W3C with input from Google, Meta, Mozilla, Apple, and others. It's the browser's low-level answer to the question: *"how does a webpage talk to a VR headset or AR-capable phone camera?"*

What WebXR gives a web page, at the raw level:
- A way to ask "is there an XR device available?" and "can I start a session?"
- Head position/rotation tracking, per eye, many times per second
- Controller position/button state (for headsets with controllers)
- A rendering loop synced to the headset's refresh rate so the picture doesn't lag behind head movement (critical for not making people motion-sick)
- Two session types: `immersive-vr` (fully replaces your view — what your project uses) and `immersive-ar` (overlays 3D content on the camera passthrough — not used in your project, mentioned in doc 01)

**The catch: WebXR is deliberately low-level and verbose.** Using it directly means writing raw JavaScript that manages a render loop, a 3D scene graph, matrices, shaders — the same amount of code you'd write using Three.js directly, just with extra XR session plumbing on top. It is *not* something you'd hand-write for a project like yours unless you specifically wanted that level of control.

This is exactly the gap A-Frame fills.

## What A-Frame actually is

**A-Frame** ([aframe.io](https://aframe.io/)) is a JavaScript framework that does two things:

1. **Wraps [Three.js](https://threejs.org/)** (the most popular JS 3D-rendering library) so you don't write raw 3D graphics code.
2. **Wraps the WebXR Device API** so entering/exiting VR, headset tracking, and stereo rendering all happen automatically the moment you click A-Frame's built-in "Enter VR" button — no extra code from you at all.

On top of both of those, A-Frame adds its own trick: it lets you describe a 3D scene **declaratively in HTML**, using the custom-tag mechanism explained in doc 02, instead of writing JavaScript to build the scene imperatively. Compare:

```html
<!-- A-Frame: describe what you want -->
<a-scene>
  <a-sky src="images/room1.jpg"></a-sky>
  <a-box position="0 1 -3" color="red"></a-box>
</a-scene>
```

```js
// Raw Three.js: you build it step by step
const scene = new THREE.Scene();
const skyGeo = new THREE.SphereGeometry(500, 60, 40);
const skyMat = new THREE.MeshBasicMaterial({ map: textureLoader.load('images/room1.jpg'), side: THREE.BackSide });
scene.add(new THREE.Mesh(skyGeo, skyMat));
const box = new THREE.Mesh(new THREE.BoxGeometry(), new THREE.MeshStandardMaterial({ color: 'red' }));
box.position.set(0, 1, -3);
scene.add(box);
// ...plus a renderer, camera, lights, animation loop, and XR session handling, all written by hand
```

Same visual result. A-Frame's version is what your project uses throughout.

## Where A-Frame's real power is: the Entity-Component-System (ECS)

Every object in an A-Frame scene is an **entity** (`<a-entity>`, or shorthand tags like `<a-box>`, `<a-sky>`), and everything about how it looks/behaves is attached as a **component**:

```html
<a-entity
  geometry="primitive: box"
  material="color: red"
  position="0 1 -3"
  sound="src: #beep; autoplay: true">
</a-entity>
```

Each attribute (`geometry`, `material`, `position`, `sound`) is an independently swappable, independently reusable **component**. This is the same architectural pattern (ECS) used in professional game engines like Unity — you compose behavior out of small reusable pieces instead of writing one big class per object type.

Your own code already extends this system — every time your `phobia.html`/`index.html` calls `AFRAME.registerComponent('billboard', {...})` or `AFRAME.registerComponent('follow-camera', {...})`, you are writing a **custom component**, in the exact same style as A-Frame's built-in ones. This is the "correct," idiomatic way to add new behavior in A-Frame, and it's also why there's a large ecosystem of free, drop-in community components (physics, hand-tracking, particle effects, teleport-locomotion, etc.) you can add with a single `<script src="...">` tag — see [A-Frame's Awesome/Ecosystem list](https://github.com/aframevr/awesome-aframe).

## Other libraries in the same space, and when you'd pick them instead

| Library | What it is | When you'd choose it over A-Frame |
|---|---|---|
| **[Three.js](https://threejs.org/)** | The lower-level 3D engine A-Frame is *built on*. Pure JavaScript, no HTML tags. | You need fine-grained control A-Frame's components don't expose, or you're not building a "scene" at all (e.g. a 2D-canvas-style data visualization that happens to be 3D). Much steeper learning curve. |
| **[Babylon.js](https://www.babylonjs.com/)** | A full alternative game-engine-style 3D/WebXR library, Microsoft-backed. Also wraps WebXR directly. | You want a more "game engine" feature set out of the box (built-in physics, a visual editor, asset pipeline) and don't need A-Frame's HTML-declarative style. |
| **[PlayCanvas](https://playcanvas.com/)** | A full engine *with a hosted visual editor* (drag-and-drop scene building in a browser IDE), built on WebGL/WebXR. | You want a non-programmer-friendly visual editor rather than hand-writing HTML/JS. |
| **[`<model-viewer>`](https://modelviewer.dev/)** (Google) | A single custom HTML tag for showing *one* 3D model with rotate/zoom/AR-placement, nothing more. | You just need to show one product/object (e.g. "view this chair in AR"), not a full navigable scene. Massive overkill to use A-Frame for that use case. |
| **[AR.js](https://ar-js-org.github.io/AR.js-Docs/)** | Marker-based AR for the web (point your camera at a printed QR-like marker, a 3D model appears on it). Can plug into A-Frame via `aframe-ar` component. | You specifically want camera-passthrough AR anchored to a physical marker, and don't need a headset-VR mode at all. |
| **[8th Wall](https://www.8thwall.com/)** | Commercial (paid) markerless WebAR platform (floor/surface detection without a printed marker, like Snapchat filters). | You want polished markerless AR and are OK paying for a commercial SaaS platform. |

**Bottom line for your two projects:** A-Frame is the right tool. You're building fully navigable 360° environments with menus, audio, and simple 3D icon models — exactly A-Frame's home turf — and you get free VR-headset support via WebXR with zero extra code. There's no library here that would meaningfully out-perform A-Frame for what you're doing; the effort would go into content (better images/videos/sounds/models) and scene logic, not into switching frameworks.

## Practical note: A-Frame version

You're currently on **A-Frame 1.7.1**. As of writing, **1.8.0** is the current stable release — it finished removing legacy WebVR-era code paths (WebVR itself was deprecated years ago in favor of WebXR, but old compatibility code lingered in A-Frame until this release), and it renamed the `oculus-touch-controls` component to `meta-touch-controls` to match Meta's current branding of Quest controllers. Neither change affects anything your current code uses (you don't reference either), so upgrading is low-risk whenever you want to do it — just swap the file in `aframe/` and re-test. Get the latest build from [aframe.io/releases](https://aframe.io/releases/) or `npm i aframe` if you ever move to a build-tooled setup.

**Further reading:**
- [A-Frame official docs](https://aframe.io/docs/1.7.0/introduction/) — the best starting point
- [A-Frame School (interactive tutorial)](https://aframe.io/aframe-school/)
- [MDN: WebXR Device API](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API)
- [immersiveweb.dev](https://immersiveweb.dev/) — WebXR feature/browser support tracker
