#!/usr/bin/env python3
"""
Utility to build a safe redirect URL after authentication.
"""

import urllib.parse

# Example list of external domains that are allowed for redirection
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL by combining the application base URL with
    a user-provided redirect parameter.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (not within the base domain and not an
        allowed external domain).
    """
    # Parse base URL to get scheme and netloc for safety checks
    base_parsed = urllib.parse.urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect target
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(resolved)

    # If the resolved URL is relative (no scheme), it's safe
    if not parsed.scheme:
        return resolved

    # If the domain matches the base domain, it's safe
    if parsed.netloc == base_parsed.netloc:
        return resolved

    # Otherwise, ensure the domain is in ALLOWED_DOMAINS
    host = parsed.hostname or ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(
            f"Unsafe redirect target: {parsed.netloc} is not allowed"
        )

    return resolved