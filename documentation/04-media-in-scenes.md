# 4. Media files and scene assets

The app uses a consistent pattern for all scene content: media is defined once and then referenced by the JavaScript scene logic. This keeps the scene data clear and lets the app swap between image and video backgrounds without rebuilding the entire scene structure.

## Image-based scenes

The app uses `<a-sky>` for panoramic stills. Each scene entry points to an equirectangular image stored under [Images/](../Images/). These are treated as 360° backgrounds that fill the world around the user.

## Video-based scenes

For the harsher exposure scenes, the app switches to a `<a-videosphere>`. The video file is loaded through the `activeVideo` element and uses the `videoSphere` object for rendering. This is how the app supports 360° video scenes in the same interaction flow as the image scenes.

## Audio and music behavior

The app includes a `sceneMusic` audio element and a small 3D GLB icon used as a toggle button. If a scene has a valid music path, the music toggle appears and allows the user to pause or resume the ambient audio for that scene.

The current logic in [phobia.html](../phobia.html):

- pauses music when leaving a scene
- starts music when a relevant scene is entered
- prevents autoplay issues by handling playback carefully on load
- toggles the audio state when the music button is activated

## Asset organization

The supported media folders are:

- [Images/](../Images/)
- [Videos/](../Videos/)
- [Sounds/](../Sounds/)
- [3DModels/](../3DModels/)

These folders are the project’s actual scene asset pipeline. If a scene fails to load, it is usually because a file path or asset is missing from one of these locations.

## Why scene quality matters

The therapy experience depends heavily on image and video quality. A panoramic image or a 360° video that is too compressed, too low resolution, or incorrectly stitched will weaken the experience even if the navigation logic is perfect. The scene logic is only part of the final effect; the media quality is equally important.
