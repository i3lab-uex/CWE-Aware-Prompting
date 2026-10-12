import urllib.parse

# Trusted API domains and endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.example.org",
}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

def generate_redirect_link(base_url: str, endpoint_path: str,
                           query_info: dict | None = None) -> str:
    """
    Construct a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The root URL of the target API (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API path (e.g., "/v1/users").
    query_info : dict, optional
        Dictionary of key/value pairs to be encoded as the query string.

    Returns
    -------
    str
        A complete, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed
        endpoint.  This protects against open‑redirect vulnerabilities (CWE‑601).
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_url)

    # Validate scheme and host
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must include scheme and host")

    # Ensure the domain is approved
    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {domain}")

    # Normalize endpoint path
    normalized_endpoint = urllib.parse.urljoin("/", endpoint_path)
    if not normalized_endpoint.startswith("/"):
        raise ValueError("Endpoint path must start with a slash")

    # Ensure endpoint is allowed
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {normalized_endpoint}")

    # Merge path components
    new_path = urllib.parse.urljoin(parsed_base.path, normalized_endpoint)

    # Encode query parameters
    query_string = urllib.parse.urlencode(query_info or {}, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        new_path,
        "",          # params
        query_string,
        ""           # fragment
    ))

    return final_url