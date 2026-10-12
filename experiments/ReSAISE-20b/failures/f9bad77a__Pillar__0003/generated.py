# -*- coding: utf-8 -*-

"""
Utility for constructing secure API redirect URLs.

The module validates that the resulting URL uses a trusted domain and
endpoint before returning it.  This prevents accidental or malicious
redirects to unapproved services.

Author: Your Name
License: MIT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration:  Trusted domains and allowed endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.example.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/users",
    "/orders",
    "/products",
    "/search",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_domain(url: str) -> Optional[str]:
    """
    Extract the hostname from a URL and return it in lowercase.
    Return ``None`` if parsing fails or no netloc is present.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.hostname.lower() if parsed.hostname else None
    except Exception:
        return None


def _validate_domain(hostname: str) -> bool:
    """
    Check if the hostname belongs to an approved domain.
    """
    return hostname in APPROVED_API_DOMAINS


def _validate_endpoint(endpoint: str) -> bool:
    """
    Check if the endpoint is in the list of allowed endpoints.
    Normalise leading slashes for comparison.
    """
    normalized = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    return normalized in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a full API redirect URL by combining the base URL, endpoint,
    and optional query parameters.

    Parameters
    ----------
    main_url : str
        Base API URL (e.g., ``https://api.example.com``).
    endpoint_name : str
        API endpoint path (e.g., ``/users`` or ``users``).
    params_dict : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        A fully qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL uses an unapproved domain or endpoint.
    """
    if not main_url:
        raise ValueError("main_url must be a non-empty string")

    # Ensure the main URL has a scheme
    if not urllib.parse.urlparse(main_url).scheme:
        raise ValueError("main_url must include a scheme (e.g., 'https://')")

    # Parse the base URL to extract its components
    parsed_main = urllib.parse.urlparse(main_url)

    # Normalise the endpoint path
    normalized_endpoint = (
        endpoint_name if endpoint_name.startswith("/") else f"/{endpoint_name}"
    )

    # Validate domain
    hostname = _normalize_domain(main_url)
    if not hostname or not _validate_domain(hostname):
        raise ValueError(f"Unapproved domain in URL: {hostname!r}")

    # Validate endpoint
    if not _validate_endpoint(normalized_endpoint):
        raise ValueError(f"Unapproved endpoint: {normalized_endpoint!r}")

    # Build the new path
    new_path = urllib.parse.urljoin(parsed_main.path, normalized_endpoint)

    # Merge existing query parameters from the base URL with the new ones
    original_query = urllib.parse.parse_qs(parsed_main.query, keep_blank_values=True)
    # Flatten original query to single values for simplicity
    merged_query = {k: v[0] if len(v) == 1 else v for k, v in original_query.items()}

    # Update with new params
    if params_dict:
        for key, value in params_dict.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("Query parameter keys and values must be strings")
            merged_query[key] = value

    # Encode the query string
    encoded_query = urllib.parse.urlencode(merged_query, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            new_path,
            "",  # params
            encoded_query,
            "",  # fragment
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            main_url="https://api.example.com",
            endpoint_name="/users",
            params_dict={"id": "123", "verbose": "true"},
        )
        print("Constructed URL:", url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")