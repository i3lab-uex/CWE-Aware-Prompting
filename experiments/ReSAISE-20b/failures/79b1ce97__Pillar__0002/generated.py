# -*- coding: utf-8 -*-
"""
Utility to safely construct an API redirect URL.

The function validates the base URL and endpoint against a whitelist of
approved domains and allowed endpoints, then appends optional query
parameters in a safe manner.

Caveats:
- The function performs strict validation to avoid open redirect or
  request forgery attacks.
- It does not keep any persistent state, preventing CWE‑664 issues
  (improper resource control).
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional, Set

# --------------------------------------------------------------------------- #
# Configuration – replace these with the real values for your environment.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "secure-api.mycorp.io",
}

ALLOWED_ENDPOINTS: Iterable[str] = (
    "/v1/users",
    "/v1/transactions",
    "/v2/orders",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_endpoint(endpoint: str) -> str:
    """
    Normalise the endpoint string.

    Ensures it starts with a single slash, has no trailing slashes,
    and does not contain dangerous path traversal components.
    """
    if not endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")
    # Prevent path traversal
    if ".." in endpoint.split("/"):
        raise ValueError("Endpoint contains forbidden components")
    # Remove duplicate slashes
    endpoint = urllib.parse.urljoin("/", endpoint)
    return endpoint.rstrip("/")

def _validate_domain(netloc: str) -> None:
    """
    Validate that the netloc (domain part) is in the approved list.
    """
    # Strip port if present
    domain = netloc.split(":")[0]
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

def _validate_endpoint(endpoint: str) -> None:
    """
    Validate that the endpoint is in the allowed list.
    """
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full API redirect URL after validating domain and endpoint.

    Parameters
    ----------
    base_url_api : str
        The base URL of the API (e.g. "https://api.example.com").
    desired_endpoint : str
        The specific API endpoint (e.g. "/v1/users").
    optional_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")
    _validate_domain(parsed_base.netloc)

    # Normalise and validate the endpoint
    endpoint = _normalize_endpoint(desired_endpoint)
    _validate_endpoint(endpoint)

    # Build the path
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", endpoint.lstrip("/"))

    # Build query string
    query = ""
    if optional_params:
        if not isinstance(optional_params, dict):
            raise ValueError("optional_params must be a dictionary")
        query = urllib.parse.urlencode(optional_params, doseq=True)

    # Assemble the final URL
    result = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return result

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example base URL
    base = "https://api.example.com"
    endpoint = "/v1/users"
    params = {"page": "2", "sort": "name"}

    try:
        url = create_redirect_url(base, endpoint, params)
        print("Redirect URL:", url)
    except ValueError as exc:
        print("Validation error:", exc)