# Build Guide

Most users should use the ready-to-flash release images. Build locally only when changing the app, the image profile, or the website.

## Website

Build the static website:

```bash
python3 scripts/update_site.py
```

The website script keeps a source checkout in:

```text
.cache/tater-tube-source
```

It clones the Tater Tube app repo if the cache is missing and fetches the latest `main` when the cache already exists.

Preview locally:

```bash
python3 -m http.server 8080 -d public_html
```

## App Development

For quick app UI checks on macOS, build the local test app from the Tater Tube source repo. The macOS build is for development only and is not a release target.

For Pi testing, use the release image or build an image profile.

## Image Profiles

The appliance image builder supports:

- `crt-ntsc`
- `crt-pal`
- `pi5-hdmi-auto`

Build examples from the Tater Tube source repo:

```bash
PI_IMAGE_PROFILE=crt-ntsc PI_IMAGE_NAME=tater-tube-ntsc ./scripts/build-pi-image.sh
PI_IMAGE_PROFILE=crt-pal PI_IMAGE_NAME=tater-tube-pal ./scripts/build-pi-image.sh
PI_IMAGE_PROFILE=pi5-hdmi-auto PI_IMAGE_NAME=tater-tube-pi5-hdmi-auto ./scripts/build-pi-image.sh
```

The release workflow publishes the app update bundle and the three ready-to-flash Raspberry Pi images.

## Release Artifacts

Each release should include:

- Pi 4 NTSC composite image.
- Pi 4 PAL composite image.
- Pi 5 HDMI auto image.
- App update tarball.
- Installer script.
- Checksums.

The website Images page reads the latest GitHub release at page load and links directly to the current image files.
