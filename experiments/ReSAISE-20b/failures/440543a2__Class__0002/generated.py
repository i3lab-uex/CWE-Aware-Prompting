#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates that the target domain and endpoint are approved
before assembling the final URL. It uses urllib.parse for robust URL
manipulation and ensures that query parameters are correctly encoded.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable

# --------------------------------------------------------------------------- #
# Configuration:  Allowed domains and endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "auth.example.org",
    # Add more approved domains here
}

ALLOWED_ENDPOINTS: Set[str] = {
    "/v1/users",
    "/v2/orders",
    "/auth/login",
    # Add more allowed endpoints here
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_domain(netloc: str) -> None:
    """
    Ensure the netloc (host[:port]) belongs to an approved domain.
    Raises ValueError if not approved.
    """
    host = netloc.split(":")[0].lower()
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")


def _validate_endpoint(path: str) -> None:
    """
    Ensure the path is an allowed endpoint.
    Raises ValueError if not approved.
    """
    # Normalise the path: strip query & fragment, ensure leading slash
    cleaned_path = urllib.parse.urlparse(path).path
    if not cleaned_path.startswith("/"):
        cleaned_path = "/" + cleaned_path

    if cleaned_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {cleaned_path}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g., "https://api.example.com").
    path : str
        The target endpoint path (e.g., "/v1/users").
    params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    _validate_domain(parsed_base.netloc)

    # Parse and validate the endpoint
    parsed_path = urllib.parse.urlparse(path)
    _validate_endpoint(parsed_path.path)

    # Build the new URL components
    scheme = parsed_base.scheme
    netloc = parsed_base.netloc

    # Resolve the new path relative to the base
    joined_path = urllib.parse.urljoin(parsed_base.path or "/", parsed_path.path)

    # Merge existing query parameters from base (if any) with new params
    base_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)
    new_params: Dict[str, str] = {}
    if params:
        for k, v in params.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError(f"Query parameters must be strings: {k!r}={v!r}")
            new_params[k] = v

    # Combine base and new query parameters, giving precedence to new_params
    merged_query = {**{k: v[0] for k, v in base_query.items()}, **new_params}
    query_string = urllib.parse.urlencode(merged_query, doseq=False)

    # Assemble the final URL
    final_parts = urllib.parse.ParseResult(
        scheme=scheme,
        netloc=netloc,
        path=joined_path,
        params="",  # No params part in the path
        query=query_string,
        fragment=""  # No fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com",
            path="/v1/users",
            params={"id": "123", "verbose": "true"}
        )
        print(f"Constructed URL: {url}")
    except ValueError as e:
        print(f"Validation error: {e}")