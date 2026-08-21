Files copied into this new repository from the original workspace:

- index.html (minimal placeholder)
- index2.html (copied placeholder)
- phobia.html (main exposure therapy page — trimmed script)
- resolution.html (copied placeholder)
- serve.py
- start-share.sh
- .gitignore
- .vscode/settings.json
- README.md, HOW_TO_RUN.md, requirements.txt, ASSETS_TO_COPY.txt

Files NOT copied (binaries / large assets):
- images/  (panoramas and other images)
- Videos/  (MP4 files)
- Sounds/  (mp3, wav files)
- 3DModels/ (GLB files)
- aframe/aframe-v1.7.1.min.js  (local JS build)

Reason: this automation copied text files but did not transfer large binary assets. Use `ASSETS_TO_COPY.txt` to copy them with `cp -r` commands.
