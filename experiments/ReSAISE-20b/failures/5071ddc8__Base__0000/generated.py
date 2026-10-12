#!/usr/bin/env python3
"""
Utility to safely assemble a redirect URL after login.

The function validates that the user supplied ``next_route`` is either:
* a relative URL path (e.g. "/dashboard")
* an absolute URL whose host matches the base application domain, or
* an absolute URL to a domain listed in ``ALLOWED_DOMAINS``.

If the supplied target does not meet these criteria, a ValueError is raised
to prevent open‑redirect attacks (CWE‑601).
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Pre‑approved external domains for redirection.
ALLOWED_DOMAINS: List[str] = [
    "trusted.com",
    "partner.example.org",
]

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URI.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_route : str
        The user supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If ``next_route`` resolves to an unsafe or disallowed URL.
    """
    # Resolve the next route relative to the base
    resolved = urljoin(main_base_url, next_route)

    parsed_main = urlparse(main_base_url)
    parsed_resolved = urlparse(resolved)

    # Helper to normalize hostnames (lowercase, strip port)
    def _host_without_port(hostport: str) -> str:
        host = hostport.split(":")[0].lower()
        return host

    main_host = _host_without_port(parsed_main.netloc)
    resolved_host = _host_without_port(parsed_resolved.netloc)

    # Case 1: relative URL (no netloc)
    if not parsed_resolved.netloc:
        return resolved

    # Case 2: same domain as the application
    if resolved_host == main_host:
        return resolved

    # Case 3: external domain but allowed
    if resolved_host in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved

    # If we reach here, the URL is unsafe
    raise ValueError(
        f"Unsafe redirect target: {resolved!r} (host={resolved_host})"
    )

# Example usage (uncomment to test)
if __name__ == "__main__":
    base = "https://app.example.com"
    tests = [
        "/profile",
        "https://app.example.com/settings",
        "http://trusted.com/welcome",
        "https://malicious.com/phish",
    ]
    for t in tests:
        try:
            print(assemble_redirect_uri(base, t))
        except ValueError as e:
            print(f"Rejected: {t} -> {e}")