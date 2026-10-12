import urllib.parse

# ------------------------------------------------------------------
# Configuration: Trusted domains and allowed endpoints.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.example.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

# ------------------------------------------------------------------
# Helper: Validate that a URL is safe to redirect to.
# ------------------------------------------------------------------
def _is_safe_url(url: str) -> bool:
    """
    Checks that the URL uses an approved domain and a permitted endpoint.
    Returns True if both checks pass, False otherwise.
    """
    parsed = urllib.parse.urlparse(url)

    # Domain check (netloc may include port)
    domain = parsed.hostname
    if not domain or domain.lower() not in APPROVED_API_DOMAINS:
        return False

    # Endpoint check
    endpoint = parsed.path
    if not any(endpoint.startswith(allowed) for allowed in ALLOWED_ENDPOINTS):
        return False

    # Optional: Reject URLs that contain fragments or non-GET methods
    if parsed.fragment:
        return False

    return True


# ------------------------------------------------------------------
# Main function: create_redirect_url
# ------------------------------------------------------------------
def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: dict | None = None
) -> str:
    """
    Build a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The base URL of the API (e.g. "https://api.example.com").
    desired_endpoint : str
        The specific endpoint path (e.g. "/v1/users").
    optional_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        A fully qualified, safe URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an approved domain or uses a disallowed endpoint.
    """
    if not base_url_api:
        raise ValueError("Base API URL must be provided.")

    # Ensure the endpoint starts with a slash
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'.")

    # Construct the base path
    joined = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", desired_endpoint.lstrip("/"))

    # Encode optional query parameters
    if optional_params:
        # Only allow string keys/values to avoid unexpected types
        safe_params = {str(k): str(v) for k, v in optional_params.items()}
        query_string = urllib.parse.urlencode(safe_params)
        full_url = f"{joined}?{query_string}"
    else:
        full_url = joined

    # Final safety check
    if not _is_safe_url(full_url):
        raise ValueError("Generated URL is unsafe or uses an unapproved domain/endpoint.")

    return full_url