#!/usr/bin/env python3
"""
Utility for safely assembling API redirect URLs.

The function `assemble_api_redirect_link` validates that the
constructed URL belongs to an approved domain and uses a whitelisted
endpoint before returning the fully‑qualified URL.  It also accepts an
optional dictionary of query parameters that are properly encoded.

Security note:
- This code protects against CWE‑610 (Externally Controlled
  Reference to a Resource in Another Sphere) by ensuring that the
  domain and path are explicitly whitelisted.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional, Set


# --------------------------------------------------------------------------- #
# Configuration:  Replace these with your real values
# --------------------------------------------------------------------------- #

# Approved API domains (e.g., 'api.example.com', 'services.mycorp.org')
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "services.mycorp.org",
}

# Whitelisted API paths (relative to the base URL)
ALLOWED_ENDPOINTS: Iterable[str] = [
    "v1/users",
    "v1/orders",
    "v2/products",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Assemble a fully-qualified API URL from components, ensuring that
    the resulting URL points to an approved domain and uses a
    whitelisted endpoint.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., 'https://api.example.com').
    api_path : str
        The endpoint path relative to the base URL (e.g., 'v1/users').
    query_dict : dict, optional
        Dictionary of query parameters to be URL‑encoded.

    Returns
    -------
    str
        The fully assembled, validated API URL.

    Raises
    ------
    ValueError
        If the domain is not in `APPROVED_API_DOMAINS` or if
        `api_path` is not in `ALLOWED_ENDPOINTS`.
    """
    # 1. Parse the base URL and validate scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # 2. Validate domain
    base_domain = parsed_base.netloc.lower()
    if base_domain not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Unapproved domain: {base_domain}")

    # 3. Validate endpoint
    normalized_path = api_path.lstrip("/")
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # 4. Construct the new path
    # Ensure we combine paths correctly, avoiding duplicate slashes
    base_path = parsed_base.path.rstrip("/")
    new_path = f"{base_path}/{normalized_path}"

    # 5. Merge query parameters
    existing_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)
    # Flatten existing query (parse_qs returns list values)
    flat_query = {k: v[0] for k, v in existing_query.items()}

    if query_dict:
        # Ensure all values are strings
        for key, value in query_dict.items():
            if not isinstance(value, str):
                raise ValueError(f"Query parameter values must be strings: {key}={value!r}")
        flat_query.update(query_dict)

    encoded_query = urllib.parse.urlencode(flat_query, doseq=True)

    # 6. Rebuild the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            base_domain,
            new_path,
            "",          # params (unused)
            encoded_query,
            "",          # fragment
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "50"},
        )
        print("Assembled URL:", url)
    except ValueError as e:
        print("Error:", e)