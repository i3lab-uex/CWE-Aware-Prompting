#!/usr/bin/env python3
"""
Secure redirect URI generator.

This module provides a single function, :func:`generate_redirect_uri`,
which safely constructs the full redirect URL that should be used after a
user logs in.  The function ensures that the resulting URI is either
within the same host as the authentication base URL or belongs to one of
the pre‑approved external domains.

The implementation follows the recommendations for mitigating CWE-610
(Externally Controlled Reference to a Resource in Another Sphere).
"""

from urllib.parse import urlparse, urljoin
from typing import List

# --------------------------------------------------------------------------- #
# Configuration: list of external domains that are allowed for redirection.
# Example values – replace with your actual allowed domains.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

# --------------------------------------------------------------------------- #
def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URI after login.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g. "https://app.example.com").
    post_login_param : str
        The user supplied path or full URL to which the user wants to be redirected.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL is outside the allowed domain(s).
    """
    # Parse the base authentication URL
    base_parsed = urlparse(auth_base_url)
    if not (base_parsed.scheme and base_parsed.netloc):
        raise ValueError(f"Invalid auth_base_url: {auth_base_url!r}")

    # Resolve the post-login target against the base URL
    resolved = urljoin(auth_base_url, post_login_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urlparse(resolved)

    # The redirect must use the same scheme as the base (e.g. https)
    if target_parsed.scheme != base_parsed.scheme:
        raise ValueError(f"Redirect scheme {target_parsed.scheme!r} does not match base scheme {base_parsed.scheme!r}")

    # Determine whether the target is internal (same host) or external
    if target_parsed.netloc == base_parsed.netloc:
        # Internal redirect – allowed
        return resolved

    # External redirect – check against the whitelist
    host = target_parsed.hostname or ""
    if host in ALLOWED_DOMAINS:
        return resolved

    # If the hostname contains a subdomain of an allowed domain, also allow
    for domain in ALLOWED_DOMAINS:
        if host.endswith("." + domain):
            return resolved

    # If none of the checks pass, reject the redirect
    raise ValueError(
        f"Unsafe redirect target: {resolved!r} (host {target_parsed.hostname!r} not allowed)"
    )

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and basic sanity checks
    try:
        print(generate_redirect_uri("https://app.example.com", "/dashboard"))
        print(generate_redirect_uri("https://app.example.com", "https://example.com/home"))
        # The following should raise ValueError
        print(generate_redirect_uri("https://app.example.com", "http://malicious.com"))
    except ValueError as exc:
        print(f"Error: {exc}")