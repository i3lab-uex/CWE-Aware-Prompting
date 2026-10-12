#!/usr/bin/env python3
"""
Utility for constructing a safe redirect URL after login.

The function ensures that the resulting URL either points to the same
domain as ``main_url`` or to one of a set of explicitly permitted domains.
Any attempt to redirect to an unknown domain will raise ``ValueError``.

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Domains that are allowed to be redirected to even if they differ from main_url
PERMITTED_DOMAINS: List[str] = [
    "https://trusted.com",
    "https://partner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a secure redirect URL based on the user-provided target.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    target_param : str
        The path or full URL supplied by the user.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL points outside the application domain and is not in PERMITTED_DOMAINS.
    """
    # Parse the main URL once
    base_parsed = urlparse(main_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Resolve the target relative to the base URL
    # This handles both absolute URLs and relative paths
    resolved = urljoin(main_url, target_param)

    parsed_target = urlparse(resolved)

    # Helper to compare netlocs ignoring default ports
    def normalize_netloc(netloc: str) -> str:
        host, *port = netloc.split(":")
        return f"{host.lower()}:{port[0]}" if port else host.lower()

    # Determine if target is within the same domain or a permitted domain
    base_netloc = normalize_netloc(base_parsed.netloc)
    target_netloc = normalize_netloc(parsed_target.netloc)

    # Check if the resolved URL is a full absolute URL
    is_absolute = bool(parsed_target.scheme and parsed_target.netloc)

    if is_absolute:
        # If absolute, ensure it's either the same domain or permitted
        if target_netloc != base_netloc and not any(
            normalize_netloc(urlparse(d).netloc) == target_netloc for d in PERMITTED_DOMAINS
        ):
            raise ValueError(f"Redirect target {resolved!r} is not allowed.")
    else:
        # For relative URLs, ensure they don't escape the base (e.g., via "//")
        if parsed_target.netloc:
            # A netloc present in a relative path indicates an attempt to escape
            raise ValueError(f"Invalid relative redirect target: {target_param!r}")

    return resolved

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     main = "https://app.example.com"
#     for target in ["/dashboard", "../admin", "https://trusted.com/home",
#                    "http://malicious.com"]:
#         try:
#             print(construct_redirect_url(main, target))
#         except ValueError as e:
#             print(f"Rejected: {e}")