#!/usr/bin/env python3
"""
Utility for generating a secure API redirect URL.

This module defines `create_api_redirect_link`, which safely
constructs an absolute URL from a base API endpoint, a target path,
and optional query parameters. It validates that the resulting URL
points to an approved domain and uses a whitelisted endpoint,
preventing open redirect or arbitrary request forgery vulnerabilities.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable

# --------------------------------------------------------------------------- #
# Configuration: Allowed domains and endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.secure.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.

    Parameters
    ----------
    domain : str
        Domain to normalise (e.g., 'API.EXAMPLE.COM').

    Returns
    -------
    str
        Lower‑cased domain without surrounding whitespace.
    """
    return domain.strip().lower()


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether a domain is approved.

    Parameters
    ----------
    domain : str
        Domain to check.

    Returns
    -------
    bool
        True if the domain is in ``APPROVED_API_DOMAINS``.
    """
    return _normalize_domain(domain) in APPROVED_API_DOMAINS


def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Check whether a path is in the whitelist of allowed endpoints.

    Parameters
    ----------
    endpoint : str
        The path component of a URL (e.g., '/v1/users').

    Returns
    -------
    bool
        True if the endpoint is in ``ALLOWED_ENDPOINTS``.
    """
    return endpoint in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified API URL from a base, path and optional query
    parameters while enforcing domain and endpoint restrictions.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g., 'https://api.example.com').
    path : str
        The endpoint path to be appended (e.g., '/v1/users').
    params : Optional[Dict[str, str]]
        Query parameters to include in the URL.

    Returns
    -------
    str
        The fully constructed and validated API URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a
        disallowed endpoint.
    """
    # ----------------------------------------------------------------------- #
    # 1. Parse and normalise the base URL
    # ----------------------------------------------------------------------- #
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: '{base_url}'")

    # ----------------------------------------------------------------------- #
    # 2. Validate the domain
    # ----------------------------------------------------------------------- #
    if not _is_approved_domain(parsed_base.netloc):
        raise ValueError(f"Unapproved domain: '{parsed_base.netloc}'")

    # ----------------------------------------------------------------------- #
    # 3. Normalise the path
    # ----------------------------------------------------------------------- #
    if not path.startswith("/"):
        raise ValueError(f"Endpoint path must start with '/': '{path}'")

    if not _is_allowed_endpoint(path):
        raise ValueError(f"Disallowed endpoint: '{path}'")

    # ----------------------------------------------------------------------- #
    # 4. Build the final URL
    # ----------------------------------------------------------------------- #
    # Use urljoin to safely combine base and path; it handles trailing slashes.
    full_url = urllib.parse.urljoin(parsed_base.geturl(), path)

    # Append query parameters if provided
    if params:
        # Encode parameters; ensure all keys and values are strings.
        encoded_params = urllib.parse.urlencode(
            {str(k): str(v) for k, v in params.items()}
        )
        full_url = f"{full_url}?{encoded_params}"

    # ----------------------------------------------------------------------- #
    # 5. Final domain check (in case path contains a scheme override)
    # ----------------------------------------------------------------------- #
    final_parsed = urllib.parse.urlparse(full_url)
    if not _is_approved_domain(final_parsed.netloc):
        raise ValueError(f"Resulting URL points to unapproved domain: '{final_parsed.netloc}'")

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com",
            path="/v1/users",
            params={"id": "123", "active": "true"},
        )
        print(f"Constructed URL: {url}")
    except ValueError as exc:
        print(f"Error: {exc}")