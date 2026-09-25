# 5. Sharing locally on the same network

This app is designed to be tested first on a local machine and then on a phone or tablet connected to the same Wi‑Fi network.

## Start the app locally

From the project root:

```bash
python3 serve.py 5500
```

Then open:

```text
http://localhost:5500/phobia.html
```

This is the simplest route for local testing.

## Use it on another device on the same network

Replace `localhost` with the computer's LAN IP address:

```text
http://192.168.1.42:5500/phobia.html
```

On Linux, check your IP with:

```bash
ip a
```

Then use the address shown on the Wi‑Fi adapter, such as:

```text
192.168.x.x
```

## Common problems

If the phone cannot reach the page, check these items:

- same Wi‑Fi network
- correct LAN IP address
- server still running
- firewall permitting port 5500

This is the standard and most reliable way to test the actual mobile interaction flow before doing a public tunnel.

## Why this matters for the app

The immersive interaction model depends on real device behavior: touch input, gaze selection, 360° view, and mobile browser handling. Local network testing is therefore an important validation step before any public share or final presentation.
