#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates that the resulting URL belongs to an approved
domain and uses one of a whitelist of endpoints.  This protects against
CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere).

Author: ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration:  Replace these with the actual values for your project.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "services.mydomain.org",
}
ALLOWED_ENDPOINTS: set[str] = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}


def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to call (e.g. "/v1/users").
    opts : Optional[Dict[str, str]]
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is not allowed.
    """
    if opts is None:
        opts = {}

    # Normalise base URL
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api!r}")

    # Verify domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {parsed_base.hostname!r} is not approved for API calls."
        )

    # Normalise endpoint
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Verify endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {api_endpoint!r} is not allowed.")

    # Construct the path
    full_path = urllib.parse.urljoin(parsed_base.path, api_endpoint)

    # Build query string
    if opts:
        # Sort parameters for deterministic output and to avoid duplicate keys
        query = urllib.parse.urlencode(
            sorted(opts.items()), doseq=True, safe=":/"
        )
    else:
        query = ""

    # Assemble the final URL
    redirect_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        "",  # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "format": "json"},
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")