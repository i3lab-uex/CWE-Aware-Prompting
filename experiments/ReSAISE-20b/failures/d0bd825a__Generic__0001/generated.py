import urllib.parse

# Pre‑approved domains and endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.api.org",
    "data.provider.net",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/products",
]

def _validate_domain(base_url: str) -> None:
    """
    Ensure the base URL belongs to one of the approved domains.
    Raises ValueError if not allowed.
    """
    parsed = urllib.parse.urlparse(base_url)
    domain = parsed.netloc.lower()
    if not any(domain.endswith(approved) for approved in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not approved for API redirects.")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is in the list of allowed endpoints.
    Raises ValueError if not allowed.
    """
    # Normalize: ensure it starts with a single slash and no trailing slash
    normalized = "/" + endpoint.lstrip("/").rstrip("/")
    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not permitted.")


def create_api_redirect_url(base_url_api: str, api_endpoint: str,
                            opts: dict | None = None) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base address of the target API (e.g., 'https://api.example.com').
    api_endpoint : str
        Path of the endpoint (e.g., '/users').
    opts : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # Validate inputs
    _validate_domain(base_url_api)
    _validate_endpoint(api_endpoint)

    # Parse base URL and ensure it ends with a slash for correct join
    parsed_base = urllib.parse.urlparse(base_url_api.rstrip("/"))
    base_path = parsed_base.path

    # Join the endpoint to the base path
    joined_path = urllib.parse.urljoin(base_path + "/", api_endpoint.lstrip("/"))

    # Rebuild the URL without query
    url_no_query = urllib.parse.urlunparse(
        (parsed_base.scheme, parsed_base.netloc, joined_path, "", "", "")
    )

    # Append query parameters if provided
    if opts:
        query_string = urllib.parse.urlencode(opts, doseq=True)
        return f"{url_no_query}?{query_string}"
    else:
        return url_no_query