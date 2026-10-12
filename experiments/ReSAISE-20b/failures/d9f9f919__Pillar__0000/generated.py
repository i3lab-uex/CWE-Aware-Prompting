#!/usr/bin/env python3
"""
Utility for building a safe post‑login redirect URL.

The function validates the user supplied ``redirect_param`` against
the application base URL and a whitelist of allowed external domains.
If the resulting URL is not safe, ``ValueError`` is raised.

CWE‑664: The implementation keeps a strict boundary on the redirect
resource, ensuring that no external or unintended resources are used
throughout its lifetime.
"""

from urllib.parse import urlparse, urlunparse, urljoin
import re

# --------------------------------------------------------------------------- #
# Configuration: list of external domains that are explicitly permitted.
# These should be fully qualified domain names, e.g. "example.com".
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
}

# --------------------------------------------------------------------------- #
def _is_subdomain(base: str, target: str) -> bool:
    """
    Return ``True`` if *target* is a subdomain of *base*.
    Both arguments are expected to be hostnames only, no scheme or port.
    """
    base = base.lower()
    target = target.lower()

    # Direct match or sub‑domain
    return target == base or target.endswith("." + base)


def _normalize_host(host: str) -> str:
    """
    Normalise hostnames by removing trailing dots and converting to
    lower case.  This helps mitigate subtle redirect attacks.
    """
    return host.rstrip(".").lower()


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g. ``https://app.example.com/login``).
    redirect_param : str
        The user supplied path or URL to which the user wishes to be redirected.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe – i.e. it points to a host that is not
        within the application domain and not in ``ALLOWED_DOMAINS``.
    """

    # Parse base URL
    base_parsed = urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect against the base
    # ``urljoin`` handles relative paths correctly.
    joined = urljoin(app_base_url, redirect_param)

    # Parse the resulting URL
    result_parsed = urlparse(joined)

    # Ensure scheme is HTTP/HTTPS (no data:, javascript:, etc.)
    if result_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsafe URL scheme: {result_parsed.scheme}")

    # Normalise hosts
    base_host = _normalize_host(base_parsed.hostname)
    result_host = _normalize_host(result_parsed.hostname)

    # 1. If the redirect is relative (no netloc), it is safe
    if not result_parsed.netloc:
        return joined

    # 2. If the host is a sub‑domain of the base host, it's safe
    if _is_subdomain(base_host, result_host):
        return joined

    # 3. If the host is in ALLOWED_DOMAINS, it's safe
    if result_host in {d.lower() for d in ALLOWED_DOMAINS}:
        return joined

    # 4. Anything else is considered unsafe
    raise ValueError(f"Redirect URL points to unapproved domain: {result_host}")


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple tests
    base = "https://app.example.com/login"

    tests = [
        "/dashboard",
        "https://app.example.com/settings",
        "https://example.com/abc",          # allowed subdomain
        "http://trustedpartner.org/page",
        "https://malicious.com/phish",      # should raise
    ]

    for t in tests:
        try:
            print(f"Input: {t}\n  Result: {build_redirect_link(base, t)}\n")
        except ValueError as e:
            print(f"Input: {t}\n  Error: {e}\n")