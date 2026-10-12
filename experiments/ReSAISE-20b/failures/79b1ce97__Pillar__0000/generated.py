#!/usr/bin/env python3
"""
Utility to build a secure redirect URL for API calls.

The function validates that the resulting URL is within an approved
domain list and that the requested endpoint is allowed.  It uses
`urllib.parse` to construct URLs safely, avoiding common pitfalls such as
URL injection or double‑encoding.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Mapping, MutableMapping, Optional

# --------------------------------------------------------------------------- #
# Configuration:  Define the set of domains and endpoints that are trusted.
# These can be populated from environment variables or a config file in
# production.  For illustration purposes, they are hard‑coded here.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS: Iterable[str] = {
    "api.example.com",
    "services.internal.company.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #
def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain by stripping any leading scheme or path.
    Example: "https://api.example.com/v1" -> "api.example.com"
    """
    parsed = urllib.parse.urlparse(domain)
    return parsed.netloc or domain

def _is_domain_approved(url: str) -> bool:
    """
    Check whether the domain of `url` is in the approved list.
    """
    parsed = urllib.parse.urlparse(url)
    domain = _normalize_domain(parsed.netloc)
    return domain in APPROVED_API_DOMAINS

def _is_endpoint_allowed(endpoint: str) -> bool:
    """
    Verify that the endpoint is in the allowed list.
    Leading/trailing slashes are normalised to avoid false negatives.
    """
    normalized = endpoint.strip()
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    return normalized in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #
def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Mapping[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The base URL of the API (e.g., "https://api.example.com").
    desired_endpoint : str
        The specific endpoint to hit (e.g., "/users").
    optional_params : Mapping[str, str] | None
        Optional query parameters to include in the URL.

    Returns
    -------
    str
        A fully‑qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL points to an unapproved domain or uses a
        disallowed endpoint.
    """
    # Ensure the base URL is parsed correctly
    base_parsed = urllib.parse.urlparse(base_url_api)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api!r}")

    # Validate domain
    if not _is_domain_approved(base_url_api):
        raise ValueError(f"Domain not approved: {base_parsed.netloc!r}")

    # Validate endpoint
    if not _is_endpoint_allowed(desired_endpoint):
        raise ValueError(f"Endpoint not allowed: {desired_endpoint!r}")

    # Build the path
    base_path = base_parsed.path.rstrip("/")
    endpoint_path = desired_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}"

    # Encode query parameters safely
    query_string = ""
    if optional_params:
        if not isinstance(optional_params, Mapping):
            raise TypeError("optional_params must be a mapping type")
        # Convert all values to strings and encode
        query_string = urllib.parse.urlencode(
            {k: str(v) for k, v in optional_params.items()}
        )

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            base_parsed.scheme,
            base_parsed.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    # Final safety check: ensure the domain hasn't changed due to manipulation
    if not _is_domain_approved(final_url):
        raise ValueError("Final URL domain mismatch after construction")

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = create_redirect_url(
            "https://api.example.com",
            "/users",
            {"id": 123, "verbose": True},
        )
        print("Redirect URL:", url)
    except Exception as exc:
        print(f"Error: {exc}")