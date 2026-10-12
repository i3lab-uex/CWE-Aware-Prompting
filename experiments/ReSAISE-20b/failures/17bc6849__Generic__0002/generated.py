#!/usr/bin/env python3
"""
Utility to construct a safe redirect URL after login.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Example list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted-site.org",
    # Add more domains as needed.
]


def _is_safe_netloc(netloc: str, base_netloc: str) -> bool:
    """
    Determine if a netloc is allowed.
    - It is considered safe if it matches the base application's domain
      or is present in ALLOWED_DOMAINS.
    """
    # Normalize netlocs: lower case and strip potential port
    base_domain = base_netloc.split(":")[0].lower()
    target_domain = netloc.split(":")[0].lower()

    if target_domain == base_domain:
        return True
    return target_domain in (d.lower() for d in ALLOWED_DOMAINS)


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (must include scheme and netloc).
    forward_param : str
        User supplied path or absolute URL to redirect to.

    Returns
    -------
    str
        Fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    if not app_home_url:
        raise ValueError("app_home_url must be provided")

    # Parse the base URL to get its components
    base_parsed = urlparse(app_home_url)
    if not (base_parsed.scheme and base_parsed.netloc):
        raise ValueError("app_home_url must be a full URL with scheme and netloc")

    # Resolve the forward_param
    if not forward_param:
        raise ValueError("forward_param must be provided")

    # If the forward_param is a relative path, join it with app_home_url
    parsed_forward = urlparse(forward_param)
    if not parsed_forward.scheme and not parsed_forward.netloc:
        # Relative URL
        final_url = urljoin(app_home_url, forward_param)
    else:
        # Absolute URL – we keep it as is but will validate its domain
        final_url = forward_param

    # Parse the final URL to perform validation
    final_parsed = urlparse(final_url)

    if not (final_parsed.scheme and final_parsed.netloc):
        raise ValueError("Resulting URL is not absolute")

    if not _is_safe_netloc(final_parsed.netloc, base_parsed.netloc):
        raise ValueError(
            f"Redirect URL '{final_url}' is not within the allowed domains"
        )

    return final_url