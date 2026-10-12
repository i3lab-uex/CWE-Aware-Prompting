#!/usr/bin/env python3
"""
Utility for constructing a secure API redirect URL.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration:  These should be populated with the domains and endpoints
# that your application is allowed to access.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS: list[str] = [
    "/v1/users",
    "/v2/orders",
    "/search",
]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API URL by merging `base_uri` with
    `api_endpoint` and optional query parameters.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g., "/v1/users").
    query : dict[str, str] | None
        Optional mapping of query parameters.

    Returns
    -------
    str
        The fully assembled URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    if not isinstance(base_uri, str) or not isinstance(api_endpoint, str):
        raise TypeError("base_uri and api_endpoint must be strings")

    # Normalize base URI
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not approved")

    # Normalize endpoint
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Validate endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {api_endpoint!r} is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Assemble the final URL components
    url_components = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        urllib.parse.urlencode(query or {}, doseq=True),
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(url_components)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "verbose": "true"},
        )
        print(url)
    except ValueError as e:
        print(f"URL generation failed: {e}")