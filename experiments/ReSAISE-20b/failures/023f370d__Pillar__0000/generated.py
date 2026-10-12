#!/usr/bin/env python3
"""
Utility for safely constructing API redirect URLs.

This module ensures that only pre‑approved domains and endpoints are used
to build the final redirect URL. It mitigates risks such as open redirects,
CWE‑664 (improper control of a resource through its lifetime) and other
security concerns by validating inputs before constructing the URL.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration:  Replace these with your real values.
# --------------------------------------------------------------------------- #

# A set of approved base API domains (e.g. "api.example.com").
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.foo.org",
}

# A list of allowed API endpoints (relative paths without leading slash).
ALLOWED_ENDPOINTS: Iterable[str] = [
    "v1/users",
    "v2/orders",
    "status/check",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the given netloc (host:port) belongs to an approved domain.
    Ports are ignored for simplicity; if you need port validation,
    adjust accordingly.
    """
    # Strip any port number for domain comparison
    host = netloc.split(":")[0]
    return host in APPROVED_API_DOMAINS


def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Verify that the endpoint is in the list of allowed endpoints.
    The comparison is case‑sensitive and expects no leading slash.
    """
    # Normalize endpoint: remove any leading/trailing slashes
    normalized = endpoint.strip("/")
    return normalized in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified API redirect URL.

    Parameters
    ----------
    base_api_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The relative endpoint path (e.g., "v1/users").
    query_options : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The complete redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # Validate inputs
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url!r}")

    if not _is_allowed_domain(parsed_base.netloc):
        raise ValueError(
            f"Domain '{parsed_base.netloc}' is not in the list of approved domains."
        )

    if not _is_allowed_endpoint(api_endpoint):
        raise ValueError(
            f"Endpoint '{api_endpoint}' is not an allowed API endpoint."
        )

    # Construct the path
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = api_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}"

    # Build the final URL
    base_url_with_path = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            "",  # query (to be added later)
            "",  # fragment
        )
    )

    if query_options:
        # Ensure values are strings; otherwise, raise TypeError
        for key, value in query_options.items():
            if not isinstance(value, str):
                raise TypeError(
                    f"Query parameter value for key '{key}' must be a string."
                )
        query_string = urllib.parse.urlencode(query_options)
        redirect_url = f"{base_url_with_path}?{query_string}"
    else:
        redirect_url = base_url_with_path

    return redirect_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_api_redirect(
            base_api_url="https://api.example.com",
            api_endpoint="/v1/users",
            query_options={"id": "123", "format": "json"},
        )
        print("Redirect URL:", url)
    except Exception as e:
        print(f"Error: {e}")