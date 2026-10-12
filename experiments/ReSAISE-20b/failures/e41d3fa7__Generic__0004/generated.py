#!/usr/bin/env python3
"""
Utility to build a secure redirect URL for API requests.

The function validates that the base URL belongs to an approved domain and
that the requested endpoint is on a whitelist. It also safely encodes any
query parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be populated with real values in production.
# --------------------------------------------------------------------------- #

# A set of fully-qualified domains that are allowed as the base API host.
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.trusted.org",
}

# A list (or set) of endpoint paths that are permitted.
ALLOWED_ENDPOINTS: set[str] = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The root API URL (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint (e.g., "/users").
    query_info : dict[str, str] | None, optional
        Dictionary of query string parameters to append.

    Returns
    -------
    str
        A fully qualified, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain of `base_url` is not in :data:`APPROVED_API_DOMAINS`
        or if `endpoint_path` is not in :data:`ALLOWED_ENDPOINTS`.
    """
    # --------------------------------------------------------------------- #
    # Parse the base URL and validate domain
    # --------------------------------------------------------------------- #
    parsed_base = urllib.parse.urlparse(base_url)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Normalize the domain to lower case for comparison
    base_domain = parsed_base.hostname.lower() if parsed_base.hostname else ""

    if base_domain not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {base_domain!r} not approved. "
            f"Allowed domains: {sorted(APPROVED_API_DOMAINS)}"
        )

    # --------------------------------------------------------------------- #
    # Validate the endpoint
    # --------------------------------------------------------------------- #
    # Ensure endpoint_path starts with a slash and is in the whitelist.
    if not endpoint_path.startswith("/"):
        endpoint_path = "/" + endpoint_path

    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint {endpoint_path!r} is not allowed. "
            f"Allowed endpoints: {sorted(ALLOWED_ENDPOINTS)}"
        )

    # --------------------------------------------------------------------- #
    # Construct the full URL
    # --------------------------------------------------------------------- #
    # Merge the base path (if any) with the endpoint.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # Build the query string
    if query_info:
        encoded_query = urllib.parse.urlencode(query_info, doseq=True)
    else:
        encoded_query = ""

    # Reassemble the URL
    redirect_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        "",  # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url

# --------------------------------------------------------------------------- #
# Example usage (remove or guard with __name__ == "__main__" in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            "https://api.example.com",
            "/users",
            {"page": "2", "sort": "asc"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")