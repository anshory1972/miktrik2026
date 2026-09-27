#!/usr/bin/env python3
"""
Finish the forum setup after the Telegram channel exists.

You create the channel and the linked discussion group in the Telegram app.
This script then checks that they are wired correctly and writes the result
into assets/config.js, so you never edit the file by hand.

It uses nothing but public t.me pages. No bot token, no API key, no login.

Usage
-----
Check a channel is public and has comments switched on:

    python tools/setup_forum.py --channel miktrik2026 --check

Set the channel and point threads at their posts:

    python tools/setup_forum.py --channel miktrik2026 \
        --thread umum=7 --thread lpm-logit-probit=9 \
        --group-link https://t.me/+AbCdEf123

Post numbers come from the end of a post's link:
    https://t.me/miktrik2026/7   ->   7
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "assets" / "config.js"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) forum-setup/1.0"


# ----------------------------------------------------------------- fetching


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def channel_is_public(channel: str) -> tuple[bool, str]:
    """A public channel renders a preview page at t.me/s/<name>."""
    try:
        html = fetch(f"https://t.me/s/{channel}")
    except urllib.error.HTTPError as e:
        return False, f"t.me returned HTTP {e.code}"
    except Exception as e:                                    # noqa: BLE001
        return False, f"could not reach t.me: {e}"

    if "tgme_channel_info" in html or "tgme_widget_message" in html:
        m = re.search(r'<meta property="og:title" content="([^"]*)"', html)
        return True, m.group(1) if m else channel
    if "tgme_page_context_link" in html or "Preview channel" in html:
        return True, channel
    return False, "no channel preview found, so it is not public yet"


def post_has_comments(channel: str, post: int) -> tuple[bool, str]:
    """The discussion widget only has something to show when the post
    carries a Comments button, which requires a linked discussion group."""
    url = f"https://t.me/{channel}/{post}?embed=1&discussion=1"
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        return False, f"post unreachable, HTTP {e.code}"
    except Exception as e:                                    # noqa: BLE001
        return False, f"post unreachable: {e}"

    if re.search(r"tgme_widget_message_(comments|footer)", html) or "Comments" in html:
        return True, "comments thread reachable"
    if "tgme_widget_message" in html:
        return False, "post exists but has no Comments button, so no group is linked"
    return False, "post not found"


# ------------------------------------------------------------ config wiring


def read_config() -> str:
    if not CONFIG.exists():
        sys.exit(f"config not found: {CONFIG}")
    return CONFIG.read_text(encoding="utf-8")


def set_channel(src: str, channel: str) -> str:
    new, n = re.subn(r'(\bchannel:\s*)"[^"]*"', rf'\g<1>"{channel}"', src, count=1)
    if n != 1:
        sys.exit("could not find the `channel:` line in assets/config.js")
    return new


def set_group_link(src: str, link: str) -> str:
    new, n = re.subn(r'(\bgroupLink:\s*)"[^"]*"', rf'\g<1>"{link}"', src, count=1)
    if n != 1:
        sys.exit("could not find the `groupLink:` line in assets/config.js")
    return new


def set_post(src: str, slug: str, post: int) -> str:
    """Set `post:` inside the thread object carrying this slug. The slug may
    sit before or after the post field, so match the whole object."""
    pattern = re.compile(
        r"\{[^{}]*?\bslug:\s*[\"']" + re.escape(slug) + r"[\"'][^{}]*?\}", re.S)
    m = pattern.search(src)
    if not m:
        sys.exit(f"no thread with slug '{slug}' in assets/config.js")
    block = m.group(0)
    new_block, n = re.subn(r"(\bpost:\s*)(null|\d+)", rf"\g<1>{post}", block, count=1)
    if n != 1:
        sys.exit(f"thread '{slug}' has no `post:` field")
    return src[:m.start()] + new_block + src[m.end():]


def known_slugs(src: str) -> list[str]:
    return re.findall(r"\bslug:\s*[\"']([^\"']+)[\"']", src)


# ------------------------------------------------------------------- driver


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verify the Telegram side and write assets/config.js.")
    ap.add_argument("--channel", required=True,
                    help="public channel username, without the @")
    ap.add_argument("--thread", action="append", default=[], metavar="SLUG=POST",
                    help="point a thread slug at a channel post number")
    ap.add_argument("--group-link", default=None,
                    help="invite link of the discussion group")
    ap.add_argument("--check", action="store_true",
                    help="verify only, write nothing")
    args = ap.parse_args()

    channel = args.channel.lstrip("@").strip()
    src = read_config()
    problems = 0

    print(f"Channel @{channel}")
    ok, detail = channel_is_public(channel)
    print(f"  public channel        {'OK  ' if ok else 'FAIL'}  {detail}")
    if not ok:
        problems += 1

    pairs: list[tuple[str, int]] = []
    for item in args.thread:
        if "=" not in item:
            sys.exit(f"--thread needs SLUG=POST, got: {item}")
        slug, _, num = item.partition("=")
        slug = slug.strip()
        if not num.strip().isdigit():
            sys.exit(f"post number must be an integer, got: {num!r}")
        pairs.append((slug, int(num)))

    slugs = known_slugs(src)
    for slug, post in pairs:
        if slug not in slugs:
            print(f"  thread '{slug}'       FAIL  not in config.js "
                  f"(known: {', '.join(slugs)})")
            problems += 1
            continue
        ok, detail = post_has_comments(channel, post)
        print(f"  post {post} -> {slug:<18} {'OK  ' if ok else 'FAIL'}  {detail}")
        if not ok:
            problems += 1

    if args.check:
        print("\nCheck only, nothing written.")
        return 1 if problems else 0

    if problems:
        print(f"\n{problems} problem(s) found. Nothing written.")
        print("Fix the Telegram side first, then run again.")
        return 1

    out = set_channel(src, channel)
    if args.group_link:
        out = set_group_link(out, args.group_link)
    for slug, post in pairs:
        out = set_post(out, slug, post)
    CONFIG.write_text(out, encoding="utf-8")

    print(f"\nWrote {CONFIG.relative_to(ROOT)}")
    print("Now publish it:")
    print("  git add -A && git commit -m \"Activate forum threads\" && git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
