# 5. Sharing on your local Wi-Fi network — no ngrok, no `serve.py`

## First, an important clarification

You *always* need **some** small web server running to view these files properly — including on your own laptop. Opening an `.html` file directly by double-clicking it (a `file:///...` address) will often *look* fine at first glance, but A-Frame's asset loading, audio, and (for other devices) any network access will be blocked or broken, because browsers deliberately restrict what a `file://` page is allowed to do.

The good news: **you already have a server running every time you use Live Server** — the VS Code extension you're using (Ritwick Dey's "Live Server") *is itself* a small local web server. You don't need to add `serve.py` or ngrok on top of it just to reach it from your phone — Live Server already listens on your whole local network, not just your laptop. You just haven't pointed your phone at the right address yet. That's what this doc fixes.

## Step 1 — find your laptop's LAN IP address

Every device on your Wi-Fi router gets a private address, usually starting with `192.168.x.x` or `10.x.x.x`. This is different from a public internet address — it only works for other devices connected to the *same* router.

**On Windows:**
```
ipconfig
```
Look for **"Wireless LAN adapter Wi-Fi"** → **IPv4 Address**. Example: `192.168.1.42`

**On macOS:**
```
ipconfig getifaddr en0
```
(or System Settings → Wi-Fi → Details → your IP is listed directly)

**On Linux (your Arch Linux laptop, per your file listing):**
```
ip a
```
Look under your Wi-Fi interface (commonly `wlan0` or `wlp3s0`) for a line like `inet 192.168.1.42/24` — the part before the `/24` is your IP.

> If you have both Wi-Fi and Ethernet active, make sure you're reading the IP from whichever interface your phone will also be connecting through (almost always Wi-Fi, since phones rarely use Ethernet).

## Step 2 — make sure Live Server is reachable from other devices, not just `localhost`

By default, Live Server binds to all network interfaces already (this is the extension's default behavior), so this step is usually a formality — but it's worth confirming in your VS Code settings (`settings.json`):

```json
{
  "liveServer.settings.host": "0.0.0.0",
  "liveServer.settings.port": 5500
}
```

`0.0.0.0` means "listen on every network interface this machine has," which is what makes it visible from your phone. Click **"Go Live"** in VS Code as usual.

## Step 3 — build the LAN URL and open it on your phone

Combine the IP from Step 1 with the port (default `5500` for Live Server) and the filename you want to open:

```
http://192.168.1.42:5500/phobia.html
http://192.168.1.42:5500/index.html
```

On your phone:
1. Connect the phone to the **exact same Wi-Fi network** as the laptop (this is the #1 reason this fails — a phone on mobile data, or on a *guest* Wi-Fi network that isolates devices from each other, will not be able to reach the laptop at all).
2. Open Chrome or Firefox and type the URL above directly into the address bar (not a search — the full `http://192.168.x.x:5500/...` address).

## Step 4 — if it doesn't connect: firewall

The most common failure at this point is the laptop's firewall blocking incoming connections on port 5500.

- **Windows:** Windows Defender Firewall will usually prompt "Allow this app through firewall?" the first time Live Server (Node/VS Code) tries to listen — click **Allow** for **Private networks**. If you missed that prompt, go to *Windows Defender Firewall → Allow an app through firewall* and manually enable Node.js/Code for Private networks.
- **Linux (Arch):** if you use `ufw`, `firewalld`, or `iptables`, you'll need to explicitly allow the port:
  ```bash
  sudo ufw allow 5500/tcp
  ```
  (adjust for whichever firewall tool you actually have active — check with `sudo ufw status` first)
- **macOS:** System Settings → Network → Firewall → allow incoming connections for the relevant app.

## A note on HTTPS and WebXR

Some WebXR features (specifically, *entering an actual immersive-vr headset session*) require a "secure context" — meaning `https://`, not `http://` — with one exception: `localhost` is always treated as secure even over plain `http`. Your LAN IP (`http://192.168.x.x:5500`) is **not** localhost, so on some browsers, the "Enter VR" button may refuse to activate a full immersive session over LAN http, even though everything else (the 360° view, gaze buttons, gyroscope look-around, "VR Box" style manual stereo view) works completely fine — those don't require an actual WebXR *session*, just normal page rendering.

If you specifically need to test full immersive-session entry over your LAN (not just visually, but confirming the WebXR session handshake), Chrome has a developer flag for this exact scenario:
```
chrome://flags/#unsafely-treat-insecure-origin-as-secure
```
Add your LAN URL (e.g. `http://192.168.1.42:5500`) to the list and relaunch Chrome. This is a **developer-only workaround**, not something to rely on for anyone else testing your project — for real sharing beyond your own testing, use one of the HTTPS options in doc 06.

**Further reading:**
- [Live Server extension docs](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
- [MDN: What is a secure context?](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)
