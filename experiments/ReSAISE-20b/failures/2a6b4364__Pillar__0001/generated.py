#!/usr/bin/env python3
"""
Utility for safely constructing a post‑login redirect URL.

The function ensures that the resulting URL is either within the same
origin as `base_url` or belongs to one of a whitelist of external domains.
This protects against open‑redirect vulnerabilities (CWE‑601) and
improper resource control (CWE‑664).
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Domains considered safe for external redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

def _is_safe_domain(domain: str) -> bool:
    """
    Check whether a domain is allowed for redirection.
    """
    # Normalize the domain (lowercase, strip trailing dot)
    normalized = domain.lower().rstrip(".")
    return any(normalized == allowed.lower() for allowed in ALLOWED_DOMAINS)

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    next_param : str
        The user‑provided path or URL fragment to redirect to.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain or is otherwise unsafe.
    """
    # Resolve relative URLs against the base URL
    resolved = urljoin(base_url, next_param)

    parsed_base = urlparse(base_url)
    parsed_resolved = urlparse(resolved)

    # Check that scheme is HTTP/HTTPS
    if parsed_resolved.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme}")

    # If the resolved host matches the base host, it's safe
    if parsed_resolved.hostname and parsed_base.hostname:
        if parsed_resolved.hostname.lower() == parsed_base.hostname.lower():
            return resolved

    # If host is in the whitelist, allow
    if parsed_resolved.hostname and _is_safe_domain(parsed_resolved.hostname):
        return resolved

    # All other cases are considered unsafe
    raise ValueError(f"Redirect URL '{resolved}' is not allowed.")

# Example usage (commented out to avoid execution on import)
# if __name__ == "__main__":
#     print(create_redirect_url("https://app.example.com/", "/dashboard"))