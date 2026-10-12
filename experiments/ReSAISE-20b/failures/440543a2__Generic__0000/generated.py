#!/usr/bin/env python3
"""
Utility for safely constructing API redirect URLs.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: allowed domains and endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    # Add additional approved domains here
}

ALLOWED_ENDPOINTS = [
    "users",
    "posts",
    "comments",
    # Add additional allowed endpoints here
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URL by merging the base URL, endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    path : str
        The endpoint to append (e.g., "users" or "posts").
    params : dict, optional
        Dictionary of query parameters to include in the URL.

    Returns
    -------
    str
        The fully constructed, validated API URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint path is disallowed.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_url)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {parsed_base.hostname!r} is not approved for API redirects."
        )

    # Validate endpoint
    clean_path = path.lstrip("/")
    if clean_path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint {clean_path!r} is not allowed. Allowed endpoints: "
            f"{', '.join(ALLOWED_ENDPOINTS)}."
        )

    # Build the new path
    new_path = urllib.parse.urljoin(parsed_base.path + "/", clean_path)

    # Merge query parameters
    base_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)
    if params:
        # Ensure all values are strings; encode list for multiple values
        for k, v in params.items():
            if isinstance(v, list):
                base_query.setdefault(k, []).extend(map(str, v))
            else:
                base_query.setdefault(k, []).append(str(v))

    encoded_query = urllib.parse.urlencode(base_query, doseq=True)

    # Assemble the final URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        "",  # params (deprecated)
        encoded_query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com/v1",
            path="users",
            params={"id": "123", "verbose": "true"}
        )
        print("Constructed URL:", url)
    except ValueError as exc:
        print("Error:", exc)