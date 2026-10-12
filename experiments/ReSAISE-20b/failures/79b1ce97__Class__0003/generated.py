import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints; replace with actual values.
APPROVED_API_DOMAINS = {"api.example.com", "secure.api.org"}
ALLOWED_ENDPOINTS = {
    "/users",
    "/posts",
    "/comments",
    "/auth/login",
    "/data/summary"
}


def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com/v1").
    desired_endpoint : str
        The specific API endpoint (e.g., "/users" or "posts").
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is not allowed.
    """
    if optional_params is None:
        optional_params = {}

    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_url_api)

    # Validate scheme
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Normalize and validate endpoint
    endpoint = desired_endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {endpoint}")

    # Combine path components safely
    base_path = parsed_base.path.rstrip("/")
    combined_path = urllib.parse.urljoin(base_path + "/", endpoint.lstrip("/"))

    # Encode query parameters
    query_string = urllib.parse.urlencode(optional_params)

    # Reconstruct the final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        combined_path,
        "",          # params (deprecated)
        query_string,
        ""           # fragment
    )
    return urllib.parse.urlunparse(final_url_parts)