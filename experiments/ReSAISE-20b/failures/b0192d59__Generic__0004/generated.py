import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – only allow known safe domains and endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_endpoint(endpoint: str) -> str:
    """
    Ensure the endpoint starts with a slash and has no trailing slashes.
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return endpoint.rstrip("/")

def _is_domain_approved(url: str) -> bool:
    """
    Verify that the hostname of the given URL is in APPROVED_API_DOMAINS.
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname in APPROVED_API_DOMAINS

def _is_endpoint_approved(endpoint: str) -> bool:
    """
    Verify that the endpoint is in ALLOWED_ENDPOINTS.
    """
    return endpoint in ALLOWED_ENDPOINTS

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a secure API redirect URL.

    Parameters
    ----------
    base_uri : str
        The base URI of the API, e.g. "https://api.example.com".
    api_endpoint : str
        The path component of the API endpoint, e.g. "/v1/users".
    query : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Normalize and validate the endpoint
    normalized_endpoint = _normalize_endpoint(api_endpoint)
    if not _is_endpoint_approved(normalized_endpoint):
        raise ValueError(f"Endpoint '{api_endpoint}' is not approved.")

    # Build the base URL (scheme + netloc)
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri}")

    # Validate domain
    if not _is_domain_approved(base_uri):
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved.")

    # Join the base and endpoint paths
    joined_path = urllib.parse.urljoin(parsed_base.path or "/", normalized_endpoint)

    # Assemble query string
    query_string = urllib.parse.urlencode(query) if query else ""

    # Reconstruct the final URL
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     url = generate_api_redirect_uri(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": "2", "limit": "50"}
#     )
#     print(url)