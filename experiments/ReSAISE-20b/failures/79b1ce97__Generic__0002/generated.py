import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Trusted domains and endpoints – replace with your actual values
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}


def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The API endpoint path (e.g., "/v1/users").
    optional_params : dict, optional
        Query string parameters to be appended.

    Returns
    -------
    str
        A fully constructed URL ready for redirection.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is not allowed.
    """
    # Parse the base URL to extract the domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Normalize the domain (strip port if present)
    netloc = parsed_base.hostname
    if not netloc:
        raise ValueError(f"Unable to determine hostname from {base_url_api}")

    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not an approved API domain")

    # Validate the endpoint
    normalized_endpoint = urllib.parse.urljoin("/", desired_endpoint)
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{desired_endpoint}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Encode query parameters if provided
    query_string = ""
    if optional_params:
        # Ensure all keys/values are strings and encode safely
        safe_params = {
            str(k): str(v) for k, v in optional_params.items() if k is not None and v is not None
        }
        query_string = urllib.parse.urlencode(safe_params)

    # Reconstruct the final URL
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