# -*- coding: utf-8 -*-
"""
Utility for constructing safe redirect URLs to the API.

This module protects against open‑redirect attacks by validating that
the target domain and endpoint are explicitly approved.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Mapping

# --------------------------------------------------------------------------- #
# Configuration – populate these with your actual values
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Iterable[str] = (
    "api.example.com",
    "api.partner.org",
)

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v1/orders",
    "/v2/status",
)

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain string for comparison:
        - lower‑case
        - strip leading/trailing whitespace
    """
    return domain.strip().lower()


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether the given domain is in the list of approved domains.
    """
    return _normalize_domain(domain) in (_normalize_domain(d) for d in APPROVED_API_DOMAINS)


def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Check whether the given endpoint is in the list of allowed endpoints.
    The comparison is case‑sensitive because API paths are usually
    case‑sensitive. Leading/trailing slashes are normalised.
    """
    # Ensure endpoint starts with a slash
    ep = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    return ep in ALLOWED_ENDPOINTS


def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Mapping[str, str] | None = None,
) -> str:
    """
    Build a fully qualified API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The base API host, e.g. ``"https://api.example.com"``.
    desired_endpoint : str
        The specific endpoint path, e.g. ``"/v1/users"``.
    optional_params : Mapping[str, str] | None
        Optional query parameters to append.

    Returns
    -------
    str
        The fully constructed URL ready for redirection.

    Raises
    ------
    ValueError
        If the target domain or endpoint is not approved.
    """
    # Parse the base URL to extract components
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url_api must be a valid URL with scheme and host")

    # Validate domain
    if not _is_approved_domain(parsed_base.netloc):
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Validate endpoint
    if not _is_allowed_endpoint(desired_endpoint):
        raise ValueError(f"Unapproved endpoint: {desired_endpoint}")

    # Build the full path
    joined_path = urllib.parse.urljoin(parsed_base.path or "/", desired_endpoint)

    # Construct query string
    query = urllib.parse.urlencode(optional_params) if optional_params else ""

    # Re‑assemble the URL
    full_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            joined_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for real deployment)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: build a URL to fetch user data
    try:
        url = create_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "detail": "full"},
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")