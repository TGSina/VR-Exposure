How to run the Exposure Therapy site locally

1) Copy assets (images, videos, sounds, 3D models, and A-Frame) as listed in `ASSETS_TO_COPY.txt`.

2) Start the Python server (from this repo root):

```bash
python3 serve.py 5500
```

Then open `http://localhost:5500/phobia.html` in your browser.

3) To share temporarily via ngrok:

```bash
./start-share.sh
```

Note: `ngrok` must be installed and authenticated (run `ngrok authtoken <your-token>`).

Alternatives to ngrok: `cloudflared tunnel` (Cloudflare Tunnel) or `localtunnel`.

4) Development tips:
- Use VS Code Live Server extension to preview static files (the project includes `serve.py` as a minimal server).
- Test on phone by opening the laptop LAN URL (e.g., `http://192.168.1.100:5500/phobia.html`).
- Verify audio autoplay behavior: browsers often require a user gesture to enable audio.

5) Git setup (recommended):

```bash
git init
git add .
git commit -m "Initial import: VR Exposure Therapy"
```

