#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

RULE_SOURCES = [
    {
        "name": "direct-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt",
        "output": "direct-list.txt",
    },
    {
        "name": "cn-apple-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/apple-cn.txt",
        "output": "cn-apple-list.txt",
    },
    {
        "name": "cn-google-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/google-cn.txt",
        "output": "cn-google-list.txt",
    },
    {
        "name": "cn-cdn-list",
        "url": "https://raw.githubusercontent.com/pmkol/easymosdns/main/rules/cdn_domain_list.txt",
        "output": "cn-cdn-list.txt",
    },
    {
        "name": "proxy-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/proxy-list.txt",
        "output": "proxy-list.txt",
    },
    {
        "name": "gfw-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/gfw.txt",
        "output": "gfw-list.txt",
    },
    {
        "name": "reject-list",
        "url": "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/reject-list.txt",
        "output": "reject-list.txt",
    },
]

DIST_DIR = Path("dist")
DIST_DIR.mkdir(parents=True, exist_ok=True)


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": "smartdns-rules-builder/1.0"})
    with urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def normalize_line(line: str) -> str | None:
    line = line.strip()
    if not line:
        return None
    if line.startswith("regexp:"):
        return None
    if line.startswith("full:"):
        return "-." + line[len("full:"):]
    if line.startswith("domain:"):
        return line[len("domain:"):]
    return line


def process_text(text: str) -> list[str]:
    items = set()
    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if line:
            items.add(line)
    return sorted(items)


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }

    for item in RULE_SOURCES:
        print(f"Processing: {item['name']} <- {item['url']}")
        raw_text = fetch_text(item["url"])
        lines = process_text(raw_text)
        output_text = "\n".join(lines) + "\n"

        output_path = DIST_DIR / item["output"]
        output_path.write_text(output_text, encoding="utf-8")

        manifest["files"].append(
            {
                "name": item["name"],
                "source_url": item["url"],
                "output": f"dist/{item['output']}",
                "line_count": len(lines),
                "sha256": sha256_of_text(output_text),
            }
        )

    (DIST_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Done.")


if __name__ == "__main__":
    main()