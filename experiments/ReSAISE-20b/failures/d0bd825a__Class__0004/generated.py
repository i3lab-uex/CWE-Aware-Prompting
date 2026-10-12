#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function verifies that the base URL belongs to an approved domain and
that the requested endpoint is on a whitelist.  It then builds a fully
qualified URL with optional query parameters.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional


# --------------------------------------------------------------------------- #
# Configuration:  These should be populated with the real allowed values.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "api.partner.com",
    # Add additional approved domains here
}

ALLOWED_ENDPOINTS = [
    "v1/users",
    "v1/items",
    "v2/orders",
    # Add additional safe endpoints here
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _normalize_domain(netloc: str) -> str:
    """
    Normalise a network location string by removing port information
    and converting to lowercase.
    """
    host, _, _ = netloc.partition(":")
    return host.lower()


def _validate_domain(base_url: str) -> None:
    """
    Ensure that the base URL uses http/https and belongs to an approved domain.
    """
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    domain = _normalize_domain(parsed.netloc)
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure that the endpoint is on the whitelist.
    """
    # Normalise by stripping leading/trailing slashes
    norm_ep = endpoint.strip("/")
    if norm_ep not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")


def _join_path(base: str, endpoint: str) -> str:
    """
    Safely join a base URL with an endpoint path.
    """
    # Ensure there is exactly one slash between components
    return urllib.parse.urljoin(base.rstrip("/") + "/", endpoint.lstrip("/"))


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint to call (e.g., "v1/users").
    opts : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        A fully constructed redirect URL, e.g.:
        "https://api.example.com/v1/users?foo=bar".

    Raises
    ------
    ValueError
        If the base URL does not belong to an approved domain,
        or if the endpoint is not in the whitelist.
    """
    # Validation
    _validate_domain(base_url_api)
    _validate_endpoint(api_endpoint)

    # Construct the path
    full_path = _join_path(base_url_api, api_endpoint)

    # Append query parameters if provided
    if opts:
        query_string = urllib.parse.urlencode(opts, doseq=True)
        full_path = f"{full_path}?{query_string}"

    return full_path


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users/",
            {"id": "123", "verbose": "true"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print("Validation error:", exc)