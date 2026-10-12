# -*- coding: utf-8 -*-
"""
Utility for constructing a secure API redirect URL.

The function validates the base URL and endpoint against approved
lists to mitigate CWE-610 (Externally Controlled Reference).
"""

from urllib.parse import urlparse, urlunparse, urlencode, ParseResult
from typing import Dict, Optional

# Example approved domains and allowed endpoints.
# In real code these would come from a config file or environment variables.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.service.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}

def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the network location (host[:port]) ends with an approved domain.
    Handles optional port numbers by stripping them before comparison.
    """
    host = netloc.split(":")[0].lower()
    return any(host == domain or host.endswith("." + domain) for domain in APPROVED_API_DOMAINS)

def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Verify that the endpoint is in the allowed list.
    The endpoint must start with '/' and be an exact match.
    """
    return endpoint in ALLOWED_ENDPOINTS

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., 'https://api.example.com').
    desired_endpoint : str
        The specific API endpoint (e.g., '/v1/users').
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the base URL or endpoint is not approved.
    """
    if not isinstance(base_url_api, str):
        raise TypeError("base_url_api must be a string")
    if not isinstance(desired_endpoint, str):
        raise TypeError("desired_endpoint must be a string")

    # Parse the base URL
    parsed_base = urlparse(base_url_api)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url_api must be a valid absolute URL")

    # Security check: approved domain
    if not _is_approved_domain(parsed_base.netloc):
        raise ValueError(f"Unapproved domain in base_url_api: {parsed_base.netloc}")

    # Security check: allowed endpoint
    if not _is_allowed_endpoint(desired_endpoint):
        raise ValueError(f"Endpoint '{desired_endpoint}' is not allowed")

    # Build the new path
    # Ensure that we don't accidentally drop slashes or create double slashes
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = desired_endpoint.lstrip("/")
    new_path = f"{base_path}/{endpoint_path}"

    # Encode query parameters if provided
    query_string = urlencode(optional_params) if optional_params else ""

    # Reconstruct the full URL
    new_url = ParseResult(
        scheme=parsed_base.scheme,
        netloc=parsed_base.netloc,
        path=new_path,
        params="",
        query=query_string,
        fragment=""
    ).geturl()

    return new_url