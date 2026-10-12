#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The module validates that the base domain is approved and the endpoint
belongs to a whitelist. It also safely encodes any query parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – adjust these sets/lists to your environment
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
    "secure.api.mycompany.net",
}

ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a validated redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        The base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g. "/users" or "orders").
    query_options : dict, optional
        Dictionary of query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed, validated API redirect URL.

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS`` or the endpoint
        is not in ``ALLOWED_ENDPOINTS``.
    """

    # Parse the base URL and ensure we have a scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url!r}")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not approved")

    # Normalise and validate endpoint
    normalized_endpoint = api_endpoint.strip()
    if not normalized_endpoint.startswith("/"):
        normalized_endpoint = "/" + normalized_endpoint

    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {normalized_endpoint!r} is not allowed")

    # Build the path by joining base path and endpoint
    # Preserve any existing path in the base URL (e.g., "/v1")
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", normalized_endpoint.lstrip("/"))

    # Encode query parameters safely
    if query_options:
        encoded_query = urllib.parse.urlencode(query_options, doseq=True)
    else:
        encoded_query = ""

    # Reconstruct the final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params (rarely used)
        encoded_query,
        ""   # fragment
    )
    return urllib.parse.urlunparse(final_url_parts)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_api_redirect(
            base_api_url="https://api.example.com/v1",
            api_endpoint="/users",
            query_options={"page": "2", "limit": "50"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")