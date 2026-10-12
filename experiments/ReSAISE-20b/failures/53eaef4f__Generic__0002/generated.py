#!/usr/bin/env python3
"""
Utility to safely build a redirect URL after successful login.

The function ensures that the target location is either:
* within the same domain as `primary_url`, or
* an explicitly allowed external domain listed in `SAFE_DOMAINS`.

Any other redirect target results in a ValueError.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Domains that are considered safe for redirection (example entries)
SAFE_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. "https://myapp.com").
    next_path : str
        The user-specified redirect target.  This may be a relative path,
        an absolute URL, or a full path with scheme and host.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to point to
        either the application domain or a safe external domain.

    Raises
    ------
    ValueError
        If the resolved URL is not within the application domain or an
        allowed external domain.
    """
    # Parse the primary URL once for reuse
    parsed_primary = urlparse(primary_url)

    if not parsed_primary.scheme or not parsed_primary.netloc:
        raise ValueError("primary_url must be a full URL with scheme and host")

    # Resolve the next_path against the primary URL
    resolved = urljoin(primary_url, next_path)

    # Parse the resolved URL to inspect its components
    parsed_resolved = urlparse(resolved)

    # If the resolved URL has no scheme or host, it is a relative path.
    # In that case, prepend the primary domain.
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        resolved = urljoin(primary_url, next_path)
        parsed_resolved = urlparse(resolved)

    # Validate the target domain
    target_netloc = parsed_resolved.netloc.lower()

    # Check if it's the same domain as primary_url
    if target_netloc == parsed_primary.netloc.lower():
        return resolved

    # Check against the list of safe domains
    for domain in SAFE_DOMAINS:
        if target_netloc == domain.lower() or target_netloc.endswith("." + domain.lower()):
            return resolved

    # If we reach here, the redirect target is not trusted
    raise ValueError(f"Unsafe redirect target: {resolved}")

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(build_redirect_uri("https://myapp.com", "/dashboard"))
#     print(build_redirect_uri("https://myapp.com", "https://example.com/welcome"))
#     print(build_redirect_uri("https://myapp.com", "http://malicious.com/"))