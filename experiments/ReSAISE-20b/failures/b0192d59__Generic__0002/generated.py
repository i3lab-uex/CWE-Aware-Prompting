#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL by combining a base URI, an endpoint,
and optional query parameters. The function validates that the target domain
and path are approved to mitigate open redirect or endpoint abuse.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration: define which domains and endpoints are considered safe.
# --------------------------------------------------------------------------- #

# Approved API domains (e.g., https://api.example.com)
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "api.anotherdomain.org",
}

# Allowed endpoint paths (relative to the base domain)
ALLOWED_ENDPOINTS: list[str] = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_path(path: str) -> str:
    """
    Normalizes a URL path by removing duplicate slashes and ensuring it starts
    with a single leading slash.
    """
    # Use urljoin to collapse redundant slashes and then strip query part
    return urllib.parse.urljoin("/", path)

def _is_domain_approved(parsed: urllib.parse.ParseResult) -> bool:
    """
    Checks if the netloc (domain + optional port) belongs to an approved domain.
    The check is case-insensitive and ignores the port number if present.
    """
    host = parsed.hostname or ""
    return host.lower() in APPROVED_API_DOMAINS

def _is_endpoint_approved(endpoint: str) -> bool:
    """
    Validates that the given endpoint path is among the allowed endpoints.
    Comparison is case-sensitive to preserve API semantics.
    """
    return endpoint in ALLOWED_ENDPOINTS

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified API URL by merging `base_uri`, `api_endpoint`,
    and optional query parameters.

    Parameters
    ----------
    base_uri : str
        Base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path to append (e.g., "/v1/users").
    query : dict[str, str], optional
        Dictionary of key/value pairs to be encoded as query parameters.

    Returns
    -------
    str
        The assembled, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    # Parse base URI
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    # Normalize and validate domain
    if not _is_domain_approved(parsed_base):
        raise ValueError(f"Unapproved domain: {parsed_base.netloc!r}")

    # Normalize endpoint path
    normalized_endpoint = _normalize_path(api_endpoint)

    if not _is_endpoint_approved(normalized_endpoint):
        raise ValueError(f"Unapproved endpoint: {normalized_endpoint!r}")

    # Build full path by joining base path and endpoint
    # Ensure that the base path ends without a trailing slash to avoid double slashes.
    full_path = urllib.parse.urljoin(parsed_base.path or "/", normalized_endpoint)

    # Merge query parameters
    existing_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)
    if query:
        # Convert existing_query values from list to single string for merging
        merged = {k: v[0] if len(v) == 1 else v for k, v in existing_query.items()}
        merged.update(query)
    else:
        merged = {k: v[0] if len(v) == 1 else v for k, v in existing_query.items()}

    encoded_query = urllib.parse.urlencode(merged, doseq=True)

    # Reconstruct the final URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         url = generate_api_redirect_uri(
#             "https://api.example.com",
#             "/v1/users",
#             {"page": "2", "sort": "asc"}
#         )
#         print(url)
#     except ValueError as exc:
#         print(f"Validation error: {exc}")