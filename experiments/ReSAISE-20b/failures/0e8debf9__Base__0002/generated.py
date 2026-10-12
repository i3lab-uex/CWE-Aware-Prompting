#!/usr/bin/env python3
"""
Secure redirect URI generator.

This module provides a single helper function, `generate_redirect_uri`,
which validates a user supplied redirect target against the
application’s base URL and an allow‑list of external domains.
It mitigates CWE‑601 (Open Redirect) by ensuring that only
safe destinations are returned.
"""

from urllib.parse import urlparse, urljoin, urlunparse

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of external domains that are explicitly permitted for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after authentication.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    post_login_param : str
        The user‑supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the application domain and not in
        ``ALLOWED_DOMAINS``.
    """
    # Parse the base URL to extract its components
    base_parsed = urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid auth_base_url: {auth_base_url!r}")

    # Resolve the user supplied target
    # urljoin handles relative paths and absolute URLs correctly.
    resolved_url = urljoin(auth_base_url, post_login_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urlparse(resolved_url)

    # 1. Ensure the scheme is either http or https
    if target_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {target_parsed.scheme!r}")

    # 2. Check if the target is a relative URL (no netloc)
    if not target_parsed.netloc:
        # Relative URLs are safe – they stay within the application
        return resolved_url

    # 3. For absolute URLs, verify that the domain is allowed
    target_domain = target_parsed.hostname.lower() if target_parsed.hostname else ""

    # Allow same‑origin redirects
    base_domain = base_parsed.hostname.lower() if base_parsed.hostname else ""
    if target_domain == base_domain:
        return resolved_url

    # Allow explicitly permitted external domains
    if target_domain in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved_url

    # Anything else is considered unsafe
    raise ValueError(
        f"Redirect target {resolved_url!r} is not allowed: "
        "outside the base domain and not in ALLOWED_DOMAINS."
    )

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        print(generate_redirect_uri("https://app.example.com/", "/dashboard"))
        print(generate_redirect_uri("https://app.example.com/", "https://trustedpartner.org/welcome"))
        # The following will raise ValueError
        print(generate_redirect_uri("https://app.example.com/", "http://malicious.site/"))
    except ValueError as exc:
        print(f"Redirect rejected: {exc}")