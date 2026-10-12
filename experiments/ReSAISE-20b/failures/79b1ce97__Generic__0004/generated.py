import urllib.parse
from typing import Dict, Optional

# Trusted domains and allowed endpoints – these would normally be defined elsewhere
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "v1.api.safe.net",
}

ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g. "https://api.example.com").
    desired_endpoint : str
        The endpoint to append (e.g. "/users").
    optional_params : dict, optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting domain is not approved or the endpoint is not allowed.
    """
    # Parse the base URL to extract components
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalize and validate endpoint
    endpoint = desired_endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Construct the new path (ensure no duplicate slashes)
    base_path = parsed_base.path.rstrip("/")
    full_path = f"{base_path}{endpoint}"

    # Build query string if parameters are provided
    query_string = ""
    if optional_params:
        # Ensure all values are strings and encode safely
        safe_params = {str(k): str(v) for k, v in optional_params.items()}
        query_string = urllib.parse.urlencode(safe_params)

    # Reassemble the URL
    new_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        parsed_base.params,
        query_string,
        parsed_base.fragment
    )
    return urllib.parse.urlunparse(new_url_parts)