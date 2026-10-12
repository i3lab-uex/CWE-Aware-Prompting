import urllib.parse
from typing import Dict, Optional

# Allowed domains and endpoints for security purposes
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g. "/v1/users").
    query : dict, optional
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting domain or endpoint is not approved.
    """
    # Parse the base URI to ensure we can extract scheme, netloc, etc.
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URI provided.")

    # Verify domain is approved
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved.")

    # Ensure endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Validate endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed.")

    # Build the new path by joining base path and endpoint
    # Preserve any existing path in base_uri (e.g., "/api")
    new_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Merge existing query parameters from base_uri with the new ones
    base_query = urllib.parse.parse_qs(parsed_base.query)
    # Flatten parse_qs result
    base_query = {k: v[0] for k, v in base_query.items()}

    if query:
        # Overwrite or add new parameters
        merged_query = {**base_query, **query}
    else:
        merged_query = base_query

    # Encode query string
    encoded_query = urllib.parse.urlencode(merged_query)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            new_path,
            "",  # params
            encoded_query,
            "",  # fragment
        )
    )

    return final_url