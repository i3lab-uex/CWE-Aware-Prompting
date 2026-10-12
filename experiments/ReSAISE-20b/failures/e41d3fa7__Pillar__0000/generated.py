# -*- coding: utf-8 -*-
"""
Utility module for generating secure API redirect URLs.

The implementation ensures that the constructed URL
* uses only approved domains,
* references only whitelisted endpoints, and
* safely encodes query parameters.

The module follows best practices to avoid CWE-664 (improper control of a resource through its lifetime)
by not holding onto mutable state and by validating all inputs before generating the URL.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration:  replace these with your real values
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Iterable[str] = {
    "api.example.com",
    "service.mycompany.org",
}

ALLOWED_ENDPOINTS: Iterable[str] = {
    "/users",
    "/orders",
    "/products",
    # Add more endpoints as needed
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g., "/users").
    query_info : dict, optional
        Mapping of query string parameters.

    Returns
    -------
    str
        A fully constructed, validated URL ready for use.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse base URL to extract scheme, netloc, and path
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # 1. Validate domain
    netloc = parsed_base.netloc.split(":")[0]  # ignore port if present
    if netloc.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Domain {netloc!r} is not approved")

    # 2. Validate endpoint
    if not endpoint_path.startswith("/"):
        raise ValueError("Endpoint path must start with '/'")
    if endpoint_path.lower() not in {e.lower() for e in ALLOWED_ENDPOINTS}:
        raise ValueError(f"Endpoint {endpoint_path!r} is not allowed")

    # 3. Construct the new path by joining base path and endpoint
    #    Avoid double slashes; use urljoin with a dummy trailing slash.
    base_path = parsed_base.path
    if not base_path.endswith("/"):
        base_path += "/"
    full_path = urllib.parse.urljoin(base_path, endpoint_path.lstrip("/"))

    # 4. Encode query parameters
    if query_info:
        encoded_query = urllib.parse.urlencode(query_info, doseq=True)
    else:
        encoded_query = ""

    # 5. Reassemble the URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (commented out to keep module import safe)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     url = generate_redirect_link(
#         "https://api.example.com",
#         "/users",
#         {"page": "2", "sort": "name"}
#     )
#     print(url)