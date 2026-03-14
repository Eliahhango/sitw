#!/usr/bin/env python3
"""
Simple website downloader for testing your own site.

Usage:
  python site_downloader.py https://www.elitechwiz.site -o downloaded_site --max-pages 2000 --delay 0.1 --include-related-hosts
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import pathlib
import posixpath
import re
import time
import xml.etree.ElementTree as ET
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ASSET_ATTRS = {
    "img": ["src", "srcset"],
    "script": ["src"],
    "source": ["src", "srcset"],
    "video": ["src", "poster"],
    "audio": ["src"],
    "iframe": ["src"],
}

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")
TRACKING_QUERY_PREFIXES = ("utm_", "fbclid", "gclid", "mc_")
TEXT_ASSET_EXTENSIONS = (
    "js",
    "css",
    "json",
    "map",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "svg",
    "webp",
    "ico",
    "woff",
    "woff2",
    "ttf",
    "eot",
    "mp4",
    "webm",
    "mp3",
    "wav",
)

TEXT_ASSET_URL_RE = re.compile(
    r"""(?P<url>
    (?:https?:)?//[^\s"'`()<>]+
    |
    (?:/|\.{1,2}/|static/)[A-Za-z0-9_\-./]+?\.(?:"""
    + "|".join(TEXT_ASSET_EXTENSIONS)
    + r""")
    (?:\?[A-Za-z0-9_=%&.\-]+)?
    )""",
    re.IGNORECASE | re.VERBOSE,
)


def normalize_url(raw_url: str) -> str:
    clean, _frag = urldefrag(raw_url)
    return clean.strip()


def is_http(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in ("http", "https")


def normalize_netloc(parsed) -> str:
    host = parsed.netloc.lower()
    if host.endswith(":80") and parsed.scheme == "http":
        host = host[:-3]
    elif host.endswith(":443") and parsed.scheme == "https":
        host = host[:-4]
    return host


def simplify_path(path: str) -> str:
    if not path:
        return "/"
    normalized = posixpath.normpath(path)
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    return normalized


def drop_tracking_query(query: str) -> str:
    if not query:
        return ""
    kept = []
    for part in query.split("&"):
        key = part.split("=", 1)[0].lower()
        if any(key.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES):
            continue
        kept.append(part)
    return "&".join(kept)


def canonicalize_url(raw_url: str, keep_query: bool) -> str:
    raw_url = normalize_url(raw_url)
    p = urlparse(raw_url)
    scheme = p.scheme.lower()
    if not scheme or not p.netloc:
        return raw_url
    netloc = normalize_netloc(p)
    path = simplify_path(p.path)
    query = drop_tracking_query(p.query) if keep_query else ""
    return f"{scheme}://{netloc}{path}" + (f"?{query}" if query else "")


def root_domain(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


def in_scope(url: str, root_host: str, include_related_hosts: bool, allow_external_pages: bool) -> bool:
    if allow_external_pages:
        return is_http(url)
    host = normalize_netloc(urlparse(url))
    if not host:
        return False
    if host == root_host or host == f"www.{root_host}" or root_host == f"www.{host}":
        return True
    if include_related_hosts:
        return root_domain(host) == root_domain(root_host)
    return False


def normalize_srcset(srcset: str) -> Iterable[str]:
    for part in srcset.split(","):
        candidate = part.strip().split(" ")[0]
        if candidate:
            yield candidate


def shorten_component(component: str, max_len: int = 120) -> str:
    if len(component) <= max_len:
        return component
    digest = hashlib.sha1(component.encode("utf-8", errors="ignore")).hexdigest()[:12]
    keep = max_len - 15
    return f"{component[:keep]}_{digest}"


def to_local_path(url: str, output_dir: pathlib.Path) -> pathlib.Path:
    p = urlparse(url)
    netloc = normalize_netloc(p)
    path = p.path or "/"

    if path.endswith("/"):
        path = path + "index.html"

    filename = posixpath.basename(path)
    if "." not in filename:
        path = path + "/index.html"

    safe_path = re.sub(r"[<>:\\|?*]", "_", path.lstrip("/"))
    safe_parts = [shorten_component(part) for part in safe_path.split("/") if part]
    safe_path = "/".join(safe_parts) if safe_parts else "index.html"
    local_path = output_dir / netloc / safe_path

    if len(str(local_path)) > 240:
        digest = hashlib.sha1(str(local_path).encode("utf-8", errors="ignore")).hexdigest()[:16]
        stem = shorten_component(local_path.stem, max_len=48)
        local_path = local_path.with_name(f"{stem}_{digest}{local_path.suffix}")

    return local_path


def save_content(resp: requests.Response, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(resp.content)


def is_cloudflare_challenge(resp: requests.Response) -> bool:
    server = (resp.headers.get("Server") or "").lower()
    if "cloudflare" not in server:
        return False
    body = resp.text.lower()
    return "challenge-platform" in body or "just a moment" in body


def log(message: str) -> None:
    try:
        print(message)
    except OSError:
        fallback = message.encode("ascii", errors="backslashreplace").decode("ascii")
        print(fallback)


def extract_asset_links(soup: BeautifulSoup, base_url: str) -> set[str]:
    assets: set[str] = set()
    for tag, attrs in ASSET_ATTRS.items():
        for node in soup.find_all(tag):
            for attr in attrs:
                value = node.get(attr)
                if not value:
                    continue
                if attr == "srcset":
                    for u in normalize_srcset(value):
                        assets.add(urljoin(base_url, u))
                else:
                    assets.add(urljoin(base_url, value))

    allowed_link_rels = {
        "stylesheet",
        "icon",
        "shortcut",
        "manifest",
        "preload",
        "modulepreload",
        "prefetch",
    }
    for node in soup.find_all("link", href=True):
        rel_tokens = {token.lower() for token in (node.get("rel") or [])}
        if not rel_tokens:
            continue
        if rel_tokens.intersection(allowed_link_rels):
            assets.add(urljoin(base_url, node["href"]))

    return assets


def extract_page_links(soup: BeautifulSoup, base_url: str) -> set[str]:
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(SKIP_SCHEMES):
            continue
        links.add(urljoin(base_url, href))

    for form in soup.find_all("form", action=True):
        action = form["action"].strip()
        if action and not action.startswith(SKIP_SCHEMES):
            links.add(urljoin(base_url, action))

    return links


def is_text_asset(content_type: str, url: str) -> bool:
    ctype = (content_type or "").lower()
    if any(token in ctype for token in ("javascript", "ecmascript", "css", "json", "text/plain")):
        return True
    path = urlparse(url).path.lower()
    return path.endswith((".js", ".css", ".json", ".map"))


def extract_text_asset_links(text: str, base_url: str) -> set[str]:
    found: set[str] = set()

    for m in TEXT_ASSET_URL_RE.finditer(text):
        candidate = m.group("url").strip()
        if not candidate:
            continue
        if candidate.startswith("static/"):
            candidate = "/" + candidate
        if candidate.startswith("//"):
            candidate = "https:" + candidate
        try:
            resolved = urljoin(base_url, candidate)
        except ValueError:
            continue
        found.add(resolved)

    return found


def parse_sitemap_xml(xml_text: str) -> set[str]:
    found: set[str] = set()
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return found
    for elem in root.iter():
        if elem.tag.endswith("loc") and elem.text:
            found.add(elem.text.strip())
    return found


def discover_sitemaps(start_url: str, session: requests.Session, timeout: int) -> set[str]:
    p = urlparse(start_url)
    base = f"{p.scheme}://{normalize_netloc(p)}"
    candidates = {
        f"{base}/sitemap.xml",
        f"{base}/sitemap_index.xml",
    }
    robots_url = f"{base}/robots.txt"

    try:
        resp = session.get(robots_url, timeout=timeout)
        if resp.ok:
            for line in resp.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    sitemap_url = line.split(":", 1)[1].strip()
                    if sitemap_url:
                        candidates.add(sitemap_url)
    except requests.RequestException:
        pass

    return candidates


def collect_urls_from_sitemaps(
    sitemap_urls: set[str],
    session: requests.Session,
    timeout: int,
    root_host: str,
    include_related_hosts: bool,
    allow_external_pages: bool,
) -> set[str]:
    pending = collections.deque(sorted(sitemap_urls))
    visited: set[str] = set()
    page_urls: set[str] = set()
    max_sitemap_docs = 100

    while pending and len(visited) < max_sitemap_docs:
        sitemap_url = pending.popleft()
        sitemap_url = canonicalize_url(sitemap_url, keep_query=False)

        if sitemap_url in visited or not is_http(sitemap_url):
            continue

        visited.add(sitemap_url)

        try:
            resp = session.get(sitemap_url, timeout=timeout)
        except requests.RequestException:
            continue

        if not resp.ok:
            continue

        found = parse_sitemap_xml(resp.text)

        for u in found:
            cu = canonicalize_url(u, keep_query=False)
            if not cu:
                continue
            if cu.endswith(".xml") and "sitemap" in cu:
                if cu not in visited:
                    pending.append(cu)
            elif in_scope(cu, root_host, include_related_hosts, allow_external_pages):
                page_urls.add(cu)

    return page_urls


def download_site(
    start_url: str,
    output_dir: pathlib.Path,
    max_pages: int,
    delay: float,
    timeout: int,
    user_agent: str,
    include_related_hosts: bool,
    keep_query_pages: bool,
    allow_external_pages: bool,
) -> None:
    start_url = canonicalize_url(start_url, keep_query=keep_query_pages)
    parsed_start = urlparse(start_url)

    if not is_http(start_url):
        raise ValueError("Start URL must be HTTP/HTTPS.")

    root_host = normalize_netloc(parsed_start)
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})

    queue = collections.deque([start_url])
    queued: set[str] = {start_url}
    asset_queue: collections.deque[str] = collections.deque()
    asset_queued: set[str] = set()
    seen_pages: set[str] = set()
    downloaded_assets: set[str] = set()

    sitemap_urls = discover_sitemaps(start_url, session, timeout)
    seeded_pages = collect_urls_from_sitemaps(
        sitemap_urls=sitemap_urls,
        session=session,
        timeout=timeout,
        root_host=root_host,
        include_related_hosts=include_related_hosts,
        allow_external_pages=allow_external_pages,
    )

    for page in sorted(seeded_pages):
        if page not in queued:
            queue.append(page)
            queued.add(page)

    while queue and len(seen_pages) < max_pages:
        url = queue.popleft()
        url = canonicalize_url(url, keep_query=keep_query_pages)

        if not url or url in seen_pages:
            continue

        if not is_http(url) or not in_scope(url, root_host, include_related_hosts, allow_external_pages):
            continue

        try:
            resp = session.get(url, timeout=timeout)
        except requests.RequestException as exc:
            log(f"[WARN] Failed page {url}: {exc}")
            continue

        if is_cloudflare_challenge(resp):
            log(f"[WARN] Cloudflare challenge detected at {url}. Automated crawling is blocked for this host.")
            seen_pages.add(url)
            continue

        ct = resp.headers.get("Content-Type", "")
        if "text/html" not in ct:
            if url not in downloaded_assets:
                path = to_local_path(url, output_dir)
                save_content(resp, path)
                downloaded_assets.add(url)
                log(f"[ASSET] {url} -> {path}")
            continue

        seen_pages.add(url)
        page_path = to_local_path(url, output_dir)
        save_content(resp, page_path)
        log(f"[PAGE] {url} -> {page_path}")

        soup = BeautifulSoup(resp.text, "html.parser")

        for link in extract_page_links(soup, url):
            link = canonicalize_url(link, keep_query=keep_query_pages)
            if (
                link
                and in_scope(link, root_host, include_related_hosts, allow_external_pages)
                and link not in seen_pages
                and link not in queued
            ):
                queue.append(link)
                queued.add(link)

        for asset_url in extract_asset_links(soup, url):
            asset_url = canonicalize_url(asset_url, keep_query=True)
            if (
                asset_url
                and is_http(asset_url)
                and in_scope(asset_url, root_host, include_related_hosts, allow_external_pages)
                and asset_url not in downloaded_assets
                and asset_url not in asset_queued
            ):
                asset_queue.append(asset_url)
                asset_queued.add(asset_url)

        while asset_queue:
            asset_url = asset_queue.popleft()

            if asset_url in downloaded_assets:
                continue

            try:
                asset_resp = session.get(asset_url, timeout=timeout)
                asset_ct = asset_resp.headers.get("Content-Type", "")

                if "text/html" in asset_ct:
                    page_candidate = canonicalize_url(asset_url, keep_query=keep_query_pages)
                    if (
                        page_candidate
                        and page_candidate not in seen_pages
                        and page_candidate not in queued
                        and in_scope(page_candidate, root_host, include_related_hosts, allow_external_pages)
                    ):
                        queue.append(page_candidate)
                        queued.add(page_candidate)
                    continue

                asset_path = to_local_path(asset_url, output_dir)
                save_content(asset_resp, asset_path)
                downloaded_assets.add(asset_url)
                log(f"[ASSET] {asset_url} -> {asset_path}")

                if is_text_asset(asset_ct, asset_url):
                    try:
                        text_refs = extract_text_asset_links(asset_resp.text, asset_url)
                    except UnicodeDecodeError:
                        text_refs = set()

                    for discovered in text_refs:
                        discovered = canonicalize_url(discovered, keep_query=True)
                        if (
                            discovered
                            and is_http(discovered)
                            and in_scope(discovered, root_host, include_related_hosts, allow_external_pages)
                            and discovered not in downloaded_assets
                            and discovered not in asset_queued
                        ):
                            asset_queue.append(discovered)
                            asset_queued.add(discovered)
            except requests.RequestException as exc:
                log(f"[WARN] Failed asset {asset_url}: {exc}")

        if delay > 0:
            time.sleep(delay)

    log("\nDone.")
    log(f"Pages downloaded: {len(seen_pages)}")
    log(f"Assets downloaded: {len(downloaded_assets)}")
    log(f"Saved to: {output_dir.resolve()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download pages and assets from a website you own or are authorized to test.")
    parser.add_argument("url", help="Start URL, e.g. https://www.elitechwiz.site")
    parser.add_argument("-o", "--output", default="downloaded_site", help="Output directory (default: downloaded_site)")
    parser.add_argument("--max-pages", type=int, default=2000, help="Maximum HTML pages to crawl (default: 2000)")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between page requests in seconds (default: 0.1)")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout seconds (default: 20)")
    parser.add_argument(
        "--include-related-hosts",
        action="store_true",
        help="Also crawl hosts under the same root domain (e.g. preview.example.com + www.example.com).",
    )
    parser.add_argument(
        "--keep-query-pages",
        action="store_true",
        help="Treat query-string page URLs as unique pages. Off by default to avoid duplicate crawl loops.",
    )
    parser.add_argument(
        "--allow-external-pages",
        action="store_true",
        help="Allow crawling pages/assets on other hosts discovered from the start page (use carefully).",
    )
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (compatible; SiteDownloader/1.0)",
        help="User-Agent string",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_site(
        start_url=args.url,
        output_dir=pathlib.Path(args.output),
        max_pages=args.max_pages,
        delay=args.delay,
        timeout=args.timeout,
        user_agent=args.user_agent,
        include_related_hosts=args.include_related_hosts,
        keep_query_pages=args.keep_query_pages,
        allow_external_pages=args.allow_external_pages,
    )


if __name__ == "__main__":
    main()
