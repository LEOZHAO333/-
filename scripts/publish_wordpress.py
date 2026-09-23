#!/usr/bin/env python3
"""Publish generated HTML files to WordPress through the WP REST API."""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required secret: {name}")
    return value


def extract(pattern: str, html: str, fallback: str = "") -> str:
    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    return unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip() if match else fallback


def request_json(url: str, username: str, password: str, method: str = "GET", payload=None):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "Buntou-WordPress-Publisher/1.0",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"WordPress API returned HTTP {exc.code}: {detail[:800]}") from exc


def publish_file(path: Path, site: str, username: str, password: str, status: str):
    raw = path.read_text(encoding="utf-8")
    title = extract(r"<h1[^>]*>(.*?)</h1>", raw, path.stem)
    description = extract(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        raw,
        "",
    )
    body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.IGNORECASE | re.DOTALL)
    content = body_match.group(1).strip() if body_match else raw
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem).strip("-").lower()

    api = site.rstrip("/") + "/wp-json/wp/v2/posts"
    query = api + "?" + urllib.parse.urlencode({"slug": slug, "context": "edit", "per_page": 1})
    existing = request_json(query, username, password)
    payload = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": status,
        "excerpt": description,
    }

    if existing:
        post_id = existing[0]["id"]
        result = request_json(f"{api}/{post_id}", username, password, "POST", payload)
        action = "updated"
    else:
        result = request_json(api, username, password, "POST", payload)
        action = "created"

    print(f"{action}: {path} -> post {result.get('id')} ({result.get('status')})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-list", required=True)
    args = parser.parse_args()

    site = required_env("WP_SITE_URL")
    username = required_env("WP_USERNAME")
    password = required_env("WP_APP_PASSWORD").replace(" ", "")
    status = os.getenv("WP_POST_STATUS", "draft").strip().lower()
    if status not in {"draft", "pending", "private", "publish"}:
        raise SystemExit("WP_POST_STATUS must be draft, pending, private, or publish")

    paths = [Path(line.strip()) for line in Path(args.file_list).read_text().splitlines() if line.strip()]
    if not paths:
        print("No WordPress files selected.")
        return

    failed = False
    for path in paths:
        if not path.is_file() or path.suffix.lower() != ".html" or path.parent.as_posix() != "wordpress":
            print(f"Rejected unsafe or missing path: {path}", file=sys.stderr)
            failed = True
            continue
        try:
            publish_file(path, site, username, password, status)
        except Exception as exc:
            print(f"Failed: {path}: {exc}", file=sys.stderr)
            failed = True
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
