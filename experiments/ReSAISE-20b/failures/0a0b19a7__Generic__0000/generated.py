#!/usr/bin/env python3
"""
Utility to build a secure API redirect URL.

The function validates that the resulting URL points to an approved
API domain and uses one of the allowed endpoints.  Query parameters,
if supplied, are URL‑encoded and appended to the final URL.

Usage:

    url = build_api_redirect_url(
        api_base_url="https://api.example.com",
        endpoint="/v1/users",
        query_params={"id": 42, "verbose": True}
    )
"""

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be defined in your application settings.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(url: str) -> str:
    """
    Extract and return the network location (netloc) of a URL in lower case.
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.lower()


def _validate_domain(netloc: str) -> None:
    """
    Raise ValueError if the domain is not approved.
    """
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {netloc}")


def _validate_endpoint(endpoint: str) -> None:
    """
    Raise ValueError if the endpoint is not in the allowed list.
    """
    # Ensure a leading slash for comparison
    ep = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    if ep not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{ep}' is not allowed")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API call.

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
        The fully-qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the base URL's domain is not approved or the endpoint is disallowed.
    """
    if not api_base_url:
        raise ValueError("api_base_url must be a non-empty string")

    # Validate base URL domain
    netloc = _normalize_domain(api_base_url)
    _validate_domain(netloc)

    # Validate endpoint
    _validate_endpoint(endpoint)

    # Join base URL and endpoint safely
    full_path = urllib.parse.urljoin(api_base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    # Append query parameters if provided
    if query_params:
        if not isinstance(query_params, dict):
            raise TypeError("query_params must be a dictionary")
        # Encode parameters; ensure values are strings
        encoded = urllib.parse.urlencode(
            {k: str(v) for k, v in query_params.items()}
        )
        full_path = f"{full_path}?{encoded}"

    return full_path