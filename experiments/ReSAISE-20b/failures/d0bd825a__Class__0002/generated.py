#!/usr/bin/env python3
"""
Utility for safely generating an API redirect URL.

The function validates that the resulting URL belongs to a pre‑approved domain
and that its endpoint is on an allow list.  Query parameters are encoded with
`urllib.parse.urlencode` to avoid injection vulnerabilities.

Security Note:
    This module mitigates CWE‑610 by ensuring that the final URL cannot point
    to a domain or endpoint outside of the intended control sphere.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – in a real application these would come from settings
# --------------------------------------------------------------------------- #

# Set of approved API base domains (e.g. "api.example.com")
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "service.internal.company",
}

# List of allowed endpoint paths (relative to the base URL, no leading slash)
ALLOWED_ENDPOINTS: list[str] = [
    "v1/users",
    "v2/orders",
    "healthcheck",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.

    The function lower‑cases the domain and removes any trailing dots.
    """
    return domain.lower().rstrip(".")

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the domain is in the set of approved domains.
    """
    return _normalize_domain(domain) in {_normalize_domain(d) for d in APPROVED_API_DOMAINS}

def _is_allowed_endpoint(path: str) -> bool:
    """
    Check if the endpoint path is in the list of allowed endpoints.

    The comparison ignores a leading slash.
    """
    normalized = path.lstrip("/")
    return normalized in ALLOWED_ENDPOINTS

# --------------------------------------------------------------------------- #
# Main API
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
        Base address of the API, e.g. "https://api.example.com".
    api_endpoint : str
        Endpoint path relative to the base URL, e.g. "/v1/users".
    opts : Optional[Dict[str, str]]
        Query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed redirect URL that has been validated against the
        approved domain and endpoint lists.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an approved domain or if the
        endpoint is not in the allowed list.
    """
    # Parse the base URL to validate its domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    if not _is_allowed_domain(parsed_base.netloc):
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Join the base URL and endpoint safely
    joined_url = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", api_endpoint.lstrip("/"))

    # Parse the joined URL to validate the endpoint
    parsed_joined = urllib.parse.urlparse(joined_url)
    if not _is_allowed_endpoint(parsed_joined.path):
        raise ValueError(f"Endpoint '{parsed_joined.path}' is not allowed")

    # Encode query parameters if provided
    query = urllib.parse.urlencode(opts) if opts else ""
    # Build the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_joined.scheme,
            parsed_joined.netloc,
            parsed_joined.path,
            parsed_joined.params,
            query,
            parsed_joined.fragment,
        )
    )

    return final_url