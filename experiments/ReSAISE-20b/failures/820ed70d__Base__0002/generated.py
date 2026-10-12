#!/usr/bin/env python3
"""
Utility to safely assemble an API redirect URL.

The function validates the target domain and endpoint against whitelists
to mitigate CWE‑601 (open redirect) vulnerabilities.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, List


# --------------------------------------------------------------------------- #
# Whitelists – populate these with your actual allowed values
# --------------------------------------------------------------------------- #

# Example: approved API domains (scheme‑agnostic)
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.internal.local",
}

# Example: allowed API paths (absolute paths, starting with '/')
ALLOWED_ENDPOINTS: List[str] = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_path(path: str) -> str:
    """
    Normalise a URL path to eliminate '..' and duplicate slashes.
    Ensures the result is an absolute path starting with '/'.
    """
    # urlparse treats empty path as ''
    if not path:
        return "/"

    # Ensure leading slash
    if not path.startswith("/"):
        path = "/" + path

    # Normalize the path (removes '..' and '.')
    normalized = urllib.parse.urljoin("/", path)
    # urljoin may strip trailing slash; preserve it if original had one
    if path.endswith("/") and not normalized.endswith("/"):
        normalized += "/"
    return normalized


def _validate_domain(netloc: str) -> None:
    """
    Validate that the hostname part of netloc is in the approved list.
    Raises ValueError if not.
    """
    # Extract hostname (ignore port)
    host = netloc.split(":")[0]
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")


def _validate_endpoint(path: str) -> None:
    """
    Validate that the path is in the allowed endpoints list.
    Raises ValueError if not.
    """
    # Normalize for comparison
    norm_path = _normalize_path(path)
    if norm_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {norm_path}")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Assemble a fully qualified API URL for redirection.

    Parameters
    ----------
    base_api_url : str
        The base API URL (e.g. "https://api.example.com").
    api_path : str
        The endpoint path (e.g. "/v1/users").
    query_dict : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url}")

    # Validate domain
    _validate_domain(parsed_base.netloc)

    # Normalize and validate the endpoint path
    normalized_path = _normalize_path(api_path)
    _validate_endpoint(normalized_path)

    # Merge paths: base path may have trailing slash; ensure proper join
    merged_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_path)

    # Build query string
    if query_dict:
        # Ensure all values are strings; convert otherwise
        safe_query = {
            str(k): str(v) for k, v in query_dict.items()
        }
        query_string = urllib.parse.urlencode(safe_query)
    else:
        query_string = ""

    # Reconstruct the full URL
    assembled_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        merged_path,
        "",  # params
        query_string,
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(assembled_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            base_api_url="https://api.example.com",
            api_path="/v1/users",
            query_dict={"id": "123", "verbose": "true"},
        )
        print("Assembled URL:", url)
    except ValueError as e:
        print("Validation error:", e)