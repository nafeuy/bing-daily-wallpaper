#!/usr/bin/env python3
"""Build the static GitHub Pages site with today's Bing UHD wallpaper."""

from __future__ import annotations

import json
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


BING_ORIGIN = "https://www.bing.com"
BING_API = (
    f"{BING_ORIGIN}/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
)
OUTPUT_DIR = Path("_site")
IMAGE_NAME = "bing-daily-uhd.jpg"
USER_AGENT = "bing-daily-wallpaper/1.0 (+https://github.com/nafeuy/bing-daily-wallpaper)"


def fetch(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), response.headers.get_content_type()


def main() -> None:
    metadata_bytes, content_type = fetch(BING_API)
    if content_type != "application/json":
        raise RuntimeError(f"Unexpected Bing API content type: {content_type}")

    payload = json.loads(metadata_bytes)
    if not payload.get("images"):
        raise RuntimeError("Bing API returned no images")

    image = payload["images"][0]
    url_base = image.get("urlbase")
    if not isinstance(url_base, str) or not url_base.startswith("/th?id=OHR."):
        raise RuntimeError(f"Unexpected Bing urlbase: {url_base!r}")

    upstream_url = f"{BING_ORIGIN}{url_base}_UHD.jpg"
    image_bytes, image_type = fetch(upstream_url)
    if image_type != "image/jpeg" or not image_bytes.startswith(b"\xff\xd8\xff"):
        raise RuntimeError(f"Unexpected image response: {image_type}")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    shutil.copy2("web/index.html", OUTPUT_DIR / "index.html")
    (OUTPUT_DIR / ".nojekyll").touch()
    (OUTPUT_DIR / IMAGE_NAME).write_bytes(image_bytes)

    info = {
        "date": image.get("enddate") or image.get("startdate"),
        "title": image.get("title"),
        "copyright": image.get("copyright"),
        "copyright_link": image.get("copyrightlink"),
        "image": IMAGE_NAME,
        "upstream_url": upstream_url,
        "market": "zh-CN",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (OUTPUT_DIR / "info.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Built {OUTPUT_DIR / IMAGE_NAME} ({len(image_bytes):,} bytes)")
    print(f"Bing UHD source: {upstream_url}")


if __name__ == "__main__":
    main()
