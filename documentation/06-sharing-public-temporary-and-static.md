# 6. Sharing on the public internet — temporary tunnels and free static hosting

Two different goals, two different tools. Don't conflate them:

- **"I want to show this to someone right now, temporarily"** → a *tunnel* (what ngrok does). URL usually dies when you close the terminal.
- **"I want a permanent link I can send anytime, that stays up"** → *static hosting*. Free, and yes, entirely possible for this kind of project.

## A. Temporary public sharing (ngrok alternatives)

All of these work the same way ngrok does: you run a local server (Live Server, or `serve.py`) on some port, then run a tunnel tool that creates a public URL forwarding to that port.

### Option 1 — Cloudflare Tunnel (`cloudflared`) — recommended, no signup needed for quick tunnels

```bash
# one-time install (Arch Linux)
sudo pacman -S cloudflared
# or download the binary from Cloudflare directly if not in your repos

# with Live Server (or serve.py) already running on port 5500:
cloudflared tunnel --url http://localhost:5500
```
This prints a public `https://<random-name>.trycloudflare.com` URL immediately — no account required for this "quick tunnel" mode. It's free, gives you `https://` automatically (solving the WebXR secure-context issue from doc 05), and in my experience is more stable than ngrok's free tier.

### Option 2 — localtunnel

```bash
npx localtunnel --port 5500
```
No install needed if you have Node.js (`npx` runs it on the fly). Gives a `https://<name>.loca.lt` URL. Slightly less reliable than Cloudflare's tunnel, but literally a one-line command.

### Option 3 — Tailscale Funnel

Requires creating a free [Tailscale](https://tailscale.com/) account and installing their client, but once set up gives you a **stable** URL (doesn't change every time you restart it, unlike the two options above) — worth it if you're sharing with the same person repeatedly during development rather than a one-off demo.

```bash
tailscale funnel 5500
```

### Which to use for your project specifically

Since your video/model files are large, prefer **Cloudflare Tunnel** — it doesn't impose the aggressive bandwidth/connection caps that ngrok's free tier does, which matters once you're streaming a multi-hundred-MB 360° video through it.

## B. Permanent free static hosting — yes, this is possible

"Static hosting" means: a server whose only job is to hand back the exact files you uploaded (HTML/CSS/JS/images/video) with no backend logic — which is **exactly** what your project needs, since `serve.py` isn't doing anything except plain file-serving already. All of the following are genuinely free tiers, not "free trial":

| Service | Free tier limits (approx.) | Best for |
|---|---|---|
| **[GitHub Pages](https://pages.github.com/)** | ~1GB soft repo size limit, ~100GB/month bandwidth (soft, unenforced-but-can-get-throttled) | You're already comfortable with `git` — lowest friction if the repo stays lean |
| **[Cloudflare Pages](https://pages.cloudflare.com/)** | Generous bandwidth, 25MB per-file limit on the free plan | Best free bandwidth; the 25MB/file cap is the catch (your `4096px`/`8192px` images and videos will exceed this) |
| **[Netlify](https://www.netlify.com/)** | 100GB/month bandwidth, drag-and-drop deploy | Easiest possible deploy flow (literally drag a folder onto their website) |
| **[Vercel](https://vercel.com/)** | Similar to Netlify | Also drag-and-drop / CLI-based, similar limits |
| **[Surge.sh](https://surge.sh/)** | Simple, unlimited static sites, one CLI command | Fastest CLI-only deploy if you don't want a web dashboard at all |

### Step-by-step: GitHub Pages (recommended, since you're already using git)

```bash
# 1. From inside your project folder
git init
git add .
git commit -m "Initial commit"

# 2. Create a new empty repo on github.com (via the website), then:
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

Then on GitHub: **Settings → Pages → Source → Deploy from a branch → `main` / `(root)` → Save.**

GitHub gives you a live URL after ~1 minute: `https://<your-username>.github.io/<repo-name>/`. Any file in your repo is reachable at that path, e.g. `.../phobia.html`.

### Step-by-step: Netlify Drop (fastest option, zero git required)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag your entire project folder onto the page
3. You get a live `https://<random-name>.netlify.app` URL within seconds — no account required for a one-off drop (an account lets you update it later instead of getting a new random URL each time)

## The one real obstacle for *your* project: file sizes

Your folder listing shows videos in the 25MB–234MB range and several panoramas over 10MB. This matters for static hosting specifically:

- **GitHub** hard-blocks any single file over 100MB outright (needs [Git LFS](https://git-lfs.com/) to bypass, which itself has its own free-tier storage/bandwidth caps).
- **Cloudflare Pages** free tier rejects any file over 25MB.
- Even where a host *allows* a huge file, a visitor on mobile data will need to download that entire file before the video plays (no adaptive streaming) — a poor experience for the actual therapy/tour use case.

**Practical recommendation:** before doing any permanent public deploy, compress and cap your media:
- Panoramic **images**: 4096px equirectangular width is usually the sweet spot (sharp enough in a headset, far smaller than 8192px) — re-export at ~80% JPEG quality.
- **Videos**: re-encode with `ffmpeg` to a reasonable bitrate/resolution for 360° delivery (e.g. `ffmpeg -i in.mp4 -vf scale=2880:1440 -b:v 8M -c:v libx264 out.mp4` as a starting point — real settings depend on the footage).
- Anything that's still large after that (long videos especially) is a good candidate to host separately on a video-specific host (even an unlisted YouTube 360° upload, or a service like Cloudflare Stream/R2) and just link/embed it, rather than trying to serve it as a static asset alongside your HTML.

This is worth doing as its own pass once you're happy with which media is "final" — no need to do it before your next round of local testing.

**Further reading:**
- [Cloudflare Tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [GitHub Pages docs](https://docs.github.com/en/pages)
- [Git LFS](https://git-lfs.com/) — if you decide you do want large files versioned in git
- [ffmpeg documentation](https://ffmpeg.org/documentation.html) — for video compression
