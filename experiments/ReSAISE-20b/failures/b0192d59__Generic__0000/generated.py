#!/usr/bin/env python3
"""
Utility for generating a secure API redirect URL.

The module validates the target domain and endpoint against predefined
allowlists before assembling the final URL. Optional query parameters can be
supplied as a dictionary and will be encoded safely.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Optional, Set, Iterable


# --------------------------------------------------------------------------- #
# 1. Allowlists
# --------------------------------------------------------------------------- #

# Example set of approved API domains.
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.internal.local",
}

# Example list of allowed API endpoints (paths).
ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v1/orders",
    "/v2/notifications",
)


# --------------------------------------------------------------------------- #
# 2. Core Function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API URL from a base URI, endpoint and optional
    query parameters.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g., ``https://api.example.com``).
    api_endpoint : str
        The endpoint path to be appended (e.g., ``/v1/users``).
    query : dict, optional
        Mapping of query keys to values. Values will be URL‑encoded.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain of ``base_uri`` is not in :data:`APPROVED_API_DOMAINS`
        or if ``api_endpoint`` is not in :data:`ALLOWED_ENDPOINTS`.
    """
    # ---------- Parse and validate base URI ----------
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    # Strip port for domain comparison
    netloc = parsed_base.netloc.split(":")[0]
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {netloc!r} is not approved")

    # ---------- Validate endpoint ----------
    # Normalise the endpoint to start with a single slash
    cleaned_endpoint = urllib.parse.urljoin("/", api_endpoint)
    if cleaned_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {cleaned_endpoint!r} is not allowed")

    # ---------- Build the final URL ----------
    # Join base path with endpoint
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", cleaned_endpoint.lstrip("/"))

    # Merge query parameters
    if query:
        # Ensure all values are strings for urlencode
        safe_query = {k: str(v) for k, v in query.items()}
        encoded_qs = urllib.parse.urlencode(safe_query)
    else:
        encoded_qs = ""

    # Reconstruct the URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",          # params
        encoded_qs,  # query
        "",          # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url


# --------------------------------------------------------------------------- #
# 3. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            base_uri="https://api.example.com",
            api_endpoint="/v1/users",
            query={"id": "123", "verbose": "true"},
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print(f"URL generation failed: {exc}")