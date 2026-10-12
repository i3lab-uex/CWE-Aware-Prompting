import urllib.parse

# Example pre-approved domains and allowed endpoints.
# In real usage these should be defined elsewhere in the project.
APPROVED_API_DOMAINS = {"api.example.com", "service.anotherdomain.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/health",
}

def create_api_redirect_url(base_url_api: str,
                            api_endpoint: str,
                            opts: dict | None = None) -> str:
    """
    Construct a fully-qualified API redirect URL.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint to append (e.g. "/v1/users").
    opts : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # Parse the base URL to validate its domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL: missing scheme or host")

    domain = parsed_base.hostname
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for API redirects")

    # Normalize endpoint
    endpoint = api_endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Validate endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Construct the path
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", endpoint.lstrip("/"))

    # Rebuild the URL without query
    url_parts = parsed_base._replace(path=full_path, params="", query="", fragment="")
    base_url = urllib.parse.urlunparse(url_parts)

    # Append query parameters if provided
    if opts:
        # Ensure all values are strings or convertible to string
        query = urllib.parse.urlencode({k: str(v) for k, v in opts.items()})
        base_url = f"{base_url}?{query}"

    return base_url