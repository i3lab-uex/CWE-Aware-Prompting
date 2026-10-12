#!/usr/bin/env python3
"""
Utility to build a safe redirect URL for an API call.
"""

from urllib.parse import urljoin, urlencode, urlparse
from typing import Dict, Optional

# Define approved domains and endpoints. In a real application these would
# be loaded from configuration or environment variables.
APPROVED_API_DOMAINS = {"api.example.com", "service.anotherdomain.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API redirect URL.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    endpoint : str
        The specific endpoint path (e.g., "/v1/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The complete redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or endpoint.
    """
    # Ensure the base URL ends with a slash for correct urljoin behavior
    if not api_base_url.endswith("/"):
        base = f"{api_base_url}/"
    else:
        base = api_base_url

    # Normalise the endpoint (strip leading slashes to avoid absolute paths)
    ep = endpoint.lstrip("/")
    # Reconstruct the path
    full_path = f"/{ep}"

    # Build the initial URL (without query parameters)
    url = urljoin(base, full_path)

    # Append query parameters if provided
    if query_params:
        url = f"{url}?{urlencode(query_params)}"

    # Parse the final URL to inspect components
    parsed = urlparse(url)

    # Domain validation: ensure hostname is in the approved set
    host = parsed.hostname or ""
    if host.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Unapproved API domain: {host}")

    # Endpoint validation: ensure the path is in the allowed list
    if parsed.path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed API endpoint: {parsed.path}")

    return url

# Example usage (commented out to avoid accidental execution)
if __name__ == "__main__":
    try:
        redirect = build_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "20"},
        )
        print("Redirect URL:", redirect)
    except ValueError as e:
        print("Error building redirect URL:", e)