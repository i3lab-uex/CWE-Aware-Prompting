#!/usr/bin/env python3
"""
Utility for building secure API redirect URLs.

The function ensures that the resulting URL:
* points to a pre‑approved domain,
* uses one of the allowed endpoints, and
* safely encodes any supplied query parameters.

This protects against CWE‑601 (Open Redirect) by preventing redirects to
untrusted sites.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Any

# --------------------------------------------------------------------------- #
# Configuration – in a real project these would come from settings or env
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/items",
    "/health",
]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Construct a fully‑qualified API redirect URL.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path (e.g., "/v1/users").
    opts : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        A fully constructed, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # --- Validate and normalise base URL ------------------------------------
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api!r}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {parsed_base.hostname!r} is not in the list of approved API domains."
        )

    # --- Validate endpoint -----------------------------------------------
    # Normalise to start with a single leading slash
    endpoint = api_endpoint.lstrip("/")
    endpoint_path = f"/{endpoint}"
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint {endpoint_path!r} is not allowed. Allowed endpoints: "
            f"{', '.join(sorted(ALLOWED_ENDPOINTS))}"
        )

    # --- Build the URL -----------------------------------------------
    # Join base and endpoint safely
    full_url = urllib.parse.urljoin(parsed_base.geturl(), endpoint_path)

    # Append query parameters if provided
    if opts:
        # Convert all values to strings and encode
        query = urllib.parse.urlencode({k: str(v) for k, v in opts.items()})
        full_url = f"{full_url}?{query}"

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (remove or guard with if __name__ == "__main__": in real code)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"page": 2, "sort": "name"},
        )
        print(url)
    except ValueError as exc:
        print(f"URL creation failed: {exc}")