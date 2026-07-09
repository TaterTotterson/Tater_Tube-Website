# Tater Tube

Tater Tube is a retro media appliance for Raspberry Pi. It boots straight into a VCR-style interface and keeps the Linux desktop out of the normal couch experience.

The project targets two appliance styles:

- Raspberry Pi 4 composite output for CRT televisions, with separate NTSC and PAL images.
- Raspberry Pi 5 HDMI output for modern displays, using the display's preferred mode.

## Modules

- **Over The Air** tunes HDHomeRun channels directly with an old-TV channel overlay.
- **Video on Demand** connects to Emby, Jellyfin, or Plex for movies, shows, collections, resume, TV Mode, and custom TV Mode channels.
- **Public Access** plays saved YouTube playlists, supports multiple playlists, and includes playlist-based TV Mode.
- **Usenet** browses media-focused Newznab categories, search, and trending feeds, then launches streams through a compatible streamer.
- **Tape Deck** plays music albums from Emby, Jellyfin, or Plex with a cassette-style interface.
- **Game Center** browses RetroNAS/MiSTer-style ROM folders and launches RetroArch cores.
- **PC Link** pairs with Sunshine through Moonlight for PC or Mac game streaming.
- **Local Files** plays local videos and playlists from folders on the Pi.

## Images

The release page includes three ready-to-flash images:

- Pi 4 NTSC Composite
- Pi 4 PAL Composite
- Pi 5 HDMI Auto

Download the image that matches the display, flash it to an SD card, and boot the Pi. Tater Tube starts automatically.

## Updates

Existing installs update from inside Tater Tube:

```text
Settings -> System -> Check For Updates
```

The updater refreshes the app, helpers, runtime packages, controller support, RetroArch cores, Moonlight, boot assets, IR support, Bluetooth support, fan control, and display setup without a full reflash.

## Web Setup

Open `http://tatertube.local:24024/setup` from a phone or computer on the same network to configure modules without typing everything on the TV.

The Web Setup UI includes module logins and API keys, local commercial categories with video uploads, and custom Video on Demand TV Mode channel creation from Plex, Emby, or Jellyfin movies and series.

## API

Tater Tube exposes a local HTTP API on port 24024 for companion apps and remote-control integrations.

```bash
curl http://tatertube.local:24024/api/v1/status
```

If API auth is enabled, callers send:

```text
Authorization: Bearer <token>
```

or:

```text
X-TaterTube-Token: <token>
```

## Credits

Tater Tube began as a fork of the original upstream retro media player project and is now focused on Tater Tube appliance images, Emby/Jellyfin and Plex support, HDHomeRun OTA, Public Access, Usenet streaming, RetroNAS games, PC Link, and Argon IR defaults.
