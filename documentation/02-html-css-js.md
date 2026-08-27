# 2. What is a ".html file that also contains CSS and JS"?

## The three languages, in plain terms

Every normal webpage — and every one of your `.html` files — is built from three different languages, each with one job:

| Language | Job | Analogy |
|---|---|---|
| **HTML** (HyperText Markup Language) | Defines *what content exists* and its structure: this is a button, this is an image, this is a paragraph | The skeleton/bones of a body |
| **CSS** (Cascading Style Sheets) | Defines *how it looks*: colors, spacing, fonts, positioning on screen | The skin, clothes, makeup |
| **JavaScript (JS)** | Defines *what happens* when things occur: a click, a timer finishing, a page loading | The muscles and nervous system — makes things move and react |

A browser reads a `.html` file top to bottom and builds all three into one running page.

## "Separate files" vs. "all-in-one file" — what you're doing

Normally, professional projects split these into three *separate* files:
```
index.html      <- structure only
style.css       <- linked with <link rel="stylesheet" href="style.css">
script.js       <- linked with <script src="script.js"></script>
```

But CSS and JS can *also* be written directly inside an `.html` file, using two special tags:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* CSS goes here */
    body { background: black; }
  </style>
</head>
<body>
  <button id="myBtn">Click me</button>

  <script>
    // JavaScript goes here
    document.getElementById('myBtn').addEventListener('click', () => {
      alert('Hello!');
    });
  </script>
</body>
</html>
```

This is exactly the pattern all of your files (`index.html`, `phobia.html`, `resolution.html`) follow: one file, `<style>` block for CSS, `<script>` block for JS, no separate `.css`/`.js` files at all.

**Why you (probably unknowingly) chose this pattern, and its trade-offs:**

| Pros of one big file | Cons of one big file |
|---|---|
| Dead simple to share — copy one file, everything works | Once a file passes a few hundred lines, it gets hard to scroll/navigate and hard to find things |
| No risk of "forgot to link the CSS file" bugs | Browser can't cache the CSS/JS separately from the HTML — every page load re-downloads everything together (not a big deal for a small personal project, but doesn't scale) |
| Fine for small, single-purpose demo pages (like `resolution.html`) | No reuse between files — you already have three files (`index.html`, `index2.html`, `phobia.html`) that each redefine the *same* gaze-timer and audio-unlock logic, because there's no shared `.js` file to `import` from |

**When to consider splitting it up:** once a project has logic you copy-paste between multiple `.html` files (which you already do — the audio-autoplay code and gaze-timer code are near-identical across `index.html` and `phobia.html`), that's the signal to extract it into a shared `shared.js` file and link it with `<script src="shared.js"></script>` in every page. You don't have to do this now — it's a "when it starts hurting" refactor, not a rule you're breaking.

## The part that's special to your project: custom HTML tags

Normal HTML only has tags the browser understands natively: `<div>`, `<button>`, `<img>`, `<video>`, etc. But your files also contain tags like:

```html
<a-scene>
<a-sky src="#room1"></a-sky>
<a-camera></a-camera>
```

`<a-scene>`, `<a-sky>`, `<a-camera>` are **not** built into browsers. They exist only because you loaded the A-Frame library first:

```html
<script src="aframe/aframe-v1.7.1.min.js"></script>
```

That one line of JavaScript runs code that registers a whole set of brand-new HTML tags (technically called "**Web Components**" / "**custom elements**" — a real, standard browser feature) and teaches the browser what to do when it sees them: build 3D geometry, load a texture, set up a camera, etc. This is the core trick of A-Frame: **it lets you describe a 3D scene using HTML instead of writing 3D graphics code directly.** Doc 03 goes into this in depth.

## Where each language does what, in your files

Using `phobia.html` as the concrete example:

- **HTML** — the `<a-scene>`, `<a-assets>`, `<img id="Partition1">`, `<audio id="bg-audio">` tags: this says *what exists* (which images, which sounds, which 3D scene container) but not how they behave yet.
- **CSS** (the `<style>` block) — purely for the *2D overlay* UI: the "Tap to enable audio" button, the help-text box in the corner. Note CSS does **not** style anything inside `<a-scene>` — the colors/positions of your in-VR buttons (like the "Home" button) are set via A-Frame's own attributes (`material="color:#fff"`, `position="0 0.8 -2.2"`) inside the `<script>` block, not via CSS. This is a common point of confusion: *2D page chrome = CSS, 3D scene content = A-Frame JS attributes.*
- **JavaScript** (the `<script>` block) — everything that *reacts*: gaze timers, button click handlers, switching which image the sky shows, playing/pausing audio. This is the largest and most complex part of your files, and it's where nearly all of your actual project logic lives.

**Further reading:**
- [MDN: Getting started with HTML](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics)
- [MDN: CSS basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/CSS_basics)
- [MDN: JavaScript basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics)
- [MDN: Web Components / Custom Elements](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) — the real browser feature A-Frame is built on top of
