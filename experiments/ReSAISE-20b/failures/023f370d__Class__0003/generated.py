import urllib.parse

# Pre‑approved API domains (scheme + netloc).  In a real system these would be
# read from a secure configuration file or environment variable.
APPROVED_API_DOMAINS = {
    "https://api.example.com",
    "https://service.partner.org",
}

# Safe, allowable API endpoints (relative paths).  Only these will be accepted.
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/health",
]

def construct_api_redirect(base_api_url: str,
                           api_endpoint: str,
                           query_options: dict | None = None) -> str:
    """
    Construct a redirect URL for an API call.

    Parameters
    ----------
    base_api_url : str
        Base address of the API, e.g. "https://api.example.com".
    api_endpoint : str
        Relative endpoint path, e.g. "/v1/users".
    query_options : dict | None
        Optional mapping of query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the target domain is not approved or the endpoint is not allowed.
    """
    # ---- Validate base API URL ------------------------------------------------
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not (parsed_base.scheme and parsed_base.netloc):
        raise ValueError(f"Invalid base API URL: {base_api_url}")

    # Normalise to scheme://netloc
    normalized_base = f"{parsed_base.scheme}://{parsed_base.netloc}"
    if normalized_base not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{normalized_base}' is not approved")

    # ---- Validate endpoint ----------------------------------------------------
    if not api_endpoint.startswith("/"):
        raise ValueError("API endpoint must start with '/'")
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # ---- Build query string ---------------------------------------------------
    if query_options:
        # Ensure all keys and values are strings for safety
        safe_query = {str(k): str(v) for k, v in query_options.items()}
        query_string = urllib.parse.urlencode(safe_query)
    else:
        query_string = ""

    # ---- Assemble final URL ----------------------------------------------------
    url_parts = urllib.parse.ParseResult(
        scheme=parsed_base.scheme,
        netloc=parsed_base.netloc,
        path=api_endpoint,
        params="",
        query=query_string,
        fragment=""
    )
    return url_parts.geturl()