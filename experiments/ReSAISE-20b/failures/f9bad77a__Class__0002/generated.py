#!/usr/bin/env python3
"""
Utility to safely construct a redirect URL for API calls.

The function ensures that the final URL uses an approved domain and
endpoint, mitigating CWE‑610 (externally controlled reference to a resource in another sphere).
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be populated with your trusted values
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Iterable[str] = (
    "api.example.com",
    "secure.api.org",
)

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v1/orders",
    "/v2/products",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_approved_domain(domain: str) -> bool:
    """Return True if the domain is in the approved list."""
    return domain.lower() in (d.lower() for d in APPROVED_API_DOMAINS)


def _is_allowed_endpoint(path: str) -> bool:
    """Return True if the path is in the allowed endpoint list."""
    return any(path.startswith(e) for e in ALLOWED_ENDPOINTS)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL from the base API URL, endpoint, and
    optional query parameters.

    Parameters
    ----------
    main_url : str
        Base URL of the API (e.g., "https://api.example.com").
    endpoint_name : str
        Endpoint path to append (e.g., "/v1/users").
    params_dict : dict, optional
        Dictionary of query parameters to encode.

    Returns
    -------
    str
        The fully qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting domain is not approved or the endpoint is disallowed.
    """
    # Normalize and parse base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Validate domain
    if not _is_approved_domain(parsed_main.netloc):
        raise ValueError(f"Domain {parsed_main.netloc!r} is not approved")

    # Ensure endpoint starts with a slash
    endpoint = endpoint_name if endpoint_name.startswith("/") else f"/{endpoint_name}"

    # Validate endpoint
    if not _is_allowed_endpoint(endpoint):
        raise ValueError(f"Endpoint {endpoint!r} is not allowed")

    # Build the full path
    joined_path = urllib.parse.urljoin(parsed_main.path or "/", endpoint)

    # Encode query parameters if provided
    query = urllib.parse.urlencode(params_dict or {}, doseq=True)

    # Reconstruct the final URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            joined_path,
            "",          # params
            query,       # query
            "",          # fragment
        )
    )

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "verbose": "true"}
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")