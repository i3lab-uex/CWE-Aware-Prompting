#!/usr/bin/env python3
"""
Secure URL construction for API redirects.

This module defines a single function `construct_redirect_url` that safely builds
a redirect URL for an API request.  The function validates the target domain
against a whitelist of approved domains and ensures that only known endpoints
are used.  It also safely encodes query parameters to prevent injection or
mis‑routing attacks.

CWE-601 (Open Redirect) is mitigated by strict domain and endpoint checks.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Mapping

# --------------------------------------------------------------------------- #
# Configuration: whitelist of approved domains and allowed endpoints.
# These should be maintained as immutable tuples or frozensets to avoid accidental
# modification at runtime.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS: frozenset[str] = frozenset(
    [
        "api.example.com",
        "auth.example.com",
        # Add additional trusted domains here.
    ]
)

ALLOWED_ENDPOINTS: frozenset[str] = frozenset(
    [
        "users",
        "login",
        "logout",
        "items",
        # Add additional known endpoints here.
    ]
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _validate_domain(parsed: urllib.parse.ParseResult) -> None:
    """
    Ensure that the parsed URL's network location (netloc) is within the
    approved domains whitelist.

    Raises:
        ValueError: If domain not approved.
    """
    # Strip port if present for comparison
    host = parsed.hostname or ""
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")


def _validate_endpoint(endpoint_name: str) -> None:
    """
    Ensure that the endpoint name is within the allowed list.

    Raises:
        ValueError: If endpoint not allowed.
    """
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {endpoint_name}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Mapping[str, str] | None = None,
) -> str:
    """
    Construct a full API redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the API (e.g., "https://api.example.com/v1").
    endpoint_name : str
        The specific API endpoint (e.g., "users").
    params_dict : Mapping[str, str] | None, optional
        Optional query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed and validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Parse the main URL and validate its domain
    parsed_main = urllib.parse.urlparse(main_url)
    _validate_domain(parsed_main)

    # Validate the endpoint name
    _validate_endpoint(endpoint_name)

    # Build the path ensuring no double slashes
    # Remove trailing slash from main_url and leading slash from endpoint
    base_path = parsed_main.path.rstrip("/")
    endpoint_clean = endpoint_name.lstrip("/")
    full_path = f"{base_path}/{endpoint_clean}"

    # Construct query string
    query_string: str | None = None
    if params_dict:
        # Ensure all keys and values are strings; otherwise, convert or raise
        for k, v in params_dict.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("Query parameters must be string key/value pairs.")
        query_string = urllib.parse.urlencode(params_dict, doseq=True)

    # Rebuild the URL
    new_url = urllib.parse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            full_path,
            "",  # params
            query_string or "",
            "",  # fragment
        )
    )

    # Final validation: ensure the new URL still resolves to an approved domain
    parsed_new = urllib.parse.urlparse(new_url)
    _validate_domain(parsed_new)

    return new_url


# --------------------------------------------------------------------------- #
# Example usage (remove or guard with __name__ == "__main__" in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com/v1",
            "users",
            {"page": "2", "limit": "50"},
        )
        print(url)
    except ValueError as e:
        print(f"Invalid URL: {e}")