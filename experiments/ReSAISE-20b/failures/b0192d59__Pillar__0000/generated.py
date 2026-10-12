#!/usr/bin/env python3
"""
Utility for generating a safe API redirect URL.

The implementation uses urllib.parse to safely combine the base URI,
endpoint, and optional query parameters while enforcing strict domain
and endpoint validation to mitigate security issues such as
CWE‑664 (Improper Control of a Resource Through its Lifetime) and
open redirect vulnerabilities.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable


# --------------------------------------------------------------------------- #
# Configuration: allowed domains and endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.internal.local",
}

ALLOWED_ENDPOINTS: Set[str] = {
    "/v1/users",
    "/v1/orders",
    "/v1/items",
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_domain(netloc: str) -> None:
    """
    Validate that the network location part of a URL belongs to an approved domain.

    Parameters
    ----------
    netloc : str
        The network location part of a parsed URL (e.g., 'api.example.com:443').

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS``.
    """
    # Strip port if present
    domain = netloc.split(":")[0].lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")


def _validate_endpoint(endpoint: str) -> None:
    """
    Validate that the endpoint is allowed.

    Parameters
    ----------
    endpoint : str
        The path component of a URL (e.g., '/v1/users').

    Raises
    ------
    ValueError
        If the endpoint is not in ``ALLOWED_ENDPOINTS``.
    """
    if endpoint.lower() not in (e.lower() for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Unapproved API endpoint: {endpoint}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API URL by safely merging the base URI,
    endpoint, and optional query parameters.

    The function performs the following steps:
      1. Parse ``base_uri`` and ensure its domain is approved.
      2. Resolve ``api_endpoint`` against the base path.
      3. Validate that the resulting endpoint is allowed.
      4. Merge any supplied query parameters into the final URL.

    Parameters
    ----------
    base_uri : str
        Base API URL (e.g., 'https://api.example.com/api/').
    api_endpoint : str
        Target endpoint (e.g., '/v1/users').
    query : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully-qualified, validated API URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    if not base_uri:
        raise ValueError("Base URI must be a non-empty string")

    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_uri)
    _validate_domain(parsed_base.netloc)

    # Resolve the endpoint against the base path
    joined_path = urllib.parse.urljoin(parsed_base.path, api_endpoint)
    _validate_endpoint(joined_path)

    # Merge query parameters
    base_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)
    # Flatten parse_qs output (list values) into single-value dict
    base_query = {k: v[0] for k, v in base_query.items()}

    if query:
        # Ensure all keys and values are strings
        for k, v in query.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("Query keys and values must be strings")
        # Merge with base query; new params override existing ones
        base_query.update(query)

    final_query = urllib.parse.urlencode(base_query, doseq=True)

    # Build the final URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        parsed_base.params,
        final_query,
        parsed_base.fragment,
    )
    return urllib.parse.urlunparse(final_parts)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            "https://api.example.com/api/",
            "/v1/users",
            {"id": "123", "format": "json"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")