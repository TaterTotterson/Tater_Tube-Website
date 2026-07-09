# Install Guide

Tater Tube is meant to run from a ready-to-flash Raspberry Pi appliance image.

## Choose An Image

- **Pi 4 NTSC Composite** for North American and Japanese CRTs.
- **Pi 4 PAL Composite** for PAL CRTs.
- **Pi 5 HDMI Auto** for modern HDMI displays.

Download the latest image from the Images page or the latest GitHub release.

## Flash The SD Card

Use Raspberry Pi Imager, Balena Etcher, or another image-writing tool to flash the `.img.xz` file to an SD card.

After flashing:

- Connect the Pi to the intended display.
- Connect network.
- Connect audio.
- Connect the Argon IR receiver or a keyboard/controller for first setup.
- Boot the Pi.

Tater Tube starts automatically.

## First Setup

Open Settings inside Tater Tube and configure the modules you want:

- Appearance for theme, highlight color, mascot art, and clock.
- Features for enabling or hiding modules.
- System for updates, SSH, fan control, sleep timer, and clock.
- Gamepad for Bluetooth pairing and controller mapping.

## Media Setup

Video on Demand supports Emby, Jellyfin, and Plex.

Video on Demand TV Mode can use automatic library channels plus custom movie and series channels created in the Web Setup UI. Custom channels can optionally use one specific local commercial category.

Tape Deck uses Emby, Jellyfin, or Plex music libraries.

Public Access uses public YouTube playlist IDs or playlist URLs.

Public Access TV Mode and Video on Demand TV Mode can use local commercial categories uploaded through the Web Setup UI. Commercial playback rotates through the selected pool before repeating. Video on Demand TV Mode also supports optional mid-roll commercial breaks.

Over The Air uses HDHomeRun discovery or a configured device address.

Game Center uses a RetroNAS/MiSTer-style ROM share.

PC Link uses Sunshine on the host and Moonlight on the Pi.

Usenet uses a Newznab provider and a compatible stream endpoint.

## Web Setup

Open:

```text
http://tatertube.local:24024/setup
```

Use Web Setup from a phone or computer to configure module logins, API keys, Sunshine pairing, local commercials, and custom Video on Demand TV Mode channels.

## Updates

Use:

```text
Settings -> System -> Check For Updates
```

The update splash keeps the Tater Tube image visible and shows a compact one-line bottom status while the update runs.

For SSH recovery, use the release installer:

```bash
bash <(curl -fsSL https://github.com/TaterTotterson/Tater-Tube/releases/latest/download/install.sh)
```

## Local API

Check status:

```bash
curl http://tatertube.local:24024/api/v1/status
```

Search:

```bash
curl -sS http://tatertube.local:24024/api/v1/library/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"batman","types":["movie","show","game"],"limit":10}'
```

Launch:

```bash
curl -sS http://tatertube.local:24024/api/v1/library/launch \
  -H 'Content-Type: application/json' \
  -d '{"id":"vod:movie:ITEM_ID"}'
```

If API auth is enabled, send `Authorization: Bearer <token>` or `X-TaterTube-Token: <token>`.

## Recovery

SSH is enabled by default on the appliance image so the device can be debugged without reflashing.

Useful checks:

```bash
journalctl -u tatertube -b
sudo systemctl restart tatertube
```
