# How to run the project

This file is the practical setup guide for the final VR Exposure Therapy app, which is built in [phobia.html](phobia.html).

## Required files

Before running the experience, confirm that these are present:

- [phobia.html](phobia.html)
- [serve.py](serve.py)
- [start-share.sh](start-share.sh)
- [requirements.txt](requirements.txt)
- [aframe/aframe-v1.7.1.min.js](aframe/aframe-v1.7.1.min.js)
- [Images/](Images/)
- [Videos/](Videos/)
- [Sounds/](Sounds/)
- [3DModels/](3DModels/)

If the repo was copied without the large media assets, restore them before testing.

## Local run

From the project root:

```bash
python3 -m pip install -r requirements.txt
python3 serve.py 5500
```

Then open:

```text
http://localhost:5500/phobia.html
```

This is the normal local development workflow.

## Same network / phone testing

To test on a phone or tablet on the same Wi‑Fi network, replace `localhost` with the computer's LAN IP:

```text
http://192.168.1.42:5500/phobia.html
```

On Linux, find the network address with:

```bash
ip a
```

Look for the Wi‑Fi interface's address, usually something like:

```text
192.168.x.x
```

## Troubleshooting

If the phone cannot reach the page:

- make sure the phone is on the same Wi‑Fi network
- confirm the server is still running
- check the firewall for port 5500
- verify the LAN IP is correct

## Interaction testing

The app supports all of the following:

- mouse click on desktop
- touch tap on mobile
- gaze-dwell selection for headset-like use without a controller

The center gaze reticle is essential for the final experience. The user focuses on a button and holds the gaze long enough for the timer to complete, after which the button activates.

## Temporary public sharing

For a temporary external test, run:

```bash
./start-share.sh
```

This starts the local server and creates a temporary tunnel so a tester can open the app from another device.

## Important app behavior

The final app is driven by the scene data in [phobia.html](phobia.html), not by a generic template. The current implementation expects:

- Home has 4 phobia buttons
- each phobia has a page with 4 actions: Mild, Harsh, Jungle, Beach
- calm scenes return to the correct originating phobia page
- scenes with music show the 3D music toggle model
- video scenes are muted for autoplay reliability on mobile browsers

## Recommended test path

1. Launch the app locally.
2. Confirm the Home screen loads.
3. Open each phobia overview page.
4. Check mild and harsh scenes.
5. Verify calm scenes return to the correct phobia page.
6. Test on a mobile browser and in a controller-free gaze workflow.

If content changes are needed, update the scene data and asset paths in [phobia.html](phobia.html) and reload the page.
