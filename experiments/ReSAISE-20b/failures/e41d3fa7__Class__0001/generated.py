#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates that the resulting URL uses an approved domain and
endpoint.  This mitigates CWE‑610 by ensuring that external input cannot
direct the request to an arbitrary resource outside the trusted sphere.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – replace these with the actual values for your application.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "auth.example.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/items",
    "/v2/orders",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully‑qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The root of the API (e.g. "https://api.example.com").
    endpoint_path : str
        The specific endpoint to hit (e.g. "/v1/users").
    query_info : dict, optional
        Mapping of query string parameters.

    Returns
    -------
    str
        A fully qualified, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL resolves to an unapproved domain or uses a disallowed
        endpoint.  This protects against externally controlled references.
    """
    # ----------------------------------------------------------------------- #
    # Normalise and validate the base URL
    # ----------------------------------------------------------------------- #
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname!r}")

    # ----------------------------------------------------------------------- #
    # Normalise and validate the endpoint path
    # ----------------------------------------------------------------------- #
    # Reject paths that contain components other than a single slash separated
    # string (e.g., no ".." or "//").
    normalized_endpoint = urllib.parse.urljoin("/", endpoint_path)
    if not normalized_endpoint.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {endpoint_path!r}")

    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {normalized_endpoint!r}")

    # ----------------------------------------------------------------------- #
    # Construct the full URL
    # ----------------------------------------------------------------------- #
    # Join base and endpoint, preserving scheme & netloc.
    path = urllib.parse.urljoin(parsed_base.path or "/", normalized_endpoint)
    url_parts = list(parsed_base)
    url_parts[2] = path  # index 2 is the path component

    if query_info:
        # Encode query parameters safely
        url_parts[4] = urllib.parse.urlencode(query_info, doseq=True)

    full_url = urllib.parse.urlunparse(url_parts)

    # Final sanity check: re-parse to confirm domain and path
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Final URL resolved to unapproved domain: {final_parsed.hostname!r}")
    if final_parsed.path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Final URL uses disallowed endpoint: {final_parsed.path!r}")

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         link = generate_redirect_link(
#             "https://api.example.com",
#             "/v1/users",
#             {"id": "123", "format": "json"}
#         )
#         print(link)
#     except ValueError as e:
#         print(f"Error: {e}")