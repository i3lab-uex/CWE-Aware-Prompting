#!/usr/bin/env python3
"""
Utility to build a safe redirect URL after login.

The function ensures that the user supplied `redirect_param` is either
a relative path within the application or an absolute URL that belongs to
one of the approved external domains.  Any other value results in a
`ValueError`.
"""

from urllib.parse import urlparse, urljoin

# Pre‑approved external domains for redirects
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g. "https://app.example.com/").
    redirect_param : str
        The URL path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside of the base domain and not in
        `ALLOWED_DOMAINS`).
    """
    if not isinstance(app_base_url, str) or not isinstance(redirect_param, str):
        raise TypeError("Both arguments must be strings")

    # Parse the base URL once
    base_parsed = urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect against the base
    resolved = urljoin(app_base_url, redirect_param)
    parsed_resolved = urlparse(resolved)

    # If the path is relative (no netloc), it's safe
    if not parsed_resolved.netloc:
        # Ensure it is still under the same domain
        return resolved

    # Absolute URL: check that its domain is allowed
    host = parsed_resolved.hostname or ""
    if host == base_parsed.hostname:
        # Same domain as the app
        return resolved

    if host.split(".")[-2:] == base_parsed.hostname.split("."):
        # Same top‑level domain (e.g. sub.example.com)
        return resolved

    if host in ALLOWED_DOMAINS:
        return resolved

    raise ValueError(f"Unsafe redirect URL: {resolved}")


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    base = "https://app.example.com/"
    for param in [
        "/dashboard",
        "profile/edit",
        "https://app.example.com/settings",
        "http://malicious.com/phish",
        "https://trustedpartner.org/landing",
    ]:
        try:
            print(build_redirect_link(base, param))
        except ValueError as exc:
            print(f"Rejected: {exc}")