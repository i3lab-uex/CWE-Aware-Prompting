#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates that the resulting URL:
* points to an approved domain
* uses one of the allowed endpoints
* has properly encoded query parameters

This prevents misuse such as open redirect vulnerabilities or
cross‑site request forgery via malformed URLs.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – in a real project these would be imported from a config file
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.company.org",
    "sandbox.api.test",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/transactions",
    # Add other safe endpoints here
]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path (e.g., "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        A safe, fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """

    # Parse and validate base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url}")

    # Normalise the domain (lowercase, strip 'www.')
    netloc = parsed_base.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not in the list of approved API domains.")

    # Ensure endpoint starts with a slash and is allowed
    normalized_endpoint = api_endpoint if api_endpoint.startswith("/") else f"/{api_endpoint}"
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed.")

    # Construct the path by joining base and endpoint
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Build the final URL components
    url_components = parsed_base._replace(path=joined_path)

    # Encode query parameters safely
    if query_options:
        # Ensure all values are strings; convert otherwise
        safe_query = {k: str(v) for k, v in query_options.items()}
        url_components = url_components._replace(query=urllib.parse.urlencode(safe_query))

    # Reassemble the URL
    redirect_url = urllib.parse.urlunparse(url_components)

    return redirect_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_api_redirect(
            base_api_url="https://api.example.com",
            api_endpoint="/v1/users",
            query_options={"id": "123", "format": "json"},
        )
        print("Redirect URL:", url)
    except ValueError as e:
        print(f"URL construction failed: {e}")