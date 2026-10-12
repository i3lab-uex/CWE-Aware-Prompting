import urllib.parse

# Trusted API domains and allowed endpoints
APPROVED_API_DOMAINS = {"api.example.com", "api.secure.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: dict | None = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL, e.g. "https://api.example.com".
    desired_endpoint : str
        The specific endpoint to call, e.g. "/v1/users".
    optional_params : dict | None
        Optional query parameters to append to the URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or if the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL to validate domain and scheme
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or parsed_base.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Ensure endpoint starts with a slash and is allowed
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")
    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{desired_endpoint}' is not allowed")

    # Build the path by joining base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", desired_endpoint.lstrip("/"))

    # Encode query parameters safely
    if optional_params:
        if not isinstance(optional_params, dict):
            raise ValueError("optional_params must be a dictionary")
        query = urllib.parse.urlencode(optional_params, doseq=True)
    else:
        query = ""

    # Reconstruct the full URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            domain,
            full_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return redirect_url