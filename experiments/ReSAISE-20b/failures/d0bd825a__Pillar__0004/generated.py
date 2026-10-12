#!/usr/bin/env python3
"""
Utility for generating a safe API redirect URL.
"""

from urllib.parse import urlparse, urlencode, urlunparse
from typing import Dict, Optional

# Pre-approved base API domains and allowed endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "internal.company.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/data",
    "/status",
    "/healthcheck",
]

def _validate_domain(base_url: str) -> None:
    """
    Ensure the base URL's netloc is an approved domain.
    Raises ValueError if not approved.
    """
    parsed = urlparse(base_url)
    domain = parsed.netloc.lower()
    if not any(domain == approved or domain.endswith(f".{approved}") for approved in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not approved for API redirects.")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is in the list of allowed endpoints.
    Raises ValueError if not allowed.
    """
    # Normalise: remove leading/trailing slashes for comparison
    ep = endpoint.rstrip("/")
    if not any(ep == a.rstrip("/") or ep.startswith(a.rstrip("/")) for a in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed.")


def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Specific endpoint path (e.g., "/v1/users").
    opts : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Validate inputs first to avoid constructing an unsafe URL
    _validate_domain(base_url_api)
    _validate_endpoint(api_endpoint)

    # Ensure base URL ends with a slash for proper joining
    if not base_url_api.endswith("/"):
        base_url_api += "/"

    # Construct the full path
    endpoint = api_endpoint.lstrip("/")
    full_path = f"{endpoint}"

    # Build query string if options are provided
    query = urlencode(opts) if opts else ""

    # Reassemble the URL
    parsed_base = urlparse(base_url_api)
    redirect_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    )
    redirect_url = urlunparse(redirect_parts)

    return redirect_url


# Example usage (for demonstration; remove or guard with if __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "verbose": "true"}
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid URL configuration: {exc}")