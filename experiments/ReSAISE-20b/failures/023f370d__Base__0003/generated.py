#!/usr/bin/env python3
"""
Utility to safely construct an API redirect URL.

The function ensures that the resulting URL:
* points to a pre‑approved domain
* uses an allowed endpoint
* correctly encodes optional query parameters

This protects against CWE‑601 (Open Redirect) by validating user input.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable


# --------------------------------------------------------------------------- #
# Configuration – these would normally come from a secure config file
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.foo.org",
    "secure.api.net",
}

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v2/orders",
    "/health",
    "/status",
)


def _normalize_domain(netloc: str) -> str:
    """
    Normalise a hostname for comparison.

    Parameters
    ----------
    netloc : str
        The network location part of a URL (e.g. 'api.example.com:443').

    Returns
    -------
    str
        Lower‑case hostname without port.
    """
    host = netloc.split(":")[0].lower()
    return host


def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to append (e.g. "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS`` or the endpoint is
        not listed in ``ALLOWED_ENDPOINTS``.
    """
    # Parse base URL to extract scheme and netloc
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Validate domain
    host = _normalize_domain(parsed_base.netloc)
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")

    # Validate endpoint
    if not api_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Build the path by joining base path and endpoint
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Encode query parameters if provided
    query_string = ""
    if query_options:
        if not isinstance(query_options, dict):
            raise ValueError("query_options must be a dictionary")
        query_string = urllib.parse.urlencode(query_options, doseq=True)

    # Assemble the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            joined_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_api_redirect(
            base_api_url="https://api.example.com",
            api_endpoint="/v1/users",
            query_options={"page": "2", "limit": "50"},
        )
        print("Redirect URL:", url)
    except ValueError as e:
        print(f"Error: {e}")