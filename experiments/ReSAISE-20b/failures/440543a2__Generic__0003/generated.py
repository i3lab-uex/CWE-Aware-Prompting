import urllib.parse

# ------------------------------------------------------------------
# Configuration: approved domains and endpoints.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
    "backend.internal",
}

ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/auth/login",
    "/auth/logout",
]

# ------------------------------------------------------------------
# Helper: normalize and validate the endpoint.
# ------------------------------------------------------------------
def _validate_endpoint(path: str) -> str:
    """
    Ensure the endpoint is absolute, normalized, and allowed.
    Raises ValueError if not permitted.
    """
    # Normalize the path (remove trailing slashes, etc.)
    normalized = urllib.parse.urljoin("/", path)
    if not normalized.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {path}")

    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized}' is not allowed.")
    return normalized

# ------------------------------------------------------------------
# Helper: validate the domain of a URL.
# ------------------------------------------------------------------
def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the hostname is in APPROVED_API_DOMAINS.
    Raises ValueError if not permitted.
    """
    host = parsed_url.hostname
    if host is None or host.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: dict | None = None
) -> str:
    """
    Construct a safe, fully‑qualified API URL by merging the base URL,
    an approved endpoint path, and optional query parameters.

    Parameters
    ----------
    base_url : str
        The API's base URL (e.g., "https://api.example.com/v1").
    path : str
        The target API endpoint (e.g., "/users").
    params : dict, optional
        Key‑value pairs to be appended as query parameters.

    Returns
    -------
    str
        The assembled, fully‑qualified API URL.

    Raises
    ------
    ValueError
        If the resulting domain or endpoint is not approved.
    """
    # Parse base URL and validate its domain
    parsed_base = urllib.parse.urlparse(base_url)
    _validate_domain(parsed_base)

    # Validate and normalize the endpoint
    normalized_path = _validate_endpoint(path)

    # Construct the path relative to the base
    joined_url = urllib.parse.urljoin(parsed_base.geturl(), normalized_path)

    # Append query parameters if provided
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        joined_url = f"{joined_url}?{query}"

    # Final validation (redundant but safe)
    final_parsed = urllib.parse.urlparse(joined_url)
    _validate_domain(final_parsed)

    return joined_url