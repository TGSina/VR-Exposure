# 1. Why build VR/AR "in the browser" at all?

## The two ways to build a VR/AR experience

There are, broadly, two completely different technical paths to make something like your VR Tour or Phobia Exposure project:

| | **Native VR app** | **WebVR / WebAR (what you're doing)** |
|---|---|---|
| Built with | Unity, Unreal Engine, native Android/iOS/Quest SDKs | HTML + CSS + JavaScript, running inside a normal web browser |
| Distribution | Must be installed via an app store / sideloaded `.apk` | Just a **link**. No install, no app store review, no update process |
| Performance/graphics ceiling | High — full access to GPU, native rendering pipelines | Lower — runs inside the browser's sandbox, so less raw power, but very sufficient for 360° photo/video tours |
| Cross-platform | Usually one build per platform (Quest build ≠ Android build ≠ iOS build) | **One page works everywhere** — phone browser, laptop browser, VR headset browser (Quest Browser, etc.) |
| Update cycle | Rebuild + resubmit + user re-downloads | Edit the file, refresh the page. Done. |
| Your use case fit | Overkill for what you're building | This is exactly the sweet spot |

**Why "web" makes sense for your two projects specifically:** a virtual tour and a phobia exposure tool both live or die by *how easy it is for someone else to open them*. A therapist showing a patient an Acrophobia scene doesn't want to install an app — they want to hand over a phone with a browser tab open, or put that phone in a cardboard headset. A link (or a LAN address) is the lowest-friction way to deliver that. This is the single biggest reason WebXR/WebVR projects exist as a category: **frictionless access**, at some cost in raw graphical power.

## What "VR" actually means in your project right now

Important distinction, because it affects a lot of decisions later:

- **What you have today**: 360° panoramic photo/video "spheres" (`<a-sky>`, `<a-videosphere>`) that the user looks around inside using mouse-drag, touch-drag, or phone gyroscope ("magic window" mode). This does **not** require an actual VR headset or the WebXR API to be entered — a flat phone screen already gives the "look around" effect via the device's gyroscope. This is sometimes called a "**360° tour**" rather than "true VR."
- **What "entering VR"** adds on top: when a user has an actual headset (Quest, or a phone in a Cardboard/VR Box), and clicks A-Frame's built-in "Enter VR" button, the browser requests a WebXR *immersive-vr session* — this is when stereo rendering (one slightly offset image per eye) and head-tracking kick in. A-Frame gives you this "Enter VR" button for free, automatically, as long as the device/browser supports WebXR.

So: your project is a **360° panoramic tour, which is VR-capable** — it works as a flat 2D tour, a gyroscope-driven "magic window" tour on a phone, and a stereo headset experience, all from the *same* HTML file, with zero extra code. That versatility is one of A-Frame's biggest selling points (more in doc 03).

## Common project types in this space

Knowing the landscape helps you see where your two projects sit, and what patterns to borrow from each category:

1. **360° panoramic tours** (your `index.html`/`index2.html`) — real estate walkthroughs, museum tours, campus tours, travel/tourism previews. Core building blocks: equirectangular photos on a sphere, hotspots to jump between spheres, ambient audio per location.
2. **Exposure therapy / training simulators** (your `phobia.html`) — same rendering technique as above, but the *navigation model* is a menu → scenario tree rather than room-to-room, and the content is chosen deliberately to provoke or calm a specific response, often with a "patient info" or session-control overlay for a clinician. Fire-safety training, public-speaking rehearsal apps, and flight/driving anxiety tools use this same pattern.
3. **Product/architecture configurators** — a single 3D object (`.glb`/`.gltf` model) that a user can rotate, place in AR on their real floor, and change materials/colors on. Often built with `<model-viewer>` (Google's library) rather than full A-Frame, since there's no "scene" to walk through, just one object.
4. **WebXR games / interactive experiences** — physics, hand controllers, teleportation locomotion. This is where A-Frame's component ecosystem (`aframe-physics-system`, `super-hands`, etc.) gets heavily used.
5. **Data visualization in 3D** — plotting large datasets as navigable 3D scenes (rare, niche, usually built directly on Three.js/D3 rather than A-Frame).
6. **Markerless WebAR** — camera-passthrough experiences (think: Snapchat-style filters, or "see this IKEA chair in your living room") that overlay 3D content on the live camera feed instead of showing a photographed environment. This is a different technical stack (AR.js, 8th Wall, or the WebXR `immersive-ar` session mode) — not something your current projects use, but worth knowing it's a separate branch of "VR/AR on the web," covered briefly in doc 03.

Your two projects both sit squarely in category 1/2 — the most mature, most beginner-friendly, and most content-driven (rather than code-driven) corner of this space. That's good news: the remaining work is much more about *organizing media and scene logic* than about learning new rendering techniques.

**Further reading:**
- [MDN: Introduction to WebXR](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API) — the browser API underlying all of this
- [immersiveweb.dev](https://immersiveweb.dev/) — community site tracking what WebXR features exist and where
