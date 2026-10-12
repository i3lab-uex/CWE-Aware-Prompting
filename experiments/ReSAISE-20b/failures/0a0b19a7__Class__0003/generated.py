import urllib.parse
from typing import Dict, Optional

# Example approved domains and allowed endpoints.
APPROVED_API_DOMAINS = {"api.example.com", "services.another.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/status",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API, e.g. "https://api.example.com".
    endpoint : str
        The specific API endpoint, e.g. "/v1/users".
    query_params : dict[str,str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or disallowed endpoint.
    """
    # Ensure the base URL has a scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme:
        raise ValueError("api_base_url must include a scheme (http or https)")

    # Build the path and query
    safe_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    # Validate endpoint against allowed list
    if not any(safe_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the full URL
    joined_url = urllib.parse.urljoin(api_base_url.rstrip("/") + "/", safe_endpoint.lstrip("/"))
    parsed_joined = urllib.parse.urlparse(joined_url)

    # Validate domain
    if parsed_joined.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_joined.hostname}' is not approved")

    # Add query parameters if provided
    if query_params:
        encoded_qs = urllib.parse.urlencode(query_params, doseq=True)
        final_url = parsed_joined._replace(query=encoded_qs).geturl()
    else:
        final_url = parsed_joined.geturl()

    return final_url