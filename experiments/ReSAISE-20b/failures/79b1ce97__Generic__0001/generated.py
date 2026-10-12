#!/usr/bin/env python3
"""
Utility to construct a fully-qualified redirect URL for an API call.
The function validates that the target domain and endpoint are approved
before assembling the final URL, mitigating open‑redirect attacks.
"""

from urllib.parse import urlparse, urlencode, urlunparse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – in a real project these would be imported from
# a dedicated settings module or environment variables.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "secure.api.mysite.net",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v2/orders",
    "/search",
    "/status",
}

# ----------------------------------------------------------------------
def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a safe redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base URL of the API (e.g. "https://api.example.com").
    desired_endpoint : str
        Endpoint path to be appended (e.g. "/v1/users").
    optional_params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        Fully-qualified, encoded redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL and validate its scheme
    parsed_base = urlparse(base_url_api)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Validate the domain against approved list
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Ensure the endpoint starts with a slash
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")

    # Validate the endpoint against allowed list
    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{desired_endpoint}' is not allowed")

    # Build the path by concatenating base path and endpoint
    # Preserve any existing path on the base URL (e.g. "/api")
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = desired_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}".replace("//", "/")

    # Encode query parameters if provided
    query = urlencode(optional_params or {}, doseq=True)

    # Reconstruct the full URL
    final_url = urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",          # params
        query,       # query
        ""           # fragment
    ))

    return final_url


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = create_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "25"}
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")