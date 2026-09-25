# 6. Public sharing and hosting

The app can be shared in two ways: temporarily for testing or as a static site for longer-term hosting.

## Temporary public access

The project includes a tunnel helper:

```bash
./start-share.sh
```

This starts the local server and exposes the app through a temporary public URL so another device can access it without being on the same network.

## Static hosting

Because this is a simple static web project, it can also be hosted on services that serve plain HTML, JavaScript, and media files. For this project, there are no server-side database or authentication requirements; it is a content-driven browser experience.

## Practical issue: large media files

This project includes 360° stills and videos, which may be large. That creates a real deployment issue:

- large images can slow mobile loading
- large videos can be expensive to stream
- oversized files may exceed free static-hosting limits

This is one of the main reasons it is important to keep the final media package optimized before a public or permanent deployment.

## Recommended approach

For the project in its current form:

- use local testing during development
- use a temporary tunnel for quick external reviews
- compress media before production sharing
- reserve static hosting for the final, optimized asset set

This keeps the project easy to test while avoiding poor performance on mobile data connections.
