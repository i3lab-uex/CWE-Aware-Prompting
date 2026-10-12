import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints. In real code these would be defined elsewhere.
APPROVED_API_DOMAINS = {"api.example.com", "service.another.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/login",
    "/logout"
]

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a full API redirect URL.

    Parameters
    ----------
    base_url_api : str
        Base address of the API, e.g. "https://api.example.com".
    api_endpoint : str
        Endpoint path, e.g. "/users" or "users".
    opts : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Parse base URL and validate domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Normalise endpoint (ensure it starts with '/')
    endpoint = api_endpoint if api_endpoint.startswith("/") else f"/{api_endpoint}"
    # Validate endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Join base and endpoint
    joined_url = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", endpoint.lstrip("/"))

    # Append query parameters if provided
    if opts:
        # Ensure all values are strings and encode properly
        query = urllib.parse.urlencode({k: str(v) for k, v in opts.items()})
        final_url = f"{joined_url}?{query}"
    else:
        final_url = joined_url

    return final_url