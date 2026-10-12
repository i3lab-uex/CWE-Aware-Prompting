#!/usr/bin/env python3
"""
Utility to build a secure API redirect URL.

The function validates that the resulting URL belongs to an approved
domain and uses only whitelisted endpoints. It also safely encodes
any query parameters.

Author: ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – edit these to suit your environment
# --------------------------------------------------------------------------- #

# Set of approved base API domains (e.g., 'api.example.com')
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

# List of safe, allowable API endpoints
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/posts",
    "/v2/items",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_url : str
        The base address of an API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path to be appended (e.g., "/v1/users").
    params : dict, optional
        Query parameters to be encoded into the URL.

    Returns
    -------
    str
        A fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the final URL's domain is not in ``APPROVED_API_DOMAINS`` or
        if the endpoint is not in ``ALLOWED_ENDPOINTS``.
    """
    # Parse base URL to validate domain
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Normalize the domain (strip port if present)
    base_domain = parsed_base.hostname
    if base_domain is None:
        raise ValueError(f"Could not determine domain from: {base_url!r}")

    if base_domain.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{base_domain}' is not approved for API redirects."
        )

    # Ensure the endpoint path starts with a slash
    if not api_path.startswith("/"):
        raise ValueError(f"API path must start with '/': {api_path!r}")

    # Validate the endpoint against allowed list
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed.")

    # Build the full path
    full_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", api_path.lstrip("/"))

    # Append query parameters if provided
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{full_url}?{query_string}"

    return full_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect(
            base_url="https://api.example.com",
            api_path="/v1/users",
            params={"page": "2", "limit": "50"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print("Error:", exc)