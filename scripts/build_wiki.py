#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import textwrap
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = SCRIPT_DIR.parent
PUBLIC_ROOT = WEBSITE_DIR / "public_html"
ASSET_DIR = PUBLIC_ROOT / "assets"
IMAGE_DIR = ASSET_DIR / "images"
DOC_CONTENT_DIR = WEBSITE_DIR / "docs" / "content"
SOURCE_DOC_DIR = WEBSITE_DIR / "docs" / "source"
SOURCE_CACHE_DIR = WEBSITE_DIR / ".cache" / "tater-tube-source"
GITHUB_REPO = "https://github.com/TaterTotterson/Tater-Tube"
LATEST_RELEASE = f"{GITHUB_REPO}/releases/latest"
STEAM_GITHUB_REPO = "https://github.com/TaterTotterson/Tater-Tube-Steam"
STEAM_LATEST_RELEASE = f"{STEAM_GITHUB_REPO}/releases/latest"
STEAM_ONE_CLICK_INSTALLER = f"{STEAM_LATEST_RELEASE}/download/Install-Tater-Tube.desktop"
STEAM_INSTALL_GUIDE = f"{STEAM_GITHUB_REPO}/blob/main/INSTALL.md"
SERVER_GITHUB_REPO = "https://github.com/TaterTotterson/tater-tube-server"
SERVER_LATEST_RELEASE = f"{SERVER_GITHUB_REPO}/releases/latest"

NAV_ITEMS = [
    ("home", "Home", "index.html"),
    ("modules", "Modules", "modules/index.html"),
    ("images", "Downloads", "images/index.html"),
    ("server", "Server", "server/index.html"),
    ("setup", "Setup", "setup/index.html"),
    ("api", "API", "api/index.html"),
    ("docs", "Docs", "wiki/index.html"),
]

DOC_SOURCES = [
    ("readme", "Project README", "README.md"),
    ("install", "Install Guide", "INSTALL.md"),
    ("building", "Build Guide", "BUILDING.md"),
]

MODULES = [
    {
        "title": "The Tube",
        "image": "usenet.png",
        "text": "Connect to Tater Tube Server for Tube TV channels, Newznab Stream discovery, local movie and TV libraries, music, resume history, and server-side transcoding.",
        "chips": ["Tube TV", "Stream + Local", "Server"],
    },
    {
        "title": "Over The Air",
        "image": "over-the-air.png",
        "text": "Direct HDHomeRun playback with no guide screen. Pick OTA and it tunes like an old TV, with up/down channel changes and a channel OSD.",
        "chips": ["HDHomeRun", "Live TV", "Old-TV OSD"],
    },
    {
        "title": "Video on Demand",
        "image": "video-on-demand.png",
        "text": "Browse Emby, Jellyfin, or Plex libraries from a VCR-style interface with resume playback, TV Mode, editable custom channels, no-repeat local commercials, and optional mid-roll breaks.",
        "chips": ["Emby/Jellyfin", "Mid-Roll", "Custom Channels"],
    },
    {
        "title": "Public Access",
        "image": "public-access.png",
        "text": "Save public YouTube playlists, browse videos from the couch, and run TV Mode with shuffled playlist channels and no-repeat local commercial categories.",
        "chips": ["YouTube Playlists", "yt-dlp", "Commercials"],
    },
    {
        "title": "Tape Deck",
        "image": "tape-deck.png",
        "text": "A cassette-deck music player for Tater Tube Server, Emby/Jellyfin, or Plex albums, complete with album-as-tape browsing, audio-reactive VU visuals, and tape-style fast-forward.",
        "chips": ["Server Music", "Albums", "VU Meter"],
    },
    {
        "title": "Game Center",
        "image": "game-center.png",
        "text": "Browse RetroNAS/MiSTer ROM shares and launch supported systems straight into RetroArch without exposing the RetroArch menu.",
        "chips": ["RetroNAS", "RetroArch", "Controllers"],
    },
    {
        "title": "PC Link",
        "image": "pc-link.png",
        "text": "Pair with Sunshine through Moonlight, list host apps, and stream a stable Pi profile from a PC or Mac into the Tater Tube appliance.",
        "chips": ["Sunshine", "Moonlight", "Game Streaming"],
    },
    {
        "title": "Local Files",
        "image": "local-files.png",
        "text": "Browse local folders on the Pi and play common video files or playlists with loop and shuffle options.",
        "chips": ["Local Video", "M3U", "Shuffle"],
    },
]

IMAGE_DOWNLOADS = [
    {
        "key": "crt-ntsc",
        "title": "Pi 4 NTSC Composite",
        "summary": "For North American/Japanese CRTs using composite video through the Pi 4 AV jack.",
        "chips": ["Pi 4", "CRT", "NTSC"],
    },
    {
        "key": "crt-pal",
        "title": "Pi 4 PAL Composite",
        "summary": "For PAL CRTs. Same app defaults, with PAL composite output configured at boot.",
        "chips": ["Pi 4", "CRT", "PAL"],
    },
    {
        "key": "pi5-hdmi-auto",
        "title": "Pi 5 HDMI Auto",
        "summary": "For modern HDMI screens. The image uses the display's preferred EDID mode.",
        "chips": ["Pi 5", "HDMI", "Auto"],
    },
]

def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def ensure_dirs() -> None:
    for path in [
        PUBLIC_ROOT,
        ASSET_DIR,
        IMAGE_DIR,
        PUBLIC_ROOT / "modules",
        PUBLIC_ROOT / "images",
        PUBLIC_ROOT / "server",
        PUBLIC_ROOT / "setup",
        PUBLIC_ROOT / "api",
        PUBLIC_ROOT / "wiki",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def page_base(depth: int) -> str:
    return "../" * depth


def nav_html(base: str, active: str) -> str:
    links = []
    for key, label, href in NAV_ITEMS:
        class_name = "nav-link is-active" if key == active else "nav-link"
        links.append(f'<a class="{class_name}" href="{base}{href}">{escape(label)}</a>')
    links.append(
        f'<a class="nav-link nav-link-github" href="{GITHUB_REPO}" target="_blank" rel="noreferrer">GitHub</a>'
    )
    return "\n".join(links)


def page_template(title: str, description: str, body: str, *, nav_key: str, depth: int = 0) -> str:
    base = page_base(depth)
    return textwrap.dedent(
        f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="description" content="{escape(description)}">
          <title>{escape(title)}</title>
          <link rel="icon" type="image/png" href="{base}assets/images/tater-tube-logo.png">
          <link rel="stylesheet" href="{base}assets/site.css">
          <script src="{base}assets/site.js" defer></script>
        </head>
        <body data-page="{escape(nav_key)}">
          <header class="site-header">
            <a class="brand" href="{base}index.html" aria-label="Tater Tube home">
              <img src="{base}assets/images/tater-tube-logo.png" alt="Tater Tube">
            </a>
            <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
            <nav class="site-nav" id="site-nav">
              {nav_html(base, nav_key)}
            </nav>
          </header>
          <main>
            {body}
          </main>
          <footer class="site-footer">
            <p>Tater Tube website pages are generated from this website project and the Tater Tube source docs.</p>
            <p><a href="{GITHUB_REPO}" target="_blank" rel="noreferrer">View Tater Tube on GitHub</a></p>
          </footer>
        </body>
        </html>
        """
    )


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def chip(label: str) -> str:
    return f'<span class="chip">{escape(label)}</span>'


def action_link(label: str, href: str, *, secondary: bool = False) -> str:
    class_name = "button button-secondary" if secondary else "button"
    return f'<a class="{class_name}" href="{escape(href)}">{escape(label)}</a>'


def command_box(command: str, label: str = "Terminal") -> str:
    return (
        '<div class="command-box">\n'
        '  <div class="command-head">\n'
        f"    <span>{escape(label)}</span>\n"
        '    <button type="button" data-copy-code>Copy</button>\n'
        "  </div>\n"
        f"  <pre><code>{escape(command.strip())}</code></pre>\n"
        "</div>\n"
    )


def simple_card(title: str, text: str, chips: list[str] | None = None) -> str:
    chip_html = f'<div class="chip-row">{"".join(chip(item) for item in chips or [])}</div>' if chips else ""
    return textwrap.dedent(
        f"""\
        <article class="info-card">
          <h3>{escape(title)}</h3>
          <p>{escape(text)}</p>
          {chip_html}
        </article>
        """
    )


def module_card(module: dict[str, object], base: str = "") -> str:
    chips = "".join(chip(item) for item in module.get("chips", []))
    return textwrap.dedent(
        f"""\
        <article class="module-card">
          <img src="{base}assets/images/{escape(module["image"])}" alt="">
          <h3>{escape(module["title"])}</h3>
          <p>{escape(module["text"])}</p>
          <div class="chip-row">{chips}</div>
        </article>
        """
    )


def image_download_card(image: dict[str, object]) -> str:
    chips = "".join(chip(item) for item in image.get("chips", []))
    return textwrap.dedent(
        f"""\
        <article class="download-card" data-release-card data-release-asset="{escape(image["key"])}">
          <div>
            <span class="eyebrow">Ready image</span>
            <h3>{escape(image["title"])}</h3>
            <p>{escape(image["summary"])}</p>
            <div class="chip-row">{chips}</div>
          </div>
          <dl class="download-meta">
            <div>
              <dt>Version</dt>
              <dd data-release-version>Latest</dd>
            </div>
            <div>
              <dt>File</dt>
              <dd data-release-file>Checking latest release...</dd>
            </div>
            <div>
              <dt>Size</dt>
              <dd data-release-size>--</dd>
            </div>
          </dl>
          <div class="release-actions">
            <a class="button" href="{LATEST_RELEASE}" target="_blank" rel="noreferrer" data-download-link>Open latest release</a>
            <a class="button button-secondary" href="{LATEST_RELEASE}" target="_blank" rel="noreferrer" data-release-card-link>Release notes</a>
          </div>
        </article>
        """
    )


def steam_download_card() -> str:
    return textwrap.dedent(
        f"""\
        <article class="download-card download-card-featured" data-release-card data-release-repo="TaterTotterson/Tater-Tube-Steam" data-release-asset="steam-installer">
          <div>
            <span class="eyebrow">One-click setup</span>
            <h3>Steam Deck &amp; Linux</h3>
            <p>Run the desktop installer once. It downloads the complete Tater Tube release without <code>sudo</code> and asks Steam to add Tater Tube to your non-Steam library.</p>
            <div class="chip-row">{chip("Steam Deck")}{chip("Linux x86_64")}{chip("No sudo")}</div>
          </div>
          <dl class="download-meta">
            <div>
              <dt>Version</dt>
              <dd data-release-version>Latest</dd>
            </div>
            <div>
              <dt>File</dt>
              <dd data-release-file>Install-Tater-Tube.desktop</dd>
            </div>
            <div>
              <dt>Size</dt>
              <dd data-release-size>Checking latest release...</dd>
            </div>
          </dl>
          <div class="release-actions">
            <a class="button" href="{STEAM_ONE_CLICK_INSTALLER}" data-download-link>Download one-click installer</a>
            <a class="button button-secondary" href="{STEAM_INSTALL_GUIDE}" target="_blank" rel="noreferrer">Setup guide</a>
            <a class="button button-secondary" href="{STEAM_LATEST_RELEASE}" target="_blank" rel="noreferrer" data-release-card-link>Release notes</a>
          </div>
        </article>
        """
    )


def render_home_page() -> str:
    cards = "\n".join(
        [
            simple_card(
                "Steam Deck & Linux",
                "Download the one-click desktop installer. It installs without sudo and adds Tater Tube to Steam as a non-Steam game.",
                ["One-click install", "Steam Deck", "Linux x86_64"],
            ),
            simple_card(
                "Raspberry Pi Appliance",
                "Flash the Pi 4 CRT image or Pi 5 HDMI image to an SD card and boot directly into the VCR-style interface.",
                ["Pi 4 CRT", "Pi 5 HDMI", "Ready-to-flash"],
            ),
            simple_card(
                "Tater Tube Server",
                "Run the Docker server for shared Tube TV channels, Newznab Stream, local libraries, player pairing, playback history, and optional transcoding.",
                ["Tube TV", "Docker", "Transcoding"],
            ),
        ]
    )
    featured = "\n".join(module_card(module) for module in MODULES[:4])
    body = f"""
    <section class="hero">
      <img class="hero-bg" src="assets/images/tater-tube-boot.png" alt="" aria-hidden="true">
      <div class="hero-copy">
        <span class="eyebrow">Retro media frontend for Steam Deck, Linux &amp; Raspberry Pi</span>
        <h1>Tater Tube</h1>
        <p>A VCR-style frontend for Steam Deck, Linux, and CRT or HDMI Raspberry Pi builds, led by The Tube: shared server-built TV channels, local libraries, and Newznab streaming alongside Video on Demand, OTA, Public Access, Tape Deck, Game Center, PC Link, and local files.</p>
        <div class="hero-actions">
          {action_link("Get Tater Tube", "images/index.html")}
          {action_link("Set up server", "server/index.html", secondary=True)}
          {action_link("View modules", "modules/index.html", secondary=True)}
        </div>
        <div class="hero-facts" aria-label="Tater Tube highlights">
          <span>Steam Deck one-click install</span>
          <span>Pi 4 CRT composite</span>
          <span>Pi 5 HDMI auto</span>
        </div>
      </div>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">The Tube + Tube TV</span>
        <h2>Build the station once, then tune it from every Tater Tube box.</h2>
        <p>Tater Tube Server scans local movies, series, and music; builds a shared TV schedule; and serves the same channel timeline to every paired player. Automatic genre and decade channels sit beside custom channels made from movies, series, seasons, or individual episodes.</p>
        <div class="chip-row">
          {chip("Shared schedule")}
          {chip("Custom channels")}
          {chip("Commercial breaks")}
          {chip("Channel logos")}
          {chip("TaterText")}
          {chip("Guide CH 999")}
        </div>
        <div class="action-row">
          {action_link("Explore Tater Tube Server", "server/index.html")}
        </div>
      </div>
      <figure class="image-panel">
        <img src="assets/images/usenet.png" alt="Tater mascot for The Tube">
        <figcaption>The Tube is the first module in the Tater Tube menu.</figcaption>
      </figure>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">What it is</span>
        <h2>A small media station that feels like an old TV.</h2>
        <p>Tater Tube turns a Raspberry Pi into a focused appliance. It hides the desktop, starts the app at boot, supports remotes and controllers, and keeps the interface tuned for repeat couch use.</p>
      </div>
      <div class="grid grid-3">
        {cards}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Modules</span>
        <h2>Everything lives behind the same VCR-style menu.</h2>
        <p>Each module is designed to launch cleanly from the main menu and return without showing the Linux desktop. Web Setup handles long-form configuration from a phone or computer.</p>
      </div>
      <div class="grid module-grid">
        {featured}
      </div>
      <div class="action-row">
        {action_link("See every module", "modules/index.html")}
      </div>
    </section>
    """
    return page_template(
        "Tater Tube | Retro media frontend for Steam Deck, Linux & Raspberry Pi",
        "Tater Tube is a VCR-style media frontend for Steam Deck, Linux x86_64, Raspberry Pi CRT composite, and Pi 5 HDMI builds.",
        body,
        nav_key="home",
    )


def render_modules_page() -> str:
    cards = "\n".join(module_card(module, "../") for module in MODULES)
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Module guide</span>
        <h1>Modules</h1>
        <p>Tater Tube keeps media, games, PC streaming, and local playback in separate focused modules. The main menu can show a matching Tater mascot for each one.</p>
      </div>
      <div class="grid module-grid">
        {cards}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">TV Mode</span>
        <h2>Three ways to turn a library into channels.</h2>
        <p>Each TV Mode keeps the same channel-up, channel-down, VCR overlay, and commercial-break feel while using the source that best fits the module.</p>
      </div>
      <div class="grid grid-3">
        {simple_card("Tube TV", "Tater Tube Server plans one shared timeline for every paired player. It creates category channels, honors custom channel numbers, inserts server-hosted commercials, and keeps every box tuned to the same point in the schedule.", ["Server Scheduled", "Shared Channels", "Guide CH 999"])}
        {simple_card("VoD TV Mode", "Turn Plex, Emby, or Jellyfin movies and series into automatic or custom channels. Playback stays local to that Tater Tube box and supports selected commercial categories and optional mid-rolls.", ["Plex/Emby/Jellyfin", "Custom Channels", "Mid-Roll"])}
        {simple_card("Public Access TV Mode", "Turn saved YouTube playlists into shuffled public-access channels and mix in selected local commercial categories between videos.", ["YouTube", "Playlist Channels", "Commercials"])}
      </div>
    </section>

    <section class="section flow-section">
      <div class="section-head">
        <span class="eyebrow">Tube TV dial</span>
        <h2>A complete little cable system inside The Tube.</h2>
        <p>Custom channel 01 appears only when it is explicitly created. Automatic channels begin at 02, TaterText occupies the high channel pages, and the continuously scrolling Tater Guide lives on channel 999.</p>
      </div>
      <div class="flow-strip">
        <div><strong>CH 01</strong><span>Optional custom channel</span></div>
        <div><strong>CH 02+</strong><span>Custom + automatic channels</span></div>
        <div><strong>100-888</strong><span>TaterText pages</span></div>
        <div><strong>CH 999</strong><span>Scrolling Tater Guide</span></div>
      </div>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">Shared controls</span>
        <h2>Remote, controller, keyboard, and API control use one app shell.</h2>
        <p>The Pi image includes Argon IR defaults, Bluetooth controller pairing, a controller mapper, media keys, mpv OSD overlays, and a local HTTP API for companion apps.</p>
        <div class="chip-row">
          {chip("Argon IR")}
          {chip("Bluetooth gamepads")}
          {chip("USB controllers")}
          {chip("HTTP API")}
        </div>
      </div>
      <figure class="image-panel">
        <img src="../assets/images/game-center.png" alt="Tater mascot holding a game controller">
        <figcaption>Controllers can navigate Tater Tube and map into RetroArch cores.</figcaption>
      </figure>
    </section>
    """
    return page_template(
        "Modules | Tater Tube",
        "Overview of The Tube, Tube TV, VOD, OTA, Public Access, Tape Deck, Game Center, PC Link, and Local Files.",
        body,
        nav_key="modules",
        depth=1,
    )


def render_images_page() -> str:
    cards = "\n".join(image_download_card(image) for image in IMAGE_DOWNLOADS)
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Choose your platform</span>
        <h1>Downloads</h1>
        <p>Use the one-click installer for Steam Deck or Linux. For Raspberry Pi, choose the ready-to-flash image that matches your display.</p>
      </div>
      <div class="section-head section-head-subsection">
        <span class="eyebrow">Desktop edition</span>
        <h2>Steam Deck &amp; Linux</h2>
        <p>On Steam Deck, switch to Desktop Mode before downloading. Open the installer, approve the execution prompt, and leave it open while it downloads the complete release.</p>
        <div class="latest-release-panel" data-latest-release data-release-repo="TaterTotterson/Tater-Tube-Steam">
          <div>
            <span class="release-label">Latest Steam release</span>
            <strong data-release-tag>Checking...</strong>
            <span data-release-status>The one-click installer loads from GitHub.</span>
          </div>
          <a class="button button-secondary" href="{STEAM_LATEST_RELEASE}" target="_blank" rel="noreferrer" data-release-link>Open Steam release</a>
        </div>
      </div>
      <div class="grid download-grid download-grid-featured">
        {steam_download_card()}
      </div>
      <div class="flow-strip flow-strip-four install-flow">
        <div><strong>1. Desktop Mode</strong><span>Open Steam Deck's desktop</span></div>
        <div><strong>2. Download</strong><span>Grab the one-click installer</span></div>
        <div><strong>3. Run Once</strong><span>Approve and let it finish</span></div>
        <div><strong>4. Play</strong><span>Launch Tater Tube from Steam</span></div>
      </div>
    </section>

    <section class="section" id="pi-images">
      <div class="section-head">
        <span class="eyebrow">Raspberry Pi edition</span>
        <h2>Ready-to-flash Pi images</h2>
        <p>Pick the image for your display, flash it to an SD card, and boot the Pi. Tater Tube starts automatically.</p>
        <div class="latest-release-panel" data-latest-release>
          <div>
            <span class="release-label">Latest Pi release</span>
            <strong data-release-tag>Checking...</strong>
            <span data-release-status>Direct image links load from GitHub.</span>
          </div>
          <a class="button button-secondary" href="{LATEST_RELEASE}" target="_blank" rel="noreferrer" data-release-link>Open Pi release</a>
        </div>
      </div>
      <div class="grid download-grid">
        {cards}
      </div>
    </section>

    <section class="section flow-section">
      <div class="section-head">
        <span class="eyebrow">Pi display profiles</span>
        <h2>The Pi image controls the video output.</h2>
      </div>
      <div class="flow-strip">
        <div><strong>CRT NTSC</strong><span>Pi 4 composite image</span></div>
        <div><strong>CRT PAL</strong><span>Pi 4 composite image</span></div>
        <div><strong>HDMI</strong><span>Pi 5 auto image</span></div>
        <div><strong>Update</strong><span>Built-in updater later</span></div>
        <div><strong>Recover</strong><span>SSH enabled by default</span></div>
      </div>
    </section>
    """
    return page_template(
        "Downloads | Tater Tube",
        "Download Tater Tube for Steam Deck and Linux with the one-click installer, or choose a ready-to-flash Raspberry Pi image.",
        body,
        nav_key="images",
        depth=1,
    )


def render_server_page() -> str:
    docker_compose = """services:
  tater-tube-server:
    image: ghcr.io/tatertotterson/tater-tube-server:latest
    container_name: tater-tube-server
    ports:
      - "8080:8080"
    volumes:
      - /mnt/user/appdata/tater-tube-server/config:/config
      - /mnt/user/media/movies:/media/movies:ro
      - /mnt/user/media/tv:/media/tv:ro
    restart: unless-stopped"""
    hw_compose = """services:
  tater-tube-server:
    image: ghcr.io/tatertotterson/tater-tube-server:latest
    devices:
      - /dev/dri:/dev/dri
    volumes:
      - /path/to/tater-tube-server/config:/config"""
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Backend for The Tube</span>
        <h1>Tater Tube Server</h1>
        <p>The server gives every paired player the same Tube TV lineup plus Newznab Stream discovery, local movie, TV, and music libraries, resume history, activity tracking, and optional FFmpeg transcoding.</p>
        <div class="latest-release-panel" data-latest-release data-release-repo="TaterTotterson/tater-tube-server">
          <div>
            <span class="release-label">Latest server release</span>
            <strong data-release-tag>Checking...</strong>
            <span data-release-status>Server release information loads from GitHub.</span>
          </div>
          <a class="button button-secondary" href="{SERVER_LATEST_RELEASE}" target="_blank" rel="noreferrer" data-release-link>Open release</a>
        </div>
      </div>
      <div class="grid grid-3">
        {simple_card("Tube TV", "Build automatic and custom channels from local media, then tune the same scheduled lineup from every paired Tater Tube player.", ["Shared Schedule", "Guide", "TaterText"])}
        {simple_card("Stream + Local", "Use Newznab Stream for releases and Local Media for movies, series, music, resume playback, and category browsing.", ["Newznab", "Local Media", "Music"])}
        {simple_card("Pair Players", "Create short-lived PINs in the web UI, give players friendly names, and revoke or rename them later.", ["PIN", "Rename", "Dashboard"])}
      </div>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">Docker install</span>
        <h2>Start with the latest container image.</h2>
        <p>The web UI runs on port 8080. Login is disabled by default so setup is quick on a trusted home network.</p>
        {command_box("docker pull ghcr.io/tatertotterson/tater-tube-server:latest", "Docker pull")}
        {command_box(docker_compose, "docker-compose.yml")}
      </div>
      <figure class="image-panel">
        <img src="../assets/images/tater-tube-logo.png" alt="Tater Tube logo">
        <figcaption>Open <code>http://SERVER-IP:8080</code> after the container starts.</figcaption>
      </figure>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">Tube TV</span>
        <h2>A shared, scheduled channel lineup built from your library.</h2>
        <p>The server plans the timeline ahead so every paired player sees the same program or commercial at the same moment. Automatic channels use library metadata for genres, decades, movies, and series; custom channels can include movies, entire series, seasons, or individual episodes and can claim a specific VCR-style channel number.</p>
        <div class="chip-row">
          {chip("Automatic channels")}
          {chip("Editable custom channels")}
          {chip("Assigned channel numbers")}
          {chip("Shared timeline")}
        </div>
      </div>
      <figure class="image-panel">
        <img src="../assets/images/usenet.png" alt="Tater mascot for The Tube">
        <figcaption>Tube TV appears above Stream and Local when enabled on the server.</figcaption>
      </figure>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Station details</span>
        <h2>Commercial breaks, channel logos, a guide, and TaterText are part of the schedule.</h2>
      </div>
      <div class="grid grid-3">
        {simple_card("Commercial Library", "Upload local commercial videos into server categories. Tube TV selects only enabled categories, avoids repeats until the pool is exhausted, and keeps logos off during breaks.", ["Local Uploads", "Categories", "No Repeat"])}
        {simple_card("Channel Logos", "Choose a logo and its screen corner for each custom channel. Automatic channels can select fitting station marks from the bundled TV logo catalog.", ["Watermark", "Four Corners", "Per Channel"])}
        {simple_card("Guide + TaterText", "Channel 999 is a time-synced scrolling guide. High channel pages provide authentic blocky TaterText screens for status, now playing, server information, and controls.", ["CH 999", "Pages 100-888", "VCR Style"])}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Downloads</span>
        <h2>Install the server from the Docker image.</h2>
        <p>The release publishes one multi-architecture container image tagged <code>latest</code>. Use the GitHub release for notes and the package page for container details.</p>
      </div>
      <div class="grid download-grid">
        <article class="download-card">
          <div>
            <span class="eyebrow">Recommended</span>
            <h3>Docker Image</h3>
            <p>Multi-architecture container image for amd64 and arm64 hosts.</p>
            <div class="chip-row">{chip("Docker")}{chip("amd64")}{chip("arm64")}</div>
          </div>
          {command_box("docker pull ghcr.io/tatertotterson/tater-tube-server:latest", "Pull latest")}
          <div class="release-actions">
            <a class="button" href="https://github.com/users/TaterTotterson/packages/container/package/tater-tube-server" target="_blank" rel="noreferrer">Open package</a>
          </div>
        </article>
        <article class="download-card">
          <div>
            <span class="eyebrow">Release</span>
            <h3>Server Release Notes</h3>
            <p>View the current release notes, changelog, and source archives.</p>
            <div class="chip-row">{chip("v1.0.0+")}{chip("Changelog")}{chip("Source")}</div>
          </div>
          <div class="release-actions">
            <a class="button" href="{SERVER_LATEST_RELEASE}" target="_blank" rel="noreferrer">Open release</a>
            <a class="button button-secondary" href="{SERVER_GITHUB_REPO}" target="_blank" rel="noreferrer">GitHub</a>
          </div>
        </article>
        <article class="download-card">
          <div>
            <span class="eyebrow">Persistent data</span>
            <h3>Config Volume</h3>
            <p>Map one host folder to <code>/config</code>. It stores settings, player tokens, metadata, playback history, Tube TV schedules, commercial uploads, and working cache.</p>
            <div class="chip-row">{chip("/config")}{chip("Settings")}{chip("TV Data")}</div>
          </div>
          {command_box("- /mnt/user/appdata/tater-tube-server/config:/config", "Volume")}
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Local Media</span>
        <h2>Map host folders, then add container paths in the UI.</h2>
        <p>Mount host media folders read-only into the container. In <code>Configuration -> Local Media</code>, use container paths like <code>/media/movies</code>, not host paths. Scanned metadata powers library browsing, Continue Watching, Tape Deck music, automatic channels, and the custom channel builder.</p>
      </div>
      <div class="grid grid-3">
        {simple_card("Movies", "Scans titles, dates, genres, duration, and artwork into a browsable movie library.", ["Movies", "Metadata", "Resume"])}
        {simple_card("TV Shows", "Browses by series, season, and episode while tracking the next episode and current resume point.", ["Series", "Seasons", "Continue Watching"])}
        {simple_card("Music + Folders", "Provides server albums to Tape Deck and can also preserve a source folder's directory structure.", ["Music", "Tape Deck", "Folders"])}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Dashboard + Activity</span>
        <h2>See what every player is doing.</h2>
        <p>The dashboard shows paired players and active streams. Activity keeps playback history for Tube TV, Stream, and Local with the player name, media title, time, duration, progress, and direct, software, or hardware-transcode details.</p>
      </div>
      <div class="grid grid-3">
        {simple_card("Named Players", "Name each paired box for its room, then rename or revoke it from the server.", ["PIN Pairing", "Friendly Names"])}
        {simple_card("Active Streams", "See what is playing now, current progress, throughput, selected profile, and acceleration engine.", ["Now Playing", "Live Stats"])}
        {simple_card("Playback Activity", "Review completed and interrupted local, Tube TV, and Newznab playback in one VCR-themed history view.", ["History", "Player", "HW Engine"])}
      </div>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">Hardware transcoding</span>
        <h2>Enable FFmpeg profiles when the player needs a lighter stream.</h2>
        <p>The server includes CRT 480p, HDMI 1080p, and HDMI 4K profiles. The dashboard shows detected encoders and each active player card shows direct play, software transcode, or hardware transcode.</p>
        {command_box(hw_compose, "Intel/AMD/Pi device mapping")}
      </div>
      <div class="grid">
        {simple_card("Hardware Detection", "The server checks FFmpeg and available encoders from the Hardware Transcoding tab.", ["VAAPI", "QSV", "NVENC"])}
        {simple_card("Player Stats", "The dashboard shows what each paired player is watching and whether hardware acceleration is active.", ["Now Playing", "HW Status"])}
      </div>
    </section>
    """
    return page_template(
        "Server | Tater Tube",
        "Tater Tube Server setup for Tube TV, Docker, local libraries, Newznab Stream, player pairing, activity, and hardware transcoding.",
        body,
        nav_key="server",
        depth=1,
    )


def render_setup_page() -> str:
    flash_steps = "\n".join(
        [
            simple_card("1. Download", "Open the latest GitHub release and choose the NTSC, PAL, or Pi 5 HDMI image for your display."),
            simple_card("2. Flash", "Use Raspberry Pi Imager, Balena Etcher, or dd to write the `.img.xz` to an SD card."),
            simple_card("3. Boot", "Connect the display, audio, remote receiver, and network, then boot directly into Tater Tube."),
        ]
    )
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Start here</span>
        <h1>Setup</h1>
        <p>Choose the Steam Deck/Linux installer or a ready-to-flash Raspberry Pi image, then configure modules from Settings inside Tater Tube.</p>
      </div>
      <div class="section-head section-head-subsection">
        <span class="eyebrow">Steam Deck &amp; Linux</span>
        <h2>Install Tater Tube into Steam in one pass.</h2>
        <p>On Steam Deck, switch to Desktop Mode first. Download and open <code>Install-Tater-Tube.desktop</code>, approve the execution prompt, and leave it open while the full release downloads. The installer runs without <code>sudo</code> and asks Steam to add Tater Tube to the non-Steam library.</p>
        <div class="action-row">
          {action_link("Download one-click installer", STEAM_ONE_CLICK_INSTALLER)}
          {action_link("Full Steam setup guide", STEAM_INSTALL_GUIDE, secondary=True)}
        </div>
      </div>
      <div class="grid grid-3">
        {simple_card("1. Desktop Mode", "On Steam Deck, press the Steam button, choose Power, then Switch to Desktop.")}
        {simple_card("2. Run Installer", "Download and open Install-Tater-Tube.desktop, then approve the prompt to run it.")}
        {simple_card("3. Launch in Steam", "Let the installer finish, return to Gaming Mode, and open Tater Tube from the non-Steam library.")}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Raspberry Pi</span>
        <h2>Flash the image for your display.</h2>
        <p>Choose the NTSC, PAL, or Pi 5 HDMI image. The Pi boots directly into Tater Tube as a dedicated appliance.</p>
        <div class="action-row">
          {action_link("Choose a Pi image", "../images/index.html#pi-images")}
        </div>
      </div>
      <div class="grid grid-3">
        {flash_steps}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">The Tube backend</span>
        <h2>Use Tater Tube Server for Tube TV, Stream, and Local libraries.</h2>
        <p>Install the server on a NAS, PC, or small Linux host. It handles the shared Tube TV schedule, Newznab Stream, local media folders, music, player pairing, activity history, and optional transcoding.</p>
        <div class="action-row">
          {action_link("Server setup", "../server/index.html")}
          {action_link("Server downloads", SERVER_LATEST_RELEASE, secondary=True)}
        </div>
      </div>
    </section>

    <section class="section split-section">
      <div class="split-copy">
        <span class="eyebrow">Normal update path</span>
        <h2>Existing installs update from inside Tater Tube.</h2>
        <p>On Steam Deck, Linux, or Pi, use Settings, System, Check For Updates. The Pi updater also refreshes appliance helpers, runtime packages, RetroArch cores, Moonlight, Bluetooth support, boot splash, IR, fan control, and display setup.</p>
        {command_box("bash <(curl -fsSL https://github.com/TaterTotterson/Tater-Tube/releases/latest/download/install.sh)", "SSH update fallback")}
      </div>
      <figure class="image-panel">
        <img src="../assets/images/tater-tube-boot.png" alt="Tater Tube boot screen">
        <figcaption>The image boots into Tater Tube and keeps SSH available for recovery.</figcaption>
      </figure>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Player Web Setup</span>
        <h2>Configure Pi-side modules from another device.</h2>
        <p>Open <code>http://tatertube.local:24024/setup</code> from a phone or computer on the same network. Pair The Tube to its server first, then configure VoD, Public Access, Tape Deck, Game Center, PC Link, local commercials, and custom VoD channels.</p>
      </div>
      <div class="grid grid-3">
        {simple_card("The Tube", "Enter the server address and short-lived pairing PIN. Tube TV, Stream, Local, server music, guide data, and TaterText then arrive from the server.", ["Server URL", "Pairing PIN", "First Module"])}
        {simple_card("Player Commercials", "Create local commercial categories for Public Access and VoD TV Mode. Tube TV commercials are managed separately by Tater Tube Server.", ["VoD", "Public Access", "No Repeat"])}
        {simple_card("Custom VoD Channels", "Build named TV Mode channels from Plex, Emby, or Jellyfin movies and series. Custom channels appear first and can use a specific commercial category.", ["Movies", "Series", "Categories"])}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Server Web UI</span>
        <h2>Build The Tube from <code>http://SERVER-IP:8080</code>.</h2>
        <p>Use the server UI to pair and name players, add Newznab and NNTP providers, scan local movies, series, and music, configure transcoding, upload Tube TV commercials, create channels, choose logos, and inspect the TV Guide and Activity history.</p>
      </div>
      <div class="grid grid-3">
        {simple_card("1. Add Libraries", "Map folders into Docker, add their container paths under Local Media, and scan metadata.", ["Movies", "Series", "Music"])}
        {simple_card("2. Build Tube TV", "Enable automatic channels or create your own from genres, movies, series, seasons, and episodes.", ["Custom Channels", "Commercials", "Logos"])}
        {simple_card("3. Pair Players", "Create a setup PIN, enter the server URL and PIN on each Pi, and give every box a room name.", ["Short-Lived PIN", "Named Players"])}
      </div>
    </section>
    """
    return page_template(
        "Setup | Tater Tube",
        "Tater Tube setup information for the Steam Deck and Linux one-click installer, Raspberry Pi images, updates, and module configuration.",
        body,
        nav_key="setup",
        depth=1,
    )


def render_api_page() -> str:
    endpoints = """GET  /api/v1/status
POST /api/v1/player/play-pause
POST /api/v1/player/pause
POST /api/v1/player/resume
POST /api/v1/player/stop
POST /api/v1/player/seek          {"position_ms": 60000}
POST /api/v1/player/skip-forward  {"offset_ms": 30000}
POST /api/v1/player/skip-back     {"offset_ms": -10000}
POST /api/v1/player/volume-up
POST /api/v1/player/volume-down
POST /api/v1/player/mute
POST /api/v1/player/key           {"key": "LEFT", "repeat": 1}
POST /api/v1/library/search       {"query": "batman", "types": ["movie", "show", "game"], "limit": 10}
POST /api/v1/library/launch       {"id": "vod:movie:ITEM_ID"}"""
    server_endpoints = """GET  /api/tater/server
POST /api/tater/players/pair
GET  /api/tater/tv/lineup
GET  /api/tater/streams/active"""
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Companion app control</span>
        <h1>API</h1>
        <p>The Pi image exposes a small local HTTP API on port 24024. It is meant for companion apps, remote controls, and future voice-assistant bridges.</p>
      </div>
      {command_box("curl http://tatertube.local:24024/api/v1/status", "Status check")}
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Useful endpoints</span>
        <h2>Player, key, search, and launch calls.</h2>
      </div>
      {command_box(endpoints, "API surface")}
      <p>Set <code>TATER_TUBE_API_TOKEN</code> to require <code>Authorization: Bearer &lt;token&gt;</code> or <code>X-TaterTube-Token: &lt;token&gt;</code>.</p>
    </section>

    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Server API</span>
        <h2>Tater Tube Server exposes player-facing endpoints on port 8080.</h2>
        <p>The player uses the server API for pairing, The Tube catalog, Tube TV lineup and guide data, Newznab discovery, local libraries, resume state, playback activity, stream launch, and local playback URLs.</p>
      </div>
      {command_box(server_endpoints, "Player-facing server API")}
      <div class="grid grid-3">
        {simple_card("Tube TV", "Players request the shared lineup and guide, then tune the scheduled item at its current timeline position.", ["Lineup", "Guide", "Tune"])}
        {simple_card("Library State", "The server supplies local metadata, durations, Continue Watching, next episodes, and playback progress.", ["Local", "Resume", "Duration"])}
        {simple_card("Authorized Players", "Pairing exchanges a short-lived PIN for a revocable player token used by later server requests.", ["PIN", "Token", "Revoke"])}
      </div>
      <div class="action-row">
        {action_link("Server setup", "../server/index.html")}
        {action_link("Server GitHub", SERVER_GITHUB_REPO, secondary=True)}
      </div>
    </section>
    """
    return page_template(
        "API | Tater Tube",
        "Tater Tube player and server APIs for controls, pairing, Tube TV, library state, search, and media launch.",
        body,
        nav_key="api",
        depth=1,
    )


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def convert_inline(text: str, current_depth: int) -> str:
    placeholders: list[str] = []

    def save_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{escape(match.group(1))}</code>")
        return f"\u0000{len(placeholders) - 1}\u0000"

    text = re.sub(r"`([^`]+)`", save_code, text)
    escaped = escape(text)

    def link_replace(match: re.Match[str]) -> str:
        label = match.group(1)
        href = match.group(2)
        wiki_map = {
            "README.md": "readme.html",
            "INSTALL.md": "install.html",
            "BUILDING.md": "building.html",
            "LICENSE": f"{GITHUB_REPO}/blob/main/LICENSE",
        }
        clean_href = href.split("#", 1)[0]
        if clean_href in wiki_map:
            href = wiki_map[clean_href] + (("#" + href.split("#", 1)[1]) if "#" in href else "")
        return f'<a href="{escape(href)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{index}\u0000", value)
    return escaped


def markdown_to_html(markdown: str, *, depth: int = 1) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_code = False
    code_lines: list[str] = []
    table_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{convert_inline(' '.join(paragraph), depth)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal in_list
        if in_list:
            output.append("</ul>")
            in_list = False

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = []
        for raw in table_lines:
            if re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", raw):
                continue
            cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
            rows.append(cells)
        if rows:
            head = rows[0]
            body = rows[1:]
            output.append("<table><thead><tr>" + "".join(f"<th>{convert_inline(cell, depth)}</th>" for cell in head) + "</tr></thead>")
            output.append("<tbody>")
            for row in body:
                output.append("<tr>" + "".join(f"<td>{convert_inline(cell, depth)}</td>" for cell in row) + "</tr>")
            output.append("</tbody></table>")
        table_lines = []

    for line in lines:
        if line.startswith("```"):
            if in_code:
                output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                flush_list()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            flush_paragraph()
            flush_list()
            table_lines.append(line)
            continue
        elif table_lines:
            flush_table()

        if not line.strip():
            flush_paragraph()
            flush_list()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = min(len(heading.group(1)) + 1, 4)
            title = heading.group(2).strip()
            output.append(f'<h{level} id="{slugify(title)}">{convert_inline(title, depth)}</h{level}>')
            continue

        item = re.match(r"^\s*[-*]\s+(.+)$", line)
        if item:
            flush_paragraph()
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{convert_inline(item.group(1), depth)}</li>")
            continue

        paragraph.append(line.strip())

    if in_code:
        output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    flush_paragraph()
    flush_list()
    flush_table()
    return "\n".join(output)


def doc_path(name: str) -> Path:
    content = DOC_CONTENT_DIR / name
    if content.exists():
        return content
    source = SOURCE_DOC_DIR / name
    if source.exists():
        return source
    source_dir = Path(os.getenv("TATER_TUBE_SOURCE_DIR", SOURCE_CACHE_DIR))
    return source_dir / name


def render_wiki_index() -> str:
    cards = "\n".join(
        f"""
        <article class="doc-card">
          <h3>{escape(title)}</h3>
          <p>Generated from the Tater Tube website docs.</p>
          <a class="button button-secondary" href="{escape(slug)}.html">Open doc</a>
        </article>
        """
        for slug, title, source in DOC_SOURCES
    )
    body = f"""
    <section class="section">
      <div class="section-head">
        <span class="eyebrow">Generated docs</span>
        <h1>Docs</h1>
        <p>This wiki section is generated from the Tater Tube source documentation so the website stays aligned with the app repo.</p>
      </div>
      <div class="grid grid-3">
        {cards}
      </div>
    </section>
    """
    return page_template(
        "Docs | Tater Tube",
        "Generated Tater Tube documentation wiki.",
        body,
        nav_key="docs",
        depth=1,
    )


def render_doc_page(slug: str, title: str, source_name: str) -> str:
    source = doc_path(source_name)
    markdown = source.read_text(encoding="utf-8") if source.exists() else f"# {title}\n\nSource file not found: `{source_name}`"
    article = markdown_to_html(markdown, depth=1)
    links = "\n".join(
        f'<a class="{"is-active" if item_slug == slug else ""}" href="{escape(item_slug)}.html">{escape(item_title)}</a>'
        for item_slug, item_title, _ in DOC_SOURCES
    )
    body = f"""
    <section class="section wiki-body">
      <article class="article">
        {article}
      </article>
      <nav class="doc-nav" aria-label="Docs">
        <a href="index.html">Docs home</a>
        {links}
      </nav>
    </section>
    """
    return page_template(
        f"{title} | Tater Tube Docs",
        f"Generated Tater Tube documentation page for {title}.",
        body,
        nav_key="docs",
        depth=1,
    )


def build_site_manifest() -> None:
    manifest = {
        "name": "Tater Tube Website",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo": GITHUB_REPO,
        "pages": [item[2] for item in NAV_ITEMS],
        "docs": [f"wiki/{slug}.html" for slug, _, _ in DOC_SOURCES],
    }
    write_page(PUBLIC_ROOT / "site-manifest.json", json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    ensure_dirs()
    write_page(PUBLIC_ROOT / "index.html", render_home_page())
    write_page(PUBLIC_ROOT / "modules" / "index.html", render_modules_page())
    write_page(PUBLIC_ROOT / "images" / "index.html", render_images_page())
    write_page(PUBLIC_ROOT / "server" / "index.html", render_server_page())
    write_page(PUBLIC_ROOT / "setup" / "index.html", render_setup_page())
    write_page(PUBLIC_ROOT / "api" / "index.html", render_api_page())
    write_page(PUBLIC_ROOT / "wiki" / "index.html", render_wiki_index())
    for slug, title, source in DOC_SOURCES:
        write_page(PUBLIC_ROOT / "wiki" / f"{slug}.html", render_doc_page(slug, title, source))
    build_site_manifest()
    print(f"Built Tater Tube website at {PUBLIC_ROOT}")


if __name__ == "__main__":
    main()
