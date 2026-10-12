import urllib.parse

# Trusted API domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}

# Allowed endpoint paths (example values)
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}


def generate_redirect_link(base_url: str, endpoint_path: str,
                           query_info: dict | None = None) -> str:
    """
    Build a safe redirect URL for API requests.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g., "/v1/users").
    query_info : dict, optional
        Query string parameters.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL contains an unapproved domain or endpoint.
    """
    # Parse base_url and enforce HTTPS
    parsed_base = urllib.parse.urlparse(base_url)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError("Base URL must use http or https scheme")

    # Validate domain
    netloc = parsed_base.netloc.lower()
    if not any(netloc == d or netloc.endswith("." + d) for d in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not in the approved list")

    # Normalize and validate endpoint path
    normalized_path = urllib.parse.urljoin("/", endpoint_path)
    if not any(normalized_path == ep or normalized_path.startswith(ep + "/")
               for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # Merge paths
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_path.lstrip("/"))

    # Encode query parameters
    if query_info:
        query_string = urllib.parse.urlencode(query_info, doseq=True)
    else:
        query_string = ""

    # Reconstruct the URL
    redirect_url_parts = (
        parsed_base.scheme,
        netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url