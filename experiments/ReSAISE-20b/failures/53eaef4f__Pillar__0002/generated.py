#!/usr/bin/env python3
"""
Utility for constructing a safe redirect URL after login.
"""

from urllib.parse import urlparse, urljoin
import sys

# Domains that are considered safe for external redirects.
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a full redirect URL from the application base (`primary_url`) and
    a user supplied path or URL (`next_path`).

    Parameters
    ----------
    primary_url : str
        The base URL of the application, e.g. "https://app.example.com".
    next_path : str
        The path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside the application's domain or to an
        untrusted external domain.
    """
    # Parse base URL once
    parsed_primary = urlparse(primary_url)
    if not parsed_primary.scheme or not parsed_primary.netloc:
        raise ValueError(f"Invalid primary URL: {primary_url!r}")

    # Resolve next_path against the base
    candidate = urljoin(primary_url, next_path)

    parsed_candidate = urlparse(candidate)
    if not parsed_candidate.scheme or not parsed_candidate.netloc:
        # This can happen when next_path is a relative path that ends up
        # without a scheme/host; we default to the primary host.
        parsed_candidate = parsed_candidate._replace(
            scheme=parsed_primary.scheme,
            netloc=parsed_primary.netloc
        )
        candidate = parsed_candidate.geturl()

    # Security check: ensure the host is either the primary domain or a
    # whitelisted external domain.
    candidate_host = parsed_candidate.hostname.lower() if parsed_candidate.hostname else ""
    primary_host = parsed_primary.hostname.lower() if parsed_primary.hostname else ""

    # If the host matches the primary, we accept it.
    if candidate_host == primary_host:
        return candidate

    # If the host is in SAFE_DOMAINS, we also accept it.
    if candidate_host in (d.lower() for d in SAFE_DOMAINS):
        return candidate

    # Anything else is disallowed.
    raise ValueError(
        f"Redirect target '{candidate}' is outside the allowed domains."
    )

# Example usage (for manual testing)
if __name__ == "__main__":
    try:
        print(build_redirect_uri("https://app.example.com", "/dashboard"))
        print(build_redirect_uri("https://app.example.com", "https://trustedpartner.org/welcome"))
        # The following should raise an exception
        print(build_redirect_uri("https://app.example.com", "http://malicious.com/phish"))
    except ValueError as exc:
        print(f"Security check failed: {exc}", file=sys.stderr)