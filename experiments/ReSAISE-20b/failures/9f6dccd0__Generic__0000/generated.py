import urllib.parse

# Pre‑approved base API domains (e.g. 'api.example.com')
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
}

# Safe, allowable API endpoints
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


def generate_api_redirect(base_url: str, api_path: str, params: dict | None = None) -> str:
    """
    Construct a full API redirect URL from the given base URL, endpoint and
    optional query parameters.

    Parameters
    ----------
    base_url : str
        Base address of an API (e.g. 'https://api.example.com')
    api_path : str
        Endpoint path (e.g. '/v1/users')
    params : dict | None, optional
        Dictionary of query parameters to append

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an approved domain or if the
        endpoint is not in `ALLOWED_ENDPOINTS`.
    """
    # Parse the base URL to extract its components
    parsed_base = urllib.parse.urlparse(base_url)

    # Validate the domain
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Normalise netloc to lower case for comparison
    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for API redirects")

    # Ensure the endpoint starts with a slash
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Validate the endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Build the full path by joining base path and endpoint
    # If the base URL already contains a path, we join it appropriately.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Assemble the full URL components
    url_components = (
        parsed_base.scheme,
        domain,
        full_path,
        "",  # params
        urllib.parse.urlencode(params) if params else "",
        "",  # fragment
    )
    redirect_url = urllib.parse.urlunparse(url_components)

    return redirect_url