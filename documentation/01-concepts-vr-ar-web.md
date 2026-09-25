# 1. Concepts: VR exposure therapy in the browser

This project is a browser-based exposure-therapy experience built around 360° media and guided scene navigation. The final implementation is centered on [phobia.html](../phobia.html), which contains the full app logic.

## Why this project uses the browser

The app is designed to be easy to share and easy to run. A clinician, researcher, or testing participant should be able to open a page on a phone or desktop browser without installing a native app. In a therapy scenario, that matters: the user is not meant to deal with a complex setup, just open the experience and begin the scene flow.

## What the project is doing

The app is not a generic 360° tour and not a freeform exploration scene. It is deliberately structured around exposure treatment:

- the user begins at a Home screen
- each phobia has a dedicated overview page
- mild and harsh exposure scenes are available per phobia
- calming spaces are available for a regulated reset

This gives the experience a controlled pacing: trigger → exposure → recovery, without needing a full game engine or a complex scene graph.

## Why 360° media is suitable here

The core content is immersive but still simple to deliver. A 360° panorama or video lets the user look around and feel physically present in the environment. For exposure therapy, that is more important than full physical locomotion. The app does not need the user to walk through a virtual world; it needs the user to experience a configured environment and make choices inside it.

## Current therapeutic flow

```text
Home
  -> Kenophobia / Acrophobia / Claustrophobia / Mysophobia
      -> Mild scene
      -> Harsh scene
      -> Calm place (Jungle / Beach)
```

This flow is implemented directly in the scene data and render logic. Each calm place remembers which phobia page launched it so the user can return to the correct scene path.

## What is and is not part of the project

This project is specifically about exposure therapy using web-based 360° scenes. It is not a general WebAR product configurator, a marker-based AR demo, or a full VR game. The design is intentionally constrained to the media types and navigation patterns that support the therapeutic use case.
