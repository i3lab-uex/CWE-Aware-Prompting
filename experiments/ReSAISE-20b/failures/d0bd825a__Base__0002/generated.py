import urllib.parse

# ----------------------------------------------------------------------
# Pre‑approved domains and endpoints.  In a real application these would
# be populated from configuration or environment variables.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

# ----------------------------------------------------------------------
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: dict | None = None
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to append (e.g. "/v1/users").
    opts : dict, optional
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
    if opts is None:
        opts = {}

    # ------------------------------------------------------------------
    # Validate domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Extract the domain part (e.g., api.example.com)
    domain = parsed_base.netloc.split(":")[0]  # ignore port
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirects")

    # ------------------------------------------------------------------
    # Validate endpoint
    # Ensure it starts with a slash and is in the allowed list
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # ------------------------------------------------------------------
    # Build the full URL
    base_path = urllib.parse.urljoin(parsed_base.geturl(), api_endpoint)
    if opts:
        query_string = urllib.parse.urlencode(opts, doseq=True)
        full_url = f"{base_path}?{query_string}"
    else:
        full_url = base_path

    return full_url