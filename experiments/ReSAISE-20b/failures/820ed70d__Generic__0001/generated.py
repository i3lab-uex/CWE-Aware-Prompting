import urllib.parse

# Set of approved API domains (e.g., "api.example.com")
APPROVED_API_DOMAINS = {
    "api.example.com",
    "api.partner.org",
}

# List of allowed endpoints (e.g., "/v1/users", "/v2/orders")
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/products",
    "/v2/orders",
]

def assemble_api_redirect_link(base_api_url: str,
                               api_path: str,
                               query_dict: dict | None = None) -> str:
    """
    Assemble a fully‑qualified API redirect URL from the given components.

    Parameters
    ----------
    base_api_url : str
        Base API URL, e.g. "https://api.example.com".
    api_path : str
        Path to the target endpoint, e.g. "/v1/users".
    query_dict : dict | None, optional
        Mapping of query parameters. Values are coerced to strings.

    Returns
    -------
    str
        The assembled, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    # Normalise and validate base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url!r}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname!r}")

    # Ensure the endpoint is allowed
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {api_path!r}")

    # Join the base URL with the path
    full_url = urllib.parse.urljoin(parsed_base.geturl(), api_path)

    # Add query parameters if provided
    if query_dict:
        # Convert all values to strings and encode safely
        safe_query = urllib.parse.urlencode(
            {k: str(v) for k, v in query_dict.items()}
        )
        full_url = f"{full_url}?{safe_query}"

    return full_url