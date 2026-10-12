import urllib.parse

# Pre‑approved base API domains (scheme + hostname)
APPROVED_API_DOMAINS = {
    "https://api.example.com",
    "https://services.anotherdomain.org",
}

# Safe, allowable API endpoints (path components)
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: dict | None = None
) -> str:
    """
    Build a secure redirect URL for API requests.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to be appended (e.g. "/users").
    query_options : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Normalise and validate the base domain
    parsed_base = urllib.parse.urlparse(base_api_url)
    scheme_netloc = f"{parsed_base.scheme}://{parsed_base.netloc}"
    if scheme_netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{scheme_netloc}' is not approved for API redirects.")

    # Validate the endpoint
    if not any(api_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{api_endpoint}' is not an allowed API endpoint.")

    # Construct the full URL
    path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))
    url_parts = parsed_base._replace(path=path)

    # Attach query parameters if provided
    if query_options:
        encoded_query = urllib.parse.urlencode(query_options, doseq=True)
        url_parts = url_parts._replace(query=encoded_query)

    return urllib.parse.urlunparse(url_parts)