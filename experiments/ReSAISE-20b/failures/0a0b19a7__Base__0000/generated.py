import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints. In a real application these would
# be imported from a configuration module or environment variables.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.internal.company",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        Endpoint path, must be one of ALLOWED_ENDPOINTS.
    query_params : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        A fully resolved, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or endpoint.
    """
    # Ensure base URL has a scheme
    if not urllib.parse.urlparse(api_base_url).scheme:
        raise ValueError("Base URL must include a scheme (http:// or https://)")

    # Resolve the full path
    resolved_url = urllib.parse.urljoin(api_base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    # Parse components
    parsed = urllib.parse.urlparse(resolved_url)

    # Validate domain (netloc)
    host = parsed.hostname
    if not host or host.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for API redirects")

    # Validate endpoint
    if parsed.path.lower() not in (e.lower() for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{parsed.path}' is not allowed")

    # Append query parameters if provided
    if query_params:
        # Ensure all values are strings to avoid unexpected types
        sanitized = {k: str(v) for k, v in query_params.items()}
        query_string = urllib.parse.urlencode(sanitized)
        # Build the final URL with encoded query
        final_url = urllib.parse.urlunparse(
            parsed._replace(query=query_string)
        )
    else:
        final_url = resolved_url

    return final_url