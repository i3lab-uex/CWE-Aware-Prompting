#!/usr/bin/env python3
"""
Utility to safely build a redirect URL after authentication.

The function ensures that the target URL is either:
* a relative path within the application, or
* an absolute URL whose hostname matches that of `app_base_url`, or
* an absolute URL whose hostname is in the allowed domains list.

If none of these conditions hold, a ValueError is raised to prevent open
redirect vulnerabilities (CWE‑610).
"""

from __future__ import annotations

import sys
from urllib.parse import urlparse, urlunparse, ParseResult
from typing import List

# Example list of allowed external domains.  In a real application this
# should be configured from a secure source (e.g., environment variable,
# configuration file, or secrets manager).
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

def _is_same_origin(base: ParseResult, target: ParseResult) -> bool:
    """Return True if both URLs have the same scheme and hostname."""
    return (
        base.scheme == target.scheme
        and base.hostname == target.hostname
        # Ports are considered part of the origin; if one URL omits a port,
        # it is treated as the default for that scheme.
        and (
            (base.port or _default_port(base.scheme)) ==
            (target.port or _default_port(target.scheme))
        )
    )

def _default_port(scheme: str) -> int | None:
    """Return the default port for a given scheme, or None if unknown."""
    return {"http": 80, "https": 443}.get(scheme.lower())

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g., 'https://app.example.com/login').
    redirect_param : str
        The user-supplied path or URL to redirect to after login.

    Returns
    -------
    str
        A fully qualified, safe URL for redirection.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside base domain and not in allowed domains).
    """
    if not isinstance(app_base_url, str) or not app_base_url:
        raise ValueError("app_base_url must be a non-empty string")

    if not isinstance(redirect_param, str) or not redirect_param:
        raise ValueError("redirect_param must be a non-empty string")

    base_parsed = urlparse(app_base_url)

    # Handle relative redirects (e.g., '/dashboard')
    if not urlparse(redirect_param).scheme:
        # Join the relative path to the base URL
        resolved = urlparse(base_parsed._replace(path=redirect_param).geturl())
    else:
        # Absolute redirect: parse it
        resolved = urlparse(redirect_param)

    # Ensure the scheme is HTTP or HTTPS
    if resolved.scheme not in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme")

    # Check if the target is within the same origin
    if _is_same_origin(base_parsed, resolved):
        return urlunparse(resolved)

    # Check if the hostname is in the list of allowed external domains
    if resolved.hostname and resolved.hostname.lower() in {d.lower() for d in ALLOWED_DOMAINS}:
        return urlunparse(resolved)

    # If none of the above, refuse to redirect
    raise ValueError(f"Unsafe redirect target: {redirect_param}")

# --------------------------------------------------------------------------- #
# Example usage (for manual testing). Remove or comment out in production.
if __name__ == "__main__":
    try:
        base = "https://app.example.com/login"
        for param in [
            "/dashboard",
            "https://app.example.com/profile",
            "http://example.com/home",
            "https://malicious.com/phish",
        ]:
            try:
                print(f"Redirecting to: {build_redirect_link(base, param)}")
            except ValueError as exc:
                print(f"Rejected redirect '{param}': {exc}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)