#!/usr/bin/env python3
"""
Utility module for generating a safe API redirect URL.
"""

import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: approved domains and endpoints.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.test.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ----------------------------------------------------------------------
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API URL by merging the base URI, endpoint and
    optional query parameters while enforcing strict domain and path
    validation.

    Parameters
    ----------
    base_uri : str
        Base URL of the API, e.g. "https://api.example.com".
    api_endpoint : str
        Endpoint path, e.g. "/v1/users".
    query : dict[str, str], optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain of `base_uri` is not in ``APPROVED_API_DOMAINS`` or
        the endpoint path is not in ``ALLOWED_ENDPOINTS``.
    """
    # Parse base URI
    parsed_base = urllib.parse.urlparse(base_uri)

    # Ensure scheme is HTTPS for security.
    if parsed_base.scheme.lower() != "https":
        raise ValueError("Base URI must use HTTPS scheme.")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Validate endpoint path
    normalized_endpoint = urllib.parse.urljoin("/", api_endpoint)
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {normalized_endpoint}")

    # Merge paths
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Build query string
    if query:
        # Ensure all values are strings to avoid unexpected encoding
        safe_query = {k: str(v) for k, v in query.items()}
        query_string = urllib.parse.urlencode(safe_query)
    else:
        query_string = ""

    # Reconstruct full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            combined_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return final_url

# ----------------------------------------------------------------------
# Example usage (for demonstration; remove or guard with __main__ in real use)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            base_uri="https://api.example.com",
            api_endpoint="/v1/users",
            query={"id": "123", "verbose": "true"}
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid URL: {exc}")