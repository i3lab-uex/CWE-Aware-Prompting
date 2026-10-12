import urllib.parse

# Example approved domains and endpoints (replace with actual values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org"
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status"
]

def build_api_redirect_url(api_base_url: str,
                           endpoint: str,
                           query_params: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        Endpoint path to append (e.g. "/users").
    query_params : dict, optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        Fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(api_base_url)

    if parsed_base.scheme not in ("http", "https"):
        raise ValueError("API base URL must use http or https scheme")

    # Verify the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize and validate the endpoint
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Remove any trailing slash to match list entries
    normalized_endpoint = endpoint.rstrip("/")
    if not any(normalized_endpoint == e.rstrip("/") for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path, endpoint)

    # Encode query parameters if provided
    query_string = ""
    if query_params:
        # Ensure all keys and values are strings for safety
        safe_query = {str(k): str(v) for k, v in query_params.items()}
        query_string = urllib.parse.urlencode(safe_query)

    # Assemble the final URL
    redirect_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url