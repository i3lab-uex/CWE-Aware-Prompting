#!/usr/bin/env python3
"""
Utility for constructing safe API redirect URLs.

The module validates that the resulting URL points to an approved domain and
uses only whitelisted endpoints.  It also safely encodes any query parameters.
"""

from __future__ import annotations

import urllib.parse
from typing import Dict, Iterable, Optional

# --------------------------------------------------------------------------- #
# Configuration – populate these with your real values
APPROVED_API_DOMAINS: set[str] = {
    "api.example.com",
    "services.anotherdomain.org",
}
ALLOWED_ENDPOINTS: list[str] = [
    "/v1/users",
    "/v2/data",
    "/status",
]

# --------------------------------------------------------------------------- #
def _normalize_endpoint(endpoint: str) -> str:
    """
    Normalise the endpoint by ensuring it starts with a slash and contains
    no disallowed characters (e.g. '..' or backslashes).
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    # Reject path traversal or backslashes
    if ".." in endpoint or "\\" in endpoint:
        raise ValueError("Endpoint contains disallowed characters.")
    return endpoint


def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the URL's netloc (domain) is in the approved list.
    """
    domain = parsed_url.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved.")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is in the allowed list.
    """
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed.")


def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    endpoint : str
        The specific API endpoint (e.g., "/v1/users").
    query_params : dict[str, str], optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        The fully constructed, validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (e.g., https://).")

    # Normalise and validate the endpoint
    norm_endpoint = _normalize_endpoint(endpoint)
    _validate_endpoint(norm_endpoint)

    # Build the path by joining base and endpoint
    # urljoin handles cases where base ends with or without a slash.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", norm_endpoint.lstrip("/"))

    # Reconstruct the URL with the validated domain and path
    new_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            "",  # query (to be added later)
            "",  # fragment
        )
    )

    # Validate domain
    parsed_new = urllib.parse.urlparse(new_url)
    _validate_domain(parsed_new)

    # Append query parameters if provided
    if query_params:
        encoded_query = urllib.parse.urlencode(query_params, doseq=True)
        new_url += f"?{encoded_query}"

    return new_url


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage – replace with your actual values
    try:
        url = build_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "format": "json"},
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Invalid configuration: {exc}")