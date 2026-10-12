# -*- coding: utf-8 -*-
"""
Utility module for generating secure API redirect URLs.

The `generate_redirect_link` function constructs a full URL by
combining a base API URL, an endpoint path and optional query
parameters.  It validates that the resulting URL belongs to one of
the approved domains and that the endpoint is allowed.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------
# Configuration:  These should be defined by the application.
# --------------------------------------------------------------------

APPROVED_API_DOMAINS: Iterable[str] = {
    "api.example.com",
    "api.safe-service.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _normalize_endpoint(endpoint: str) -> str:
    """
    Ensure the endpoint starts with a single leading slash and contains
    no trailing slashes (except for root "/").
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    # Remove trailing slash unless the endpoint is just "/"
    if len(endpoint) > 1 and endpoint.endswith("/"):
        endpoint = endpoint.rstrip("/")
    return endpoint


def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Raise ValueError if the URL's domain is not in APPROVED_API_DOMAINS.
    """
    host = parsed_url.hostname
    if host is None or host.lower() not in (d.lower() for d in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{host}' is not an approved API domain.")


def _validate_endpoint(endpoint: str) -> None:
    """
    Raise ValueError if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    norm_endpoint = _normalize_endpoint(endpoint)
    if norm_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{norm_endpoint}' is not allowed.")


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API redirect URL.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g., "/v1/users").
    query_info : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The complete, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not use an approved domain or endpoint.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: '{base_url}'")
    _validate_domain(parsed_base)

    # Normalize and validate the endpoint
    normalized_endpoint = _normalize_endpoint(endpoint_path)
    _validate_endpoint(normalized_endpoint)

    # Build the full path
    # Ensure no double slashes when joining base and endpoint
    path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Encode query parameters if provided
    query_string = urllib.parse.urlencode(query_info or {})

    # Assemble the final URL
    full_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        path,
        "",  # params
        query_string,
        ""   # fragment
    )
    full_url = urllib.parse.urlunparse(full_url_parts)

    return full_url


# --------------------------------------------------------------------
# Example usage (commented out; remove for production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "25"}
        )
        print(url)  # https://api.example.com/v1/users?page=2&limit=25
    except ValueError as exc:
        print(f"URL generation failed: {exc}")