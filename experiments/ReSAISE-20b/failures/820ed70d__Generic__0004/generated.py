#!/usr/bin/env python3
"""
Utility to safely assemble an API redirect URL.

The module defines:
- APPROVED_API_DOMAINS: set of allowed domain names.
- ALLOWED_ENDPOINTS: list of permitted endpoint paths.

The core function, `assemble_api_redirect_link`, validates the domain and
endpoint before constructing a fully‑qualified URL with optional query
parameters. It uses urllib.parse for robust URL handling.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional


# --------------------------------------------------------------------------- #
# Configuration – adjust these to your environment
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS: list[str] = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Assemble a safe API redirect URL.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g. ``https://api.example.com``).
    api_path : str
        The API endpoint path (e.g. ``/v1/users``).
    query_dict : dict[str, str] | None, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL to validate scheme and extract netloc
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or parsed_base.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme!r}")

    # Domain validation
    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not approved")

    # Endpoint validation
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {api_path!r} is not allowed")

    # Construct the new URL by merging base and path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))
    new_parsed = parsed_base._replace(path=joined_path)

    # Add query parameters if provided
    if query_dict:
        # Ensure all keys/values are strings; encode accordingly
        encoded_query = urllib.parse.urlencode(
            {str(k): str(v) for k, v in query_dict.items()}
        )
        new_parsed = new_parsed._replace(query=encoded_query)

    # Rebuild the full URL
    final_url = urllib.parse.urlunparse(new_parsed)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            base_api_url="https://api.example.com",
            api_path="/v1/users",
            query_dict={"page": "2", "limit": "50"},
        )
        print(f"Redirect URL: {url}")
    except ValueError as exc:
        print(f"URL assembly failed: {exc}")