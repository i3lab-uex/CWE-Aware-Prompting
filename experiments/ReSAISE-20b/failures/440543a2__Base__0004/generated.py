#!/usr/bin/env python3
"""
Secure API redirect URL builder.

This module provides a single function `create_api_redirect_link` that
constructs an API URL from a base URL, a target endpoint path and optional
query parameters.  The function performs strict validation of the domain
and endpoint to mitigate CWE‑601 (Open Redirect) attacks.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional


# --------------------------------------------------------------------------- #
# Configuration – these should be populated with the real values for your
# deployment environment.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "secure.api.org",
}  # Example approved domains

ALLOWED_ENDPOINTS: Iterable[str] = [
    "/v1/users",
    "/v1/orders",
    "/v2/items",
]  # Example allowed paths


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API URL by merging `base_url` with `path`
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        The API's base URL (e.g. "https://api.example.com").
    path : str
        The target endpoint path (e.g. "/v1/users").
    params : dict[str, str], optional
        Key/value pairs to be appended as query parameters.

    Returns
    -------
    str
        The fully-qualified, validated API URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    if not base_url:
        raise ValueError("base_url must be a non-empty string")
    if not path:
        raise ValueError("path must be a non-empty string")

    # Normalise the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base_url: {base_url!r}")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Combine base and path safely
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", path.lstrip("/"))
    # Normalize the resulting path
    normalized_path = urllib.parse.urlparse(combined_path).path

    # Validate the endpoint
    if not any(
        normalized_path.startswith(endpoint.rstrip("/"))
        for endpoint in ALLOWED_ENDPOINTS
    ):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Build the query string
    query = urllib.parse.urlencode(params or {})

    # Assemble final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        normalized_path,
        "",  # params (unused)
        query,
        "",
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com",
            path="/v1/users",
            params={"page": "2", "limit": "50"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")