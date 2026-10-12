#!/usr/bin/env python3
"""
Utility to generate a safe post‑login redirect URI.

The function validates that the target URL is either:
  * relative to the authentication base URL, or
  * an absolute URL whose domain is in ``ALLOWED_DOMAINS``.

If the target is unsafe, a ValueError is raised.
"""

from urllib.parse import urlparse, urljoin

# Pre‑approved external domains for redirects
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add other domains as needed
}


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after authentication.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    post_login_param : str
        The user‑supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in
        ``ALLOWED_DOMAINS``).
    """
    if not auth_base_url:
        raise ValueError("auth_base_url must be provided")

    # Resolve the target URL relative to the base
    resolved = urljoin(auth_base_url, post_login_param)

    parsed_resolved = urlparse(resolved)
    parsed_base = urlparse(auth_base_url)

    # If the resolved URL is relative (no netloc), it's safe
    if not parsed_resolved.netloc:
        return resolved

    # If the host matches the base domain, it's safe
    if parsed_resolved.netloc == parsed_base.netloc:
        return resolved

    # If the host is in the list of allowed external domains, it's safe
    if parsed_resolved.hostname and parsed_resolved.hostname.lower() in ALLOWED_DOMAINS:
        return resolved

    # Otherwise the URL is considered unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")