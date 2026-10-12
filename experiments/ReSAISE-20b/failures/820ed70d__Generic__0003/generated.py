import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------
# Configuration: approved domains and endpoints
# --------------------------------------------------------------------

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/payments",
]

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _is_domain_approved(parsed_url: urllib.parse.ParseResult) -> bool:
    """Return True if the URL's domain is in APPROVED_API_DOMAINS."""
    # urllib.parse.ParseResult.hostname returns None if no hostname
    return bool(parsed_url.hostname and parsed_url.hostname in APPROVED_API_DOMAINS)

def _is_endpoint_allowed(endpoint: str) -> bool:
    """Return True if the endpoint is in ALLOWED_ENDPOINTS."""
    return endpoint in ALLOWED_ENDPOINTS

def _join_path(base: str, path: str) -> str:
    """
    Join base and path ensuring a single '/' separator.
    Handles cases where either part may or may not start/end with '/'.
    """
    if base.endswith("/") and path.startswith("/"):
        return base.rstrip("/") + path
    if not base.endswith("/") and not path.startswith("/"):
        return f"{base}/{path}"
    return base + path

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Assemble a full API redirect URL from the base, endpoint and optional
    query parameters.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    query_dict : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Parse base URL
    parsed_base = urllib.parse.urlparse(base_api_url)

    if not _is_domain_approved(parsed_base):
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved.")

    # Validate endpoint
    if not _is_endpoint_allowed(api_path):
        raise ValueError(f"Endpoint '{api_path}' is not allowed.")

    # Construct full path
    full_path = _join_path(parsed_base.path, api_path)

    # Build query string if provided
    query = urllib.parse.urlencode(query_dict) if query_dict else ""

    # Reassemble the URL
    assembled = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return assembled

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": "2", "limit": "50"},
#     )
#     print(url)