import urllib.parse

# Allowed domains and endpoints for security
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/status",
]

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: dict | None = None
) -> str:
    """
    Build a secure API redirect URL.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    query_dict : dict | None, optional
        Dictionary of query parameters to include.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    # Ensure base_url has a scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme:
        raise ValueError("Base API URL must include a scheme (http or https).")

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved.")

    # Normalize and validate endpoint
    normalized_path = urllib.parse.urljoin("/", api_path.lstrip("/"))
    if not any(normalized_path.startswith(ep) for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed.")

    # Build the full path
    full_url = urllib.parse.urljoin(base_api_url.rstrip("/") + "/", normalized_path.lstrip("/"))

    # Append query parameters if provided
    if query_dict:
        # Ensure all keys and values are strings for safety
        safe_query = {str(k): str(v) for k, v in query_dict.items()}
        full_url += "?" + urllib.parse.urlencode(safe_query)

    return full_url