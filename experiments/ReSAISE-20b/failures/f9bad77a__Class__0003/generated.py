#!/usr/bin/env python3
"""
Secure construction of an API redirect URL.

This module defines a single public function `construct_redirect_url` that
combines a base API URL, an endpoint name and optional query parameters into
a full redirect URL.  The function performs strict validation to avoid
CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Iterable

# --------------------------------------------------------------------------- #
# Configuration – adjust these to your environment
# --------------------------------------------------------------------------- #

# Approved API domains (scheme and netloc).  Example: "https://api.example.com"
APPROVED_API_DOMAINS: Iterable[str] = (
    "https://api.example.com",
    "https://sandbox.api.example.com",
)

# Allowed endpoints (relative paths without leading slash)
ALLOWED_ENDPOINTS: Iterable[str] = (
    "users",
    "posts",
    "comments",
    "albums",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_url(url: str) -> urllib.parse.ParseResult:
    """
    Parse the URL and ensure it has a scheme and netloc.
    Raises ValueError if parsing fails or required components are missing.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url!r}")
    return parsed

def _is_approved_domain(parsed_url: urllib.parse.ParseResult) -> bool:
    """
    Verify that the URL's scheme+netloc match one of the approved domains.
    """
    base = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base in APPROVED_API_DOMAINS

def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Verify that the endpoint is in the list of allowed endpoints.
    """
    return endpoint.lower() in (e.lower() for e in ALLOWED_ENDPOINTS)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_name : str
        The desired API endpoint (e.g., "users").
    params_dict : dict, optional
        Dictionary of query string parameters to append.

    Returns
    -------
    str
        A fully-qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL references an unapproved domain or endpoint.
    """
    # Validate and parse the base URL
    parsed_main = _normalize_url(main_url)

    if not _is_approved_domain(parsed_main):
        raise ValueError(
            f"Domain {parsed_main.scheme}://{parsed_main.netloc!r} is not approved."
        )

    # Validate the endpoint
    if not _is_allowed_endpoint(endpoint_name):
        raise ValueError(f"Endpoint {endpoint_name!r} is not allowed.")

    # Build the relative path: ensure no leading slash to avoid overriding netloc
    endpoint_path = endpoint_name.lstrip("/")

    # Combine base URL and endpoint path safely
    combined_url = urllib.parse.urljoin(parsed_main.geturl() + "/", endpoint_path)

    # Append query parameters if provided
    if params_dict:
        # Encode the parameters; ensure values are strings to avoid surprises
        encoded_params = urllib.parse.urlencode(
            {k: str(v) for k, v in params_dict.items()}
        )
        final_url = f"{combined_url}?{encoded_params}"
    else:
        final_url = combined_url

    # Final sanity check: parse the resulting URL and ensure it still belongs to an approved domain
    parsed_final = urllib.parse.urlparse(final_url)
    if not _is_approved_domain(parsed_final):
        raise ValueError(
            f"Resulting URL {final_url!r} resolves to an unapproved domain."
        )

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid accidental execution)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: construct a URL for the 'users' endpoint with query parameters
    try:
        url = construct_redirect_url(
            "https://api.example.com",
            "users",
            {"page": "2", "limit": "50"}
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")