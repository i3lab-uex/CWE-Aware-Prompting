#!/usr/bin/env python3
"""
Utility to construct a safe API redirect URL.

The function validates that the target domain and endpoint are
whitelisted before assembling the final URL.  This protects against
CWE‑601: Open Redirect vulnerabilities.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Whitelists – adjust these to match your application's policy.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "services.example.org",
}

ALLOWED_ENDPOINTS: set[str] = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(url: str) -> str:
    """
    Extract the network location (domain + port) from a URL
    and convert it to lowercase for comparison.
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.lower()

def _validate_domain(domain: str) -> None:
    """
    Raise ValueError if the domain is not in APPROVED_API_DOMAINS.
    """
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")

def _validate_endpoint(endpoint: str) -> None:
    """
    Raise ValueError if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    # Normalise leading slash
    normalized = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {normalized}")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified API URL.

    Parameters
    ----------
    base_url : str
        The root URL of the API (e.g. "https://api.example.com").
    path : str
        The specific endpoint to hit (e.g. "/v1/users").
    params : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        A validated and encoded URL ready for redirecting the user.

    Raises
    ------
    ValueError
        If the domain or endpoint is not in the respective whitelists.
    """
    # 1. Validate base URL domain
    domain = _normalize_domain(base_url)
    _validate_domain(domain)

    # 2. Validate endpoint
    _validate_endpoint(path)

    # 3. Build the URL components
    parsed_base = urllib.parse.urlparse(base_url)

    # Ensure that we don't inadvertently strip a trailing slash
    # from the base URL when joining paths.
    joined_path = urllib.parse.urljoin(parsed_base.path, path)

    # 4. Encode query parameters
    query = urllib.parse.urlencode(params or {})

    # 5. Reassemble the URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",  # params (deprecated)
        query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com",
            path="/v1/users",
            params={"id": "123", "view": "full"}
        )
        print(f"Redirect URL: {url}")
    except ValueError as exc:
        print(f"Invalid request: {exc}")