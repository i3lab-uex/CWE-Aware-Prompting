#!/usr/bin/env python3
"""
Utility for generating safe API redirect URLs.

The function validates that the base URL is from an approved domain
and that the requested endpoint is in a whitelist of allowed endpoints.
It then constructs a full URL with optional query parameters.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: Allowed domains and endpoints
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
    "data.provider.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
    "/public/info",
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _normalize_domain(url: str) -> str:
    """
    Extract and normalize the network location (netloc) from a URL.
    The normalization removes common prefixes such as 'www.' and lowercases the domain.
    """
    parsed = urllib.parse.urlparse(url)
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc

def _validate_domain(base_url: str) -> None:
    """
    Raise ValueError if the base URL's domain is not in APPROVED_API_DOMAINS.
    """
    domain = _normalize_domain(base_url)
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for API redirects.")

def _validate_endpoint(api_path: str) -> None:
    """
    Raise ValueError if the API path is not in ALLOWED_ENDPOINTS.
    Normalization ensures a leading slash and removes trailing slashes for comparison.
    """
    # Ensure path starts with '/' and strip any query string or fragment
    path = urllib.parse.urlparse(api_path).path
    if not path.startswith("/"):
        path = "/" + path
    # Compare against the whitelist exactly
    if path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{path}' is not allowed.")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Generate a secure redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    params : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Validate domain and endpoint before constructing URL
    _validate_domain(base_url)
    _validate_endpoint(api_path)

    # Parse base URL to preserve scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)

    # Construct the new path: base path + api_path
    # Ensure there is exactly one slash between them
    base_path = parsed_base.path.rstrip("/")
    new_path = f"{base_path}{api_path}"

    # Merge query parameters if provided
    query = urllib.parse.urlencode(params) if params else ""

    # Rebuild the full URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            new_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return redirect_url

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         url = generate_api_redirect(
#             "https://api.example.com",
#             "/v1/users",
#             {"page": "2", "limit": "50"}
#         )
#         print(url)
#     except ValueError as exc:
#         print(f"Invalid request: {exc}")