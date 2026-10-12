#!/usr/bin/env python3
"""
Utility to assemble a secure API redirect URL.

The function validates that the resulting URL uses an approved domain
and endpoint, and appends optional query parameters safely.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable


# --------------------------------------------------------------------------- #
# Configuration: approved domains and endpoints
# --------------------------------------------------------------------------- #

# Allowed API domains (e.g., "api.example.com")
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "auth.example.org",
}

# Allowed API paths (e.g., "/v1/users")
ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v1/orders",
    "/v2/transactions",
)


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full API URL by combining the base, path and optional query
    parameters. The resulting URL is validated against a whitelist of domains
    and endpoints.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g., "https://api.example.com").
    api_path : str
        Endpoint path to append (e.g., "/v1/users").
    query_dict : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        Fully assembled and validated URL.

    Raises
    ------
    ValueError
        If the constructed URL contains an unapproved domain or endpoint.
    """
    # Normalize base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme:
        raise ValueError("Base API URL must include a scheme (e.g., https://)")

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {parsed_base.netloc}")

    # Validate endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {api_path}")

    # Join base URL with path
    full_url = urllib.parse.urljoin(base_api_url.rstrip("/") + "/", api_path.lstrip("/"))

    # Append query parameters if provided
    if query_dict:
        # Encode only non-empty values; skip None or empty strings
        filtered = {k: v for k, v in query_dict.items() if v not in (None, "",)}
        if filtered:
            query_string = urllib.parse.urlencode(filtered)
            full_url = f"{full_url}?{query_string}"

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example base and endpoint
    base = "https://api.example.com"
    path = "/v1/users"

    # Example query parameters
    params = {"id": "123", "detail": "full", "empty": ""}

    try:
        url = assemble_api_redirect_link(base, path, params)
        print("Assembled URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")