#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function ensures that the resulting URL points only to approved
domains and uses an allowed endpoint.  It accepts optional query
parameters, which are URL‑encoded safely.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – in a real project these would come from a secure config
# file or environment variables.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.mycorp.io",
    # Add more approved domains here
}

ALLOWED_ENDPOINTS: set[str] = {
    "/v1/users",
    "/v2/orders",
    "/status",
    # Add more safe endpoints here
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(url: str) -> str:
    """
    Extract the hostname from a URL and normalize it to lowercase.
    Raises ValueError if the URL is malformed or missing a hostname.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    return parsed.hostname.lower()


def _ensure_allowed_domain(base_url: str) -> None:
    """
    Verify that the base URL's domain is in APPROVED_API_DOMAINS.
    Raises ValueError if it is not allowed.
    """
    domain = _normalize_domain(base_url)
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for API redirects.")


def _ensure_allowed_endpoint(endpoint: str) -> None:
    """
    Verify that the endpoint is in ALLOWED_ENDPOINTS.
    Raises ValueError if it is not allowed.
    """
    # Ensure the endpoint starts with a slash for comparison
    normalized = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized}' is not allowed.")


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint to append (e.g., "/v1/users").
    opts : dict[str, str], optional
        Optional query parameters.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # 1. Validate inputs
    _ensure_allowed_domain(base_url_api)
    _ensure_allowed_endpoint(api_endpoint)

    # 2. Build the URL
    # urljoin handles missing slashes appropriately.
    base = base_url_api.rstrip("/")
    endpoint = api_endpoint.lstrip("/")
    full_path = f"{base}/{endpoint}"

    # 3. Append query parameters if provided
    if opts:
        # Ensure all keys and values are strings to avoid surprises.
        safe_opts = {str(k): str(v) for k, v in opts.items()}
        query_string = urllib.parse.urlencode(safe_opts)
        full_path += f"?{query_string}"

    return full_path


# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "format": "json"}
        )
        print(f"Redirect URL: {url}")
    except ValueError as e:
        print(f"Error: {e}")