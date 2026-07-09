(() => {
  const latestRelease = document.querySelector("[data-latest-release]");
  const navToggle = document.querySelector(".nav-toggle");
  const siteNav = document.querySelector(".site-nav");

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const isOpen = siteNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", (event) => {
      if (!siteNav.classList.contains("is-open")) return;
      const target = event.target;
      if (target instanceof Node && !siteNav.contains(target) && !navToggle.contains(target)) {
        siteNav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  document.querySelectorAll("[data-copy-code]").forEach((button) => {
    button.addEventListener("click", async () => {
      const box = button.closest(".command-box");
      const code = box?.querySelector("code")?.textContent || "";
      if (!code.trim()) return;

      try {
        await navigator.clipboard.writeText(code);
        button.textContent = "Copied";
        window.setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      } catch {
        button.textContent = "Select";
        const codeElement = box?.querySelector("code");
        const selection = window.getSelection();
        if (!codeElement || !selection) return;
        const range = document.createRange();
        range.selectNodeContents(codeElement);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    });
  });

  const imageAssetMatchers = {
    "crt-ntsc": /crt-ntsc\.img\.xz$/i,
    "crt-pal": /crt-pal\.img\.xz$/i,
    "pi5-hdmi-auto": /pi5-hdmi-auto\.img\.xz$/i,
  };

  const formatBytes = (bytes) => {
    if (!Number.isFinite(bytes) || bytes <= 0) return "--";
    const units = ["B", "KB", "MB", "GB"];
    let value = bytes;
    let unit = 0;
    while (value >= 1024 && unit < units.length - 1) {
      value /= 1024;
      unit += 1;
    }
    const digits = value >= 10 || unit === 0 ? 0 : 1;
    return `${value.toFixed(digits)} ${units[unit]}`;
  };

  const formatDate = (value) => {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const setReleaseStatus = (message) => {
    const status = latestRelease?.querySelector("[data-release-status]");
    if (status) status.textContent = message;
  };

  const hydrateImageDownloads = async () => {
    if (!latestRelease) return;

    try {
      const response = await fetch("https://api.github.com/repos/TaterTotterson/Tater-Tube/releases/latest", {
        headers: { Accept: "application/vnd.github+json" },
      });
      if (!response.ok) throw new Error(`GitHub release lookup failed: ${response.status}`);

      const release = await response.json();
      const releaseUrl = release.html_url || "https://github.com/TaterTotterson/Tater-Tube/releases/latest";
      const releaseName = release.name || release.tag_name || "Latest release";
      const releaseDate = formatDate(release.published_at);

      latestRelease.querySelector("[data-release-tag]").textContent = releaseName;
      latestRelease.querySelector("[data-release-link]").href = releaseUrl;
      setReleaseStatus(releaseDate ? `Published ${releaseDate}. Direct image links are ready.` : "Direct image links are ready.");

      document.querySelectorAll("[data-release-card]").forEach((card) => {
        const assetKey = card.getAttribute("data-release-asset");
        const matcher = imageAssetMatchers[assetKey];
        const asset = Array.isArray(release.assets) && matcher
          ? release.assets.find((item) => matcher.test(item.name || ""))
          : null;

        const version = card.querySelector("[data-release-version]");
        const filename = card.querySelector("[data-release-file]");
        const size = card.querySelector("[data-release-size]");
        const downloadLink = card.querySelector("[data-download-link]");
        const releaseLink = card.querySelector("[data-release-card-link]");

        if (version) version.textContent = release.tag_name || "Latest";
        if (releaseLink) releaseLink.href = releaseUrl;

        if (!asset) {
          card.classList.add("is-missing-asset");
          if (filename) filename.textContent = "Open release to download";
          if (size) size.textContent = "--";
          if (downloadLink) {
            downloadLink.href = releaseUrl;
            downloadLink.textContent = "Open latest release";
          }
          return;
        }

        if (filename) filename.textContent = asset.name;
        if (size) size.textContent = formatBytes(asset.size);
        if (downloadLink) {
          downloadLink.href = asset.browser_download_url;
          downloadLink.textContent = "Download image";
        }
      });
    } catch (error) {
      latestRelease.querySelector("[data-release-tag]").textContent = "Latest release";
      setReleaseStatus("GitHub could not be reached. Use the release page link.");
    }
  };

  hydrateImageDownloads();
})();
