# -*- coding: utf-8 -*-
"""
Utility to generate a secure redirect URL for API requests.
"""

from urllib.parse import urlparse, urlunparse, urlencode, quote
import re

# --------------------------------------------------------------------------- #
# Configuration – normally these would be imported from a secure config file.
# --------------------------------------------------------------------------- #

# Approved domains (regex patterns to allow subdomains if needed)
APPROVED_API_DOMAINS = {
    r"^api\.trustedservice\.com$",
    r"^secure\.example\.org$",
}

# Allowed endpoint paths (exact matches, no trailing slash)
ALLOWED_ENDPOINTS = {
    "v1/users",
    "v2/orders",
    "status/check",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_approved_domain(host: str) -> bool:
    """Check if host matches any approved domain pattern."""
    return any(re.match(pattern, host) for pattern in APPROVED_API_DOMAINS)

def _is_allowed_endpoint(path: str) -> bool:
    """Check if the endpoint path is in the allowed list."""
    # Normalize to remove leading/trailing slashes
    normalized = path.strip("/")
    return normalized in ALLOWED_ENDPOINTS

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: dict | None = None
) -> str:
    """
    Build a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.trustedservice.com").
    endpoint_path : str
        The specific API endpoint (e.g., "v1/users").
    query_info : dict, optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        A complete, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the base domain or endpoint is not approved/allowed.
    """
    if not isinstance(base_url, str) or not base_url:
        raise ValueError("base_url must be a non-empty string")

    if not isinstance(endpoint_path, str) or not endpoint_path:
        raise ValueError("endpoint_path must be a non-empty string")

    # Parse base URL to validate scheme and domain
    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError("base_url must use http or https scheme")

    if not _is_approved_domain(parsed_base.hostname or ""):
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Validate endpoint path
    if not _is_allowed_endpoint(endpoint_path):
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # Construct the path
    endpoint_clean = endpoint_path.lstrip("/")
    full_path = f"/{endpoint_clean}"

    # Build query string
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        # Ensure all keys and values are strings
        query_parts = {
            str(k): str(v) for k, v in query_info.items()
        }
        encoded_query = urlencode(query_parts, doseq=True)
    else:
        encoded_query = ""

    # Assemble final URL
    new_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        ""   # fragment
    )
    final_url = urlunparse(new_url_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     url = generate_redirect_link(
#         "https://api.trustedservice.com",
#         "v1/users",
#         {"id": 123, "verbose": True}
#     )
#     print(url)