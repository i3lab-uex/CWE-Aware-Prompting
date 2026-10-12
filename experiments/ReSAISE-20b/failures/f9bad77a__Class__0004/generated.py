#!/usr/bin/env python3
"""
Utility for constructing safe API redirect URLs.

The module defines a function `construct_redirect_url` that safely combines
a base API URL, an endpoint name, and optional query parameters into a
fully‑qualified redirect URL.  The function validates that the resulting
URL points to an approved domain and uses a permitted endpoint, guarding
against CWE‑610 (externally controlled reference to a resource in another sphere).

Author: ChatGPT
"""

from __future__ import annotations

import urllib.parse as _urlparse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – normally this would come from a secure configuration file
# --------------------------------------------------------------------------- #

#: A set of fully qualified hostnames that are trusted for API requests.
APPROVED_API_DOMAINS: frozenset[str] = frozenset(
    {
        "api.example.com",
        "service.secure.org",
        # Add additional approved domains here.
    }
)

#: A set of endpoint paths that are allowed.  Each entry should be a
#: simple path component (no leading slash).
ALLOWED_ENDPOINTS: frozenset[str] = frozenset(
    {
        "users",
        "orders",
        "products",
        # Add additional allowed endpoints here.
    }
)

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base URL of the API (e.g. ``https://api.example.com``).
    endpoint_name : str
        The name of the desired API endpoint (e.g. ``users``).
    params_dict : dict[str, str] | None
        Optional dictionary of query string parameters.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or uses a
        disallowed endpoint.

    Notes
    -----
    The function performs the following safety checks:

    1. **Domain validation** – ensures that the host part of ``main_url``
       is present in :data:`APPROVED_API_DOMAINS`.
    2. **Endpoint validation** – ensures that ``endpoint_name`` is in
       :data:`ALLOWED_ENDPOINTS`.  The function treats the endpoint as a
       simple path component; it does not allow slashes or query strings.
    3. **URL construction** – uses :mod:`urllib.parse` to safely combine
       components and encode query parameters.

    This design mitigates CWE‑610 by preventing an attacker from
    redirecting the request to an untrusted domain or endpoint.
    """

    # --------------------------------------------------------------------- #
    # Validate and parse the base URL
    # --------------------------------------------------------------------- #
    parsed_main = _urlparse.urlparse(main_url)

    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Ensure the host is approved
    if parsed_main.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_main.hostname}' is not in the list of approved API domains."
        )

    # --------------------------------------------------------------------- #
    # Validate the endpoint
    # --------------------------------------------------------------------- #
    if "/" in endpoint_name or "?" in endpoint_name:
        raise ValueError("Endpoint name must be a simple path component without slashes or query strings.")

    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_name}' is not an allowed API endpoint.")

    # --------------------------------------------------------------------- #
    # Build the final URL
    # --------------------------------------------------------------------- #
    # Construct a new path by joining the existing path with the endpoint.
    # Ensure exactly one slash separates components.
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = f"/{endpoint_name}"
    full_path = f"{base_path}{endpoint_path}"

    # Encode query parameters if provided
    query_string = ""
    if params_dict:
        if not isinstance(params_dict, dict):
            raise ValueError("params_dict must be a dictionary.")
        # Convert all values to string and encode
        query_string = _urlparse.urlencode(
            {k: str(v) for k, v in params_dict.items()}
        )

    # Reconstruct the full URL
    final_url = _urlparse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            full_path,
            "",          # params (deprecated)
            query_string,
            "",          # fragment
        )
    )

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com/v1",
            "users",
            {"page": 2, "limit": 50},
        )
        print(f"Redirect URL: {url}")
    except ValueError as exc:
        print(f"URL construction failed: {exc}")