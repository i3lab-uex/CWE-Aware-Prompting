#!/usr/bin/env python3
"""
Utility to safely construct a full redirect URL for API requests.
"""

from urllib.parse import urlparse, urlunparse, urlencode, quote_plus
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be kept in sync with the deployment environment
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.example.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v1/products",
    "/v2/status",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_path(path: str) -> str:
    """
    Normalise the endpoint path to avoid double slashes or traversal.
    Ensures the path starts with a single leading slash and does not contain
    '..' components.
    """
    if not path.startswith("/"):
        path = "/" + path
    # Reject any '..' segments that could lead to directory traversal.
    if ".." in path.split("/"):
        raise ValueError("Endpoint path contains disallowed '..' component")
    # Collapse multiple slashes
    return "/".join(part for part in path.split("/") if part)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint path (e.g., "/v1/users").
    query_info : dict, optional
        Dictionary of key/value pairs to be encoded as the query string.

    Returns
    -------
    str
        A fully-qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed
        endpoint. Also raised for malformed inputs.
    """
    if not isinstance(base_url, str) or not base_url:
        raise ValueError("base_url must be a non-empty string")
    if not isinstance(endpoint_path, str) or not endpoint_path:
        raise ValueError("endpoint_path must be a non-empty string")

    # Parse base URL and validate scheme
    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure base_url has a netloc
    if not parsed_base.netloc:
        raise ValueError("base_url must include a network location (netloc)")

    # Verify domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalise and validate endpoint
    normalized_endpoint = _normalize_path(endpoint_path)
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed")

    # Build the path
    full_path = normalized_endpoint

    # Encode query parameters if provided
    query_string = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        # Use quote_plus to encode spaces as '+', safe for URLs
        query_string = urlencode(
            {k: v for k, v in query_info.items() if isinstance(k, str) and isinstance(v, str)},
            doseq=True,
        )

    # Construct the final URL
    redirect_url = urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            query_string,  # query
            ""           # fragment
        )
    )

    return redirect_url

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "filter": "active"}
        )
        print("Generated URL:", url)
    except ValueError as exc:
        print("Error generating redirect link:", exc)