# Tater Tube Website

Static website for Tater Tube.

The generated site lives in `public_html`.

## Build

```bash
python3 scripts/update_site.py
```

By default the scripts keep a local Tater Tube source checkout at:

```text
.cache/tater-tube-source
```

If the cache is missing, the script clones:

```text
https://github.com/TaterTotterson/Tater-Tube.git
```

If the cache already exists, the script fetches and resets it to the latest `main` before syncing docs and assets.

Use a local source checkout instead with:

```bash
TATER_TUBE_SOURCE_DIR=/path/to/Tater-Tube python3 scripts/update_site.py
```

Use a different source repo or branch with:

```bash
TATER_TUBE_SOURCE_REPO=https://github.com/example/Tater-Tube.git TATER_TUBE_SOURCE_REF=main python3 scripts/update_site.py
```

## Local Preview

```bash
python3 -m http.server 8080 -d public_html
```
