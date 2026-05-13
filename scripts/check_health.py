#!/usr/bin/env python3
"""Fast preflight checks for the local Checkee updater."""

from __future__ import annotations

import argparse
import socket
import sys
import tempfile
from contextlib import closing


def ok(name: str, detail: str) -> None:
    print(f"OK   {name}: {detail}")


def fail(name: str, detail: str) -> None:
    print(f"FAIL {name}: {detail}")


def check_dns(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        fail(f"dns {host}", str(exc))
        return False
    addrs = sorted({item[4][0] for item in infos})
    ok(f"dns {host}", ", ".join(addrs[:3]))
    return True


def check_https(url: str) -> bool:
    try:
        import requests

        response = requests.get(url, timeout=8)
    except Exception as exc:
        fail(f"https {url}", str(exc))
        return False
    if response.status_code >= 500:
        fail(f"https {url}", f"HTTP {response.status_code}")
        return False
    ok(f"https {url}", f"HTTP {response.status_code}")
    return True


def check_port_bind(host: str) -> bool:
    family = socket.AF_INET6 if ":" in host else socket.AF_INET
    try:
        with closing(socket.socket(family, socket.SOCK_STREAM)) as sock:
            sock.bind((host, 0))
            port = sock.getsockname()[1]
    except OSError as exc:
        fail(f"local port {host}", str(exc))
        return False
    ok(f"local port {host}", f"free port {port}")
    return True


def check_selenium_start() -> bool:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except Exception as exc:
        fail("selenium import", str(exc))
        return False

    with tempfile.TemporaryDirectory(prefix="checkee-health-chrome-") as profile:
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument(f"--user-data-dir={profile}")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        try:
            driver = webdriver.Chrome(options=opts)
            driver.set_page_load_timeout(8)
            driver.get("about:blank")
            driver.quit()
        except Exception as exc:
            fail("selenium chrome", str(exc).splitlines()[0])
            return False
    ok("selenium chrome", "started and closed")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-selenium", action="store_true")
    args = parser.parse_args()

    checks = [
        check_dns("www.checkee.info"),
        check_dns("github.com"),
        check_https("https://www.checkee.info/"),
        check_port_bind("127.0.0.1"),
    ]
    try:
        checks.append(check_port_bind("::1"))
    except OSError:
        pass
    if not args.skip_selenium:
        checks.append(check_selenium_start())

    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
