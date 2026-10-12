import urllib.parse

# Pre‑approved base API domains and safe endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "data.api.gov",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/status",
]

def generate_api_redirect(base_url: str, api_path: str, params: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/users/123").
    params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed redirect URL that is guaranteed to belong to an approved domain
        and use a safe endpoint.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Normalise and parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Verify the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_base.hostname!r} is not approved")

    # Ensure the endpoint starts with a slash
    api_path = api_path or ""
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Verify the endpoint is allowed
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {api_path!r} is not allowed")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path, api_path)

    # Build query string if params are supplied
    query = ""
    if params:
        if not isinstance(params, dict):
            raise ValueError("Params must be a dictionary")
        # Ensure all keys and values are strings
        safe_params = {}
        for k, v in params.items():
            if not isinstance(k, str):
                raise ValueError(f"Parameter key {k!r} is not a string")
            if isinstance(v, (list, tuple)):
                # Encode multiple values
                safe_params[k] = [str(x) for x in v]
            else:
                safe_params[k] = str(v)
        query = urllib.parse.urlencode(safe_params, doseq=True)

    # Assemble the final URL
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    ))
    return redirect_url