#!/usr/bin/env python3
"""
Secure redirect URL construction.

This module provides a single helper function,
`construct_redirect_url`, which safely builds the final
redirect URL after authentication. It guards against open‑
redirect vulnerabilities by validating that the target
URL belongs to the application domain or an explicitly
whitelisted external domain.

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Domains that are considered safe for redirection.
PERMITTED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    main_url : str
        The base application URL (e.g. "https://app.example.com/").
    target_param : str
        The path or full URL supplied by the user for post‑login navigation.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to the application domain
        or one of the permitted external domains.
    """
    if not main_url:
        raise ValueError("Main URL must be provided")

    # Parse the base application URL
    main_parsed = urlparse(main_url)
    if not main_parsed.scheme or not main_parsed.netloc:
        raise ValueError("Main URL must be a valid absolute URL")

    # Resolve the target relative to the main URL
    resolved = urljoin(main_url, target_param)

    # Parse the resolved target URL
    target_parsed = urlparse(resolved)

    # Ensure scheme is http or https (to avoid schemes like data:, javascript:)
    if target_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {target_parsed.scheme}")

    # Determine if the target is internal (same host) or external but permitted
    is_internal = (
        target_parsed.netloc == main_parsed.netloc or
        target_parsed.hostname == main_parsed.hostname
    )

    is_permitted_external = (
        target_parsed.netloc in PERMITTED_DOMAINS or
        (target_parsed.hostname and any(
            target_parsed.hostname == d or target_parsed.hostname.endswith(f".{d}")
            for d in PERMITTED_DOMAINS
        ))
    )

    if not (is_internal or is_permitted_external):
        raise ValueError(
            f"Redirect target '{resolved}' is not within the application domain "
            "or an allowed external domain."
        )

    # Normalise: ensure a trailing slash if the path is empty
    if not target_parsed.path:
        resolved = f"{resolved}/"

    return resolved

# Example usage (commented out)
# if __name__ == "__main__":
#     base = "https://app.example.com/"
#     next_path = "/dashboard"
#     print(construct_redirect_url(base, next_path))