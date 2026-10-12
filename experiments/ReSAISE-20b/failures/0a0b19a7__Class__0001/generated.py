import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints; replace with real values.
APPROVED_API_DOMAINS = {"api.example.com", "api2.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/status",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    endpoint : str
        The specific endpoint path (e.g., "/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL to ensure it contains a scheme and host
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {api_base_url}")

    # Normalize and validate the domain
    host = parsed_base.netloc.lower()
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Normalize endpoint: ensure it starts with a single '/'
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    # Remove trailing slash for consistency with allowed list
    normalized_endpoint = endpoint.rstrip("/")
    if not any(normalized_endpoint == ep.rstrip("/") for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the path: combine base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    full_path = f"{base_path}{endpoint}"

    # Encode query parameters if provided
    query_string = ""
    if query_params:
        # Ensure all keys/values are strings to avoid encoding issues
        safe_query = {str(k): str(v) for k, v in query_params.items()}
        query_string = urllib.parse.urlencode(safe_query)

    # Reconstruct the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            host,
            full_path,
            "",  # params
            query_string,
            ""   # fragment
        )
    )

    return redirect_url