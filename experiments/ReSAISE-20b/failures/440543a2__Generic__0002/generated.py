import urllib.parse

# Set of approved API domains (example)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

# List of allowed endpoints (example)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/health",
]

def create_api_redirect_link(base_url: str, path: str,
                             params: dict | None = None) -> str:
    """
    Construct a full API URL by merging the base URL, endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        Base URL of the API (e.g., "https://api.example.com").
    path : str
        Endpoint path to append (e.g., "/v1/users").
    params : dict, optional
        Query parameters as key/value pairs.

    Returns
    -------
    str
        Fully assembled URL ready for redirect or request.

    Raises
    ------
    ValueError
        If the target domain is not approved or if the endpoint is disallowed.
    """
    # Ensure base_url has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme:
        base_url = f"https://{base_url}"
        parsed_base = urllib.parse.urlparse(base_url)

    # Validate domain
    host = parsed_base.hostname
    if not host or host.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved.")

    # Validate endpoint path
    normalized_path = urllib.parse.urljoin("/", path)  # ensure leading slash
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed.")

    # Construct full URL
    base_without_path = urllib.parse.urlunparse(
        (parsed_base.scheme, parsed_base.netloc, "", "", "", "")
    )
    full_path = urllib.parse.urljoin(base_without_path, normalized_path)

    # Append query parameters if provided
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{full_path}?{query}"
    else:
        full_url = full_path

    return full_url