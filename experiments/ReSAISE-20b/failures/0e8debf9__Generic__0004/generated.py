#!/usr/bin/env python3
"""
Utility to safely construct a post‑login redirect URL.

The function combines an application base URL with a user supplied
redirect target while ensuring the final URL stays within approved domains.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# A list of external domains that are allowed for redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Build a full redirect URL from the base authentication URL and a
    user supplied path or absolute URL.

    Parameters
    ----------
    auth_base_url : str
        Base authentication URL of the application (e.g. 'https://app.example.com').
    post_login_param : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        The resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe domain (outside the base domain
        and not in :data:`ALLOWED_DOMAINS`).
    """
    # Parse the base URL once
    base_parsed = urlparse(auth_base_url)

    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid auth_base_url: {auth_base_url!r}")

    # Parse the target URL (could be relative or absolute)
    target_parsed = urlparse(post_login_param)

    # If the target is a relative path, simply join it with the base
    if not target_parsed.scheme and not target_parsed.netloc:
        # urljoin handles leading '/' correctly
        resolved = urljoin(auth_base_url, post_login_param)
    else:
        # Absolute URL: check that its domain is allowed
        target_netloc = target_parsed.netloc.lower()

        # Allow the same domain as the base
        if target_netloc == base_parsed.netloc.lower():
            resolved = post_login_param
        else:
            # Check against the list of approved external domains
            if any(target_netloc == d.lower() or target_netloc.endswith("." + d.lower())
                   for d in ALLOWED_DOMAINS):
                resolved = post_login_param
            else:
                raise ValueError(
                    f"Unsafe redirect target: {post_login_param!r} "
                    f"is not in allowed domains or the base domain."
                )

    # Final safety check: parse again to ensure we didn't lose scheme/netloc
    final_parsed = urlparse(resolved)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError(f"Resulting URL is malformed: {resolved!r}")

    return resolved


# Example usage (uncomment to test)
if __name__ == "__main__":
    base = "https://app.example.com"
    # Relative path
    print(generate_redirect_uri(base, "/dashboard"))
    # Absolute URL to same domain
    print(generate_redirect_uri(base, "https://app.example.com/profile"))
    # Absolute URL to allowed external domain
    print(generate_redirect_uri(base, "https://example.com/welcome"))
    # This will raise ValueError
    try:
        print(generate_redirect_uri(base, "https://malicious.com/phish"))
    except ValueError as exc:
        print("Caught error:", exc)