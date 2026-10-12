#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates the base domain and endpoint against whitelists
to mitigate CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere).
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional


# --------------------------------------------------------------------------- #
# Whitelists – update these to match your environment
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.internal.company.net",
}

ALLOWED_ENDPOINTS: set[str] = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified API URL from a base, path and optional query parameters.

    Parameters
    ----------
    base_url : str
        Base URL of the API, e.g. "https://api.example.com".
    path : str
        Endpoint path relative to the base, e.g. "/users".
    params : dict[str,str], optional
        Query parameters to append.

    Returns
    -------
    str
        The assembled, validated URL.

    Raises
    ------
    ValueError
        If the base domain is not in ``APPROVED_API_DOMAINS`` or if the
        path is not one of the ``ALLOWED_ENDPOINTS``.
    """
    # --------------------------------------------------------------------- #
    # Validate base URL
    # --------------------------------------------------------------------- #
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Normalize the domain (lowercase, strip port)
    host = parsed_base.hostname
    if not host:
        raise ValueError(f"Could not determine hostname from base URL: {base_url!r}")

    if host.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host!r}")

    # --------------------------------------------------------------------- #
    # Validate path
    # --------------------------------------------------------------------- #
    if not path.startswith("/"):
        raise ValueError(f"Path must start with '/': {path!r}")

    # Normalise path to avoid duplicate slashes
    normalized_path = urllib.parse.urljoin("/", path)

    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {normalized_path!r}")

    # --------------------------------------------------------------------- #
    # Build the final URL
    # --------------------------------------------------------------------- #
    base_without_path = urllib.parse.urlunparse(
        (parsed_base.scheme, parsed_base.netloc, "", "", "", "")
    )
    full_path = urllib.parse.urljoin(base_without_path + "/", normalized_path.lstrip("/"))

    if params:
        # Ensure all keys and values are strings; encode any other types
        encoded_params = {
            str(k): str(v) for k, v in params.items()
        }
        query_string = urllib.parse.urlencode(encoded_params)
        final_url = f"{full_path}?{query_string}"
    else:
        final_url = full_path

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com",
            path="/users",
            params={"id": "123", "format": "json"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")