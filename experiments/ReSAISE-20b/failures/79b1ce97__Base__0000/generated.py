import urllib.parse

# Trusted API domains and allowed endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]

def create_redirect_url(base_url_api: str,
                        desired_endpoint: str,
                        optional_params: dict | None = None) -> str:
    """
    Build a safe redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g. "https://api.example.com").
    desired_endpoint : str
        The endpoint path (e.g. "/users").
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse base URL to extract scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL format")

    # Validate domain
    if parsed_base.netloc.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Normalize and validate endpoint
    endpoint = urllib.parse.urljoin("/", desired_endpoint)  # ensures leading slash
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {endpoint}")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint.lstrip("/"))

    # Encode query parameters if provided
    query = urllib.parse.urlencode(optional_params or {}, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    ))

    return final_url