#!/usr/bin/env python3
"""
Utility to assemble a secure API redirect URL.

The function validates that the resulting URL belongs to an approved domain
and that the requested endpoint is allowed.  This mitigates CWE‑610
(Externally Controlled Reference to a Resource in Another Sphere) by ensuring
that only whitelisted resources can be referenced.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Set, List, Optional

# --------------------------------------------------------------------------- #
# Configuration – adjust these to your environment
# --------------------------------------------------------------------------- #

# Approved hostnames (scheme-independent).  Example: {"api.example.com"}
APPROVED_API_DOMAINS: Set[str] = {
    "api.example.com",
    "service.internal.company.org",
}

# Allowed endpoint paths (relative to the base URL).  Example: ["v1/users", "v2/items"]
ALLOWED_ENDPOINTS: List[str] = [
    "v1/users",
    "v2/items",
    "health/check",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_path(path: str) -> str:
    """
    Normalise an endpoint path for comparison.

    Removes leading/trailing slashes and collapses multiple slashes.
    """
    return "/".join(part for part in path.split("/") if part)

def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Check whether the given endpoint is in the list of allowed endpoints.
    Comparison is case-sensitive and normalised.
    """
    norm_endpoint = _normalize_path(endpoint)
    return any(_normalize_path(allowed) == norm_endpoint for allowed in ALLOWED_ENDPOINTS)

def _is_approved_domain(parsed_url: urllib.parse.ParseResult) -> bool:
    """
    Verify that the parsed URL's hostname is in the approved domains set.
    """
    host = parsed_url.hostname
    return bool(host and host.lower() in {d.lower() for d in APPROVED_API_DOMAINS})

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a fully-qualified API URL from a base URL, an endpoint path,
    and optional query parameters.  The resulting URL is validated against
    approved domains and allowed endpoints.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g. "https://api.example.com/").
    api_path : str
        The relative endpoint path (e.g. "v1/users").
    query_dict : dict, optional
        Mapping of query parameter names to values.

    Returns
    -------
    str
        The assembled and validated URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    if not base_api_url:
        raise ValueError("base_api_url must be a non-empty string")

    # Parse the base URL to ensure it is absolute and contains scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base_api_url: {base_api_url!r}")

    # Validate domain
    if not _is_approved_domain(parsed_base):
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalise the endpoint path and validate
    if not api_path:
        raise ValueError("api_path must be a non-empty string")

    norm_api_path = _normalize_path(api_path)
    if not _is_allowed_endpoint(norm_api_path):
        raise ValueError(f"Endpoint '{norm_api_path}' is not allowed")

    # Construct the full path
    # Ensure there is exactly one slash between base and endpoint
    joined_path = urllib.parse.urljoin(
        parsed_base.path.rstrip("/") + "/",  # base path
        norm_api_path.lstrip("/"),           # endpoint
    )

    # Build query string if provided
    query_string = ""
    if query_dict:
        # Filter out None values; encode others
        filtered_query = {k: v for k, v in query_dict.items() if v is not None}
        if filtered_query:
            query_string = urllib.parse.urlencode(filtered_query, doseq=True)

    # Reconstruct the final URL
    assembled = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            joined_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return assembled

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            base_api_url="https://api.example.com/",
            api_path="/v1/users",
            query_dict={"page": "2", "active": "true"},
        )
        print("Assembled URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")