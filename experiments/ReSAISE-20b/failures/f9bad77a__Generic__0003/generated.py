#!/usr/bin/env python3
"""
Utility to construct a fully-qualified API redirect URL.

The module validates that the base URL belongs to an approved domain
and that the requested endpoint is allowed.  It then builds a new URL
with an optional query string.
"""

from urllib.parse import urlparse, urlencode, urlunparse, ParseResult
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – in a real project these would be imported from
# a dedicated configuration module or environment variables.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "auth.example.com",
    "service.example.org",
}

ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "login",
    "logout",
}

# ----------------------------------------------------------------------
# Helper function
# ----------------------------------------------------------------------
def _is_approved_domain(netloc: str) -> bool:
    """Return True if the netloc (host[:port]) belongs to an approved domain."""
    # Strip port number for comparison
    host = netloc.split(":")[0].lower()
    return host in APPROVED_API_DOMAINS


def _is_allowed_endpoint(endpoint: str) -> bool:
    """Return True if the endpoint is in the allowed list."""
    return endpoint.lower() in ALLOWED_ENDPOINTS


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base API URL (e.g. "https://api.example.com/v1").
    endpoint_name : str
        The desired API endpoint (e.g. "users").
    params_dict : dict, optional
        A dictionary of query string parameters.

    Returns
    -------
    str
        The complete, validated redirect URL.

    Raises
    ------
    ValueError
        If the base URL's domain is not approved or if the endpoint
        is not in the allowed list.
    """
    # Parse and validate the main URL
    parsed_main = urlparse(main_url)
    if not _is_approved_domain(parsed_main.netloc):
        raise ValueError(f"Domain '{parsed_main.netloc}' is not approved.")

    if parsed_main.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed_main.scheme}'. "
                         f"Only http and https are allowed.")

    # Validate endpoint
    if not _is_allowed_endpoint(endpoint_name):
        raise ValueError(f"Endpoint '{endpoint_name}' is not allowed.")

    # Construct the new path
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = f"/{endpoint_name.lstrip('/')}"
    new_path = f"{base_path}{endpoint_path}"

    # Encode query parameters
    query = urlencode(params_dict or {}, doseq=True)

    # Rebuild the URL
    new_parsed = ParseResult(
        scheme=parsed_main.scheme,
        netloc=parsed_main.netloc,
        path=new_path,
        params="",
        query=query,
        fragment=""
    )
    return urlunparse(new_parsed)


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example 1: Simple endpoint
    url = construct_redirect_url(
        "https://api.example.com/v1",
        "users"
    )
    print(url)  # https://api.example.com/v1/users

    # Example 2: With query parameters
    url = construct_redirect_url(
        "https://auth.example.com/v2",
        "login",
        {"client_id": "abc123", "redirect_uri": "https://myapp.com/callback"}
    )
    print(url)