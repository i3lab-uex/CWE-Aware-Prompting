#!/usr/bin/env python3
"""
Utility to safely assemble a post‑login redirect URL.

The function ensures that the resulting URL is either:
*   within the same domain as ``main_base_url``, or
*   an absolute URL whose hostname is in the allowed external domains list.

Any other destination raises a ValueError to prevent open‑redirect
vulnerabilities (CWE-610).
"""

from urllib.parse import urlparse, urljoin

# Pre‑approved external domains that may be used for redirection.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL from the base authentication URL and
    the user‑supplied next route.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g., https://app.example.com).
    next_route : str
        The user supplied path or absolute URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is neither the same as
        ``main_base_url`` nor in :data:`ALLOWED_DOMAINS`.
    """
    # Parse the base URL once.
    base_parsed = urlparse(main_base_url)

    # Resolve next_route against the base URL.
    joined_url = urljoin(main_base_url, next_route)

    # Parse the resolved URL to inspect its components.
    target_parsed = urlparse(joined_url)

    # If the target is a relative path (no netloc) it is safe.
    if not target_parsed.netloc:
        return joined_url

    # Normalize hostnames to lowercase for comparison.
    target_host = target_parsed.hostname.lower() if target_parsed.hostname else ""

    # Allow the same host as the base URL.
    if target_host == base_parsed.hostname.lower():
        return joined_url

    # Allow any host in the pre‑approved list.
    if target_host in ALLOWED_DOMAINS:
        return joined_url

    # If none of the above, reject as unsafe.
    raise ValueError(
        f"Unsafe redirect target: {joined_url!r} is not within the allowed domains."
    )