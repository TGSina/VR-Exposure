# 2. HTML, CSS, and JavaScript in the current app

The final experience is built as a single HTML file with embedded CSS and JavaScript. That pattern works well here because the project is small, self-contained, and meant to be easy to open and test locally.

## HTML layer

The HTML layer defines the scene container, the camera rig, audio elements, media assets, and the scene objects created by A-Frame. In [phobia.html](../phobia.html), the DOM includes:

- `a-scene` for the immersive environment
- `a-sky` for image backgrounds
- `a-videosphere` for video scenes
- camera and gaze reticle elements
- persistent overlays for the top-left and top-right UI labels

## CSS layer

The CSS in the document is not used to style the 3D scene itself. Instead, it styles the simpler 2D overlay UI, such as the help text and top-level labels. This is separate from the actual in-scene buttons, which are A-Frame entities configured in JavaScript.

## JavaScript layer

The JavaScript in [phobia.html](../phobia.html) manages the app's real logic:

- the phobia data model
- the calm scene return state
- media switching between image and video backgrounds
- button creation and behavior
- dwell-timer gaze selection
- scene rendering and teardown

This is where the app's actual behavior lives. The scene data and render functions are the core of the experience.

## Why the single-file approach is useful here

The app is a small static prototype. Putting the scene, styling, and logic together makes the project easier to move, test, and share. The project does not need a build system or a package-first setup just to load one immersive page.

## Important project-specific point

The 3D buttons are not regular HTML buttons. They are created as A-Frame entities using geometry and text components, then wired to click and gaze events. This is a project-specific requirement because the buttons must exist inside the immersive scene, not as ordinary UI elements on the page.
