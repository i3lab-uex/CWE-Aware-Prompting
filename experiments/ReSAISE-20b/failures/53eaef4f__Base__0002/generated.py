#!/usr/bin/env python3
"""
Utility for safely constructing a redirect URL after login.

The function ensures that the resulting URL stays within the
application domain or points to one of a whitelist of trusted external domains.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Whitelist of domains that are considered safe for external redirects.
SAFE_DOMAINS: List[str] = [
    "trusted.example.com",
    "partner.org",
    # Add other trusted domains here
]


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL based on the user‑provided `next_path`.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_path : str
        The path or full URL the user wants to be redirected to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the final URL is not within the application domain or an allowed
        external domain, or if the input URLs are malformed.
    """
    # Parse and validate the primary URL
    base_parsed = urlparse(primary_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("`primary_url` must be a valid absolute URL")

    # Resolve the user supplied path against the base URL
    resolved_url = urljoin(primary_url, next_path)
    parsed_resolved = urlparse(resolved_url)

    # If the resolved URL has no scheme (e.g., a relative path),
    # urljoin will prepend the base scheme and netloc.
    if not parsed_resolved.scheme:
        # In this case, the URL is definitely relative to the base
        return resolved_url

    # Check that we are still in the same domain as the application.
    if (parsed_resolved.scheme == base_parsed.scheme and
            parsed_resolved.netloc == base_parsed.netloc):
        return resolved_url

    # If the URL points to an external domain, ensure it is whitelisted.
    if parsed_resolved.netloc in SAFE_DOMAINS:
        return resolved_url

    # Anything else is considered unsafe.
    raise ValueError(
        f"Untrusted redirect target: {parsed_resolved.netloc!r}. "
        "Allowed domains are the application domain or one of the safe domains."
    )