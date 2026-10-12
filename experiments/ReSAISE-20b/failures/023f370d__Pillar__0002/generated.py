import urllib.parse
from typing import Dict, Optional

# Pre-approved domains and safe endpoints (example values)
APPROVED_API_DOMAINS = {"api.example.com", "services.foo.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/data",
    "/status",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path to append to the base URL (e.g., "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or if the endpoint is not
        listed in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL to isolate its components
    parsed_base = urllib.parse.urlparse(base_api_url)

    # Validate the domain (netloc)
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.netloc}' is not approved for API redirects."
        )

    # Ensure the endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        raise ValueError("API endpoint must start with a '/' character.")

    # Validate the endpoint against allowed list
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed.")

    # Build the full path by joining base path and endpoint
    full_path = urllib.parse.urljoin(parsed_base.path, api_endpoint)

    # Encode query parameters safely
    query_string = ""
    if query_options:
        # Ensure all keys and values are strings to avoid unexpected behavior
        safe_query = {
            str(k): str(v) for k, v in query_options.items()
        }
        query_string = urllib.parse.urlencode(safe_query)

    # Reconstruct the full URL
    redirect_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        "",  # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url