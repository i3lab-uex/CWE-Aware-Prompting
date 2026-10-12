#!/usr/bin/env python3
"""
Utility to safely construct API redirect URLs.
"""

from urllib.parse import urlparse, urlunparse, urlencode, urljoin
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – in a real project these would be defined elsewhere
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.io",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/health",
]

# ----------------------------------------------------------------------
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully‑qualified API URL from a base, endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g. "https://api.example.com").
    path : str
        The endpoint to append (e.g. "/v1/users").
    params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        The fully constructed API URL.

    Raises
    ------
    ValueError
        If the domain of ``base_url`` is not in :data:`APPROVED_API_DOMAINS`
        or if ``path`` is not in :data:`ALLOWED_ENDPOINTS`.
    """
    # Validate and normalize base URL
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Normalize path – ensure it starts with a slash
    normalized_path = path if path.startswith("/") else f"/{path}"
    # Ensure the endpoint is allowed
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Combine base path with the endpoint
    combined_url = urljoin(parsed_base.geturl(), normalized_path)

    # Add query parameters if provided
    if params:
        # Encode parameters; values are coerced to string
        query_string = urlencode({k: str(v) for k, v in params.items()})
    else:
        query_string = ""

    # Reconstruct final URL
    parsed_combined = urlparse(combined_url)
    final_components = (
        parsed_combined.scheme,
        parsed_combined.netloc,
        parsed_combined.path,
        parsed_combined.params,
        query_string,
        parsed_combined.fragment
    )
    final_url = urlunparse(final_components)

    return final_url

# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": 2, "limit": 50}
        )
        print(url)  # https://api.example.com/v1/users?page=2&limit=50
    except ValueError as exc:
        print(f"URL construction failed: {exc}")