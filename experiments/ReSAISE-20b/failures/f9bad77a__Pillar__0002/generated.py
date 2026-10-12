#!/usr/bin/env python3
"""
Utility to construct a full redirect URL for API requests.
The function validates that the target domain and endpoint are trusted
before building the final URL.  It also safely encodes any query parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Mapping

# --------------------------------------------------------------------------- #
# Configuration – replace these with your real values
# --------------------------------------------------------------------------- #

# Approved API domains (only use URLs that point to these hosts)
APPROVED_API_DOMAINS: Iterable[str] = {
    "api.example.com",
    "services.example.org",
}

# Allowed endpoints – these are the only paths that may be requested
ALLOWED_ENDPOINTS: Iterable[str] = {
    "users",
    "orders",
    "products",
    "status",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(url: str) -> str:
    """
    Extracts and normalizes the hostname from a URL.
    Raises ValueError if the URL is malformed or has no network location.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: '{url}'")
    # Convert to lowercase for comparison
    return parsed.netloc.lower()

def _validate_domain(domain: str) -> None:
    """
    Ensure the domain is within the approved list.
    """
    if domain not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not approved")

def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is within the allowed list.
    """
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Mapping[str, str] | None = None,
) -> str:
    """
    Build a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        Base URL of the API (e.g. "https://api.example.com/v1").
    endpoint_name : str
        Endpoint to append (e.g. "users").
    params_dict : Mapping[str, str], optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        A safe, fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL contains an unapproved domain or disallowed endpoint.
    """
    # Parse and validate the base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Malformed base URL: '{main_url}'")

    # Validate domain
    _validate_domain(parsed_main.netloc)

    # Normalize and validate endpoint (strip leading/trailing slashes)
    clean_endpoint = endpoint_name.strip("/")
    _validate_endpoint(clean_endpoint)

    # Build the new path: combine existing path with endpoint
    base_path = parsed_main.path.rstrip("/")
    full_path = f"{base_path}/{clean_endpoint}"

    # Encode query parameters
    query_string = ""
    if params_dict:
        # Ensure values are strings; convert otherwise
        safe_params = {k: str(v) for k, v in params_dict.items()}
        query_string = urllib.parse.urlencode(safe_params)

    # Reconstruct the full URL
    final_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",          # params (deprecated)
        query_string,
        ""           # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (remove or guard with if __name__ == "__main__": in real code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com/v1",
            "/users/",
            {"id": 42, "format": "json"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")