#!/usr/bin/env python3
"""
Utility to safely construct a redirect URL for an API request.

The function validates that the base API URL belongs to one of the
approved domains and that the requested endpoint is on an allow‑list.
It then merges any supplied query parameters into a well‑formed URL.

The implementation mitigates CWE‑610 by preventing externally controlled
references to resources outside the intended domain sphere.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable


# --------------------------------------------------------------------------- #
# Configuration – these should be defined in a secure location (e.g. env vars)
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "secure.api.net",
}
ALLOWED_ENDPOINTS: Iterable[str] = [
    "/users",
    "/posts",
    "/comments",
    "/search",
]


def _is_allowed_domain(netloc: str) -> bool:
    """Check if the network location is within an approved domain."""
    # Remove port number if present
    host = netloc.split(":")[0].lower()
    return host in APPROVED_API_DOMAINS


def _is_allowed_endpoint(path: str) -> bool:
    """Verify that the endpoint path is on the allow‑list."""
    # Normalise to a single leading slash
    normalized = "/" + path.lstrip("/")
    return normalized in ALLOWED_ENDPOINTS


def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified redirect URL for an API call.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g. "/users" or "posts").
    query_options : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    if not base_api_url:
        raise ValueError("Base API URL must be provided")

    # Parse the base URL and ensure it is absolute
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base API URL must be a full absolute URL")

    # Validate domain
    if not _is_allowed_domain(parsed_base.netloc):
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalise endpoint path
    if not api_endpoint:
        raise ValueError("API endpoint must be provided")

    # Prevent path traversal or relative paths
    if ".." in api_endpoint:
        raise ValueError("API endpoint contains disallowed path traversal")

    normalized_path = "/" + api_endpoint.lstrip("/")
    if not _is_allowed_endpoint(normalized_path):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Merge the base URL and endpoint
    joined = urllib.parse.urljoin(parsed_base.geturl(), normalized_path)

    # Append query parameters safely
    if query_options:
        if not isinstance(query_options, dict):
            raise ValueError("query_options must be a dictionary")
        # Encode parameters; ensure values are strings
        encoded = urllib.parse.urlencode(
            {k: str(v) for k, v in query_options.items()}
        )
        joined = f"{joined}?{encoded}"

    return joined


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     url = construct_api_redirect(
#         "https://api.example.com",
#         "/users",
#         {"id": 42, "verbose": "true"}
#     )
#     print(url)