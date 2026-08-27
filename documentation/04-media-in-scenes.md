# 4. How images, videos, sounds, and 3D models actually get into a scene

All four media types follow the *same two-step pattern* in A-Frame: **(1) declare/preload it once inside `<a-assets>`, (2) reference it by `#id` wherever you use it.** This separation exists so the browser can start downloading everything up front while the scene is being built, instead of stalling mid-experience waiting for a file.

```html
<a-scene>
  <a-assets>
    <!-- Step 1: declare it here, give it an id -->
    <img id="room1" src="images/room1.jpg">
  </a-assets>

  <!-- Step 2: reference it with #id anywhere in the scene -->
  <a-sky src="#room1"></a-sky>
</a-scene>
```

## Images — 360° photo spheres

**Requirement: the image must be "equirectangular."** This is a specific projection (the same one used for world maps) where a full 360°-horizontal × 180°-vertical view is flattened into a single rectangular image with an **exact 2:1 width:height aspect ratio** (e.g. 4096×2048, 8192×4096). This is *not* an ordinary wide photo — it must be captured with a 360° camera, or stitched from multiple photos with software (Hugin, PTGui, or your phone's built-in "Panorama 360"/"Photo Sphere" mode), or generated. Your `resolution.html` file is literally a test harness for comparing different resolutions of the *same* equirectangular photo (2048px vs 4096px vs 8192px) to see the quality/file-size/load-time trade-off — which is exactly the right instinct, since equirectangular files get large fast (your 8192px sample is ~12MB, and one of your other panoramas is 23MB).

Placed on the inside of a sphere with `<a-sky src="#imageId">`. Because it's a sphere with the image on the *inside* surface, standing in the middle and looking around gives the illusion of standing inside the photographed location.

```html
<a-assets>
  <img id="room1" src="images/room1.jpg">
</a-assets>
<a-sky id="sky" src="#room1" rotation="0 -90 0"></a-sky>
```

The `rotation="0 -90 0"` you see throughout your files just rotates the sphere so the image's "seam" (where the left/right edges of the flat image meet) lines up somewhere less noticeable than straight ahead.

**Switching images** (moving between rooms/scenes) is just changing which asset the sky points at — no new sphere is created, the existing one's texture is swapped:
```js
sky.setAttribute('src', '#room2');
```

## Videos — 360° video spheres

Same idea as images, but using `<a-videosphere>` instead of `<a-sky>`, referencing a `<video>` element instead of an `<img>`:

```html
<a-assets>
  <video id="myVideo" src="videos/clip.mp4" crossorigin="anonymous" preload="auto" playsinline loop></video>
</a-assets>
<a-videosphere id="videoSphere" src="#myVideo" rotation="0 -90 0"></a-videosphere>
```

The video file itself must *also* be equirectangular 360° footage (shot on a 360° camera, e.g. Insta360/Ricoh Theta, or downloaded stock 360° footage) — a normal flat video wrapped onto a sphere would look badly distorted and only fill part of the view.

Practical notes from your actual code:
- `playsinline` + `webkit-playsinline` are required on iOS so the video plays inline instead of forcing native fullscreen.
- Browsers block **autoplay with sound**; you generally need the video muted to autoplay, or gated behind a user tap (this is exactly what the "Tap to enable audio" overlay in your files is working around).
- You only ever show *one* video/image sphere at a time — your code handles this by toggling `visible="true"/"false"` on `<a-sky>` and `<a-videosphere>` together so they don't overlap.

## Sounds — ambient audio per scene

Handled via a normal HTML `<audio>` tag *outside* the 3D scene, connected into A-Frame's audio system via a `sound` component on an entity:

```html
<audio id="bg-audio" src="sounds/beach.mp3" loop autoplay muted playsinline></audio>

<a-entity sound="src: #bg-audio; autoplay: false; loop: true; volume: 0.6"></a-entity>
```

Two flavors A-Frame supports:
- **Non-positional** (`positional: false`) — what your project uses. Volume doesn't change based on where you're looking/standing; it's just ambient background sound for the whole scene. Right for "this room sounds like a construction site" ambience.
- **Positional** (`positional: true`, default) — volume/panning changes based on distance/direction from an object in 3D space, like a fire crackling in one corner of a room getting louder as you turn toward it. You're not using this yet, but it's available any time you want a sound tied to a specific in-scene object (e.g., a spider's sound in Arachnophobia coming specifically from where the spider model is).

Switching sound between scenes = changing the `<audio>` element's `.src` in JavaScript and calling `.play()` again, same pattern as swapping the sky image.

## 3D models (.glb/.gltf) — small objects placed in the scene

Your project uses `.glb` (a single-file, compressed version of the glTF 3D format — the modern standard for web-delivered 3D models, comparable to how `.jpg` is a standard for images). Same preload pattern, using `<a-asset-item>` instead of `<img>`/`<video>`:

```html
<a-assets>
  <a-asset-item id="sound-icon-model" src="3DModels/music-20.glb"></a-asset-item>
</a-assets>

<a-entity gltf-model="#sound-icon-model" position="1.6 1.2 -1" scale="0.25 0.25 0.25"></a-entity>
```

`gltf-model` is the built-in A-Frame component that loads and renders the file. `position` places it in 3D space (x = left/right, y = up/down, z = forward/back — negative z is "into the screen" from the camera's starting point), `scale` resizes it (models come in wildly different native sizes depending on how they were made, so this almost always needs tweaking per-model).

Your project currently uses this for exactly one purpose: a small clickable music-note icon (`music-20.glb`) that toggles ambient sound on/off per room in `index.html`. The same pattern is how you'd add any other small 3D prop into a scene later (a warning sign, a decorative object, an interactive item) — get/make a `.glb`, preload it, place it with `position`/`scale`, optionally attach a click handler the same way your existing buttons do.

**Where to get/make `.glb` models:** [Sketchfab](https://sketchfab.com/) (huge free/paid library, many downloadable as glTF), [Poly Pizza](https://poly.pizza/) (free, low-poly, good for stylized props), [Google Poly archive mirrors], or export directly from Blender (`File > Export > glTF 2.0`).

## Positioning things around the viewer — how your hotspot buttons work

Your code repeatedly uses a small helper (`posFromAngleDeg`) to place buttons/hotspots in a semi-circle in front of the viewer, by converting a compass-style angle into x/z coordinates on a circle of a given radius:

```js
function posFromAngleDeg(angleDeg, radius, y) {
  const a = angleDeg * Math.PI / 180;      // degrees -> radians
  const x = radius * Math.sin(a);
  const z = -radius * Math.cos(a);          // negative = in front of viewer
  return { x, y, z };
}
```

`angleDeg: -60` puts a button off to the left, `0` straight ahead, `60` off to the right, all at a fixed distance (`radius`) from wherever the viewer is standing. This is why buttons in your scenes always appear in a comfortable, non-overlapping fan shape regardless of how many there are — it's simple trigonometry, not manual trial-and-error placement.

Buttons/labels also commonly get a `billboard` custom component attached (one you wrote yourselves — see doc 03), which continuously rotates the object to always face the camera, so text never appears sideways or backwards no matter which way the viewer turns.

**Further reading:**
- [A-Frame docs: `<a-assets>`](https://aframe.io/docs/1.7.0/core/asset-management-system.html)
- [A-Frame docs: `sky` primitive](https://aframe.io/docs/1.7.0/primitives/a-sky.html), [`videosphere`](https://aframe.io/docs/1.7.0/primitives/a-videosphere.html)
- [A-Frame docs: `sound` component](https://aframe.io/docs/1.7.0/components/sound.html)
- [A-Frame docs: `gltf-model` component](https://aframe.io/docs/1.7.0/components/gltf-model.html)
- [glTF format overview (Khronos Group)](https://www.khronos.org/gltf/)
