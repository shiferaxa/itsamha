#!/usr/bin/env python3
"""Fetch badges from Credly and generate website/certifications.json.

Credly exposes public profile badges at
https://www.credly.com/users/<username>/badges.json (no auth required, but it
blocks browser CORS — so we fetch at build time and bake the result into the
site). Badges with type_category == "Certification" are featured; everything
else (Learning/Validation badges) goes into a secondary list. Certs that don't
live on Credly (e.g. Microsoft Learn) are merged in from data/extra-certs.json.

Usage: python scripts/fetch_certifications.py
"""

import json
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

CREDLY_USER = "amha-shiferaw"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "website" / "certifications.json"
EXTRA = REPO_ROOT / "data" / "extra-certs.json"


def fetch_credly_badges():
    badges = []
    page = 1
    while True:
        url = f"https://www.credly.com/users/{CREDLY_USER}/badges.json?page={page}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "itsamha.com build (github.com/shiferaxa/itsamha)",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
        data = payload.get("data", [])
        badges.extend(data)
        meta = payload.get("metadata") or {}
        total_pages = meta.get("total_pages") or 1
        if page >= total_pages or not data:
            return badges
        page += 1


def sized_image(image_url, size=220):
    # images.credly.com supports on-the-fly resizing via a /size/WxH/ prefix
    prefix = "https://images.credly.com/"
    if image_url and image_url.startswith(prefix):
        return f"{prefix}size/{size}x{size}/{image_url[len(prefix):]}"
    return image_url


# Credly issuer names are sometimes the certification *program* rather than the
# brand people recognize — normalize the display name.
ISSUER_OVERRIDES = {
    "Amazon Web Services Training and Certification": "Amazon Web Services",
}


def simplify(badge):
    template = badge.get("badge_template", {})
    issuer = ""
    try:
        issuer = badge["issuer"]["entities"][0]["entity"]["name"]
    except (KeyError, IndexError, TypeError):
        issuer = template.get("issuer", {}).get("name", "") if isinstance(template.get("issuer"), dict) else ""
    name = template.get("name", "")
    if name.startswith("HashiCorp"):
        # issued through the IBM certification program on Credly, but it's a HashiCorp cert
        issuer = "HashiCorp"
    else:
        issuer = ISSUER_OVERRIDES.get(issuer, issuer)
    return {
        "name": template.get("name", "Unknown"),
        "issuer": issuer,
        "date": badge.get("issued_at_date", ""),
        "image": sized_image(badge.get("image_url", "")),
        "url": f"https://www.credly.com/badges/{badge['id']}/public_url",
    }


def main():
    try:
        raw = fetch_credly_badges()
    except Exception as exc:
        print(f"ERROR: could not fetch Credly badges: {exc}", file=sys.stderr)
        # Keep the previously generated file rather than shipping an empty one
        if OUTPUT.exists():
            print("Keeping existing certifications.json", file=sys.stderr)
            return 0
        return 1

    featured, other = [], []
    for badge in raw:
        category = badge.get("badge_template", {}).get("type_category")
        (featured if category == "Certification" else other).append(simplify(badge))

    if EXTRA.exists():
        extras = json.loads(EXTRA.read_text(encoding="utf-8"))
        featured.extend(extras.get("featured", []))
        other.extend(extras.get("badges", []))

    def sort_key(cert):
        try:
            return date.fromisoformat(cert["date"])
        except (ValueError, KeyError):
            return date.min

    featured.sort(key=sort_key, reverse=True)
    other.sort(key=sort_key, reverse=True)

    OUTPUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": f"https://www.credly.com/users/{CREDLY_USER}",
        "featured": featured,
        "badges": other,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}: {len(featured)} certifications, {len(other)} badges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
