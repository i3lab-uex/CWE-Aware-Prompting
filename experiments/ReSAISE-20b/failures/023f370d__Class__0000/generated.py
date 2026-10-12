import urllib.parse

# --------------------------------------------------------------------------- #
#  Configuration – these should be populated with real values in production
# --------------------------------------------------------------------------- #

# Approved base domains (e.g. "https://api.example.com")
APPROVED_API_DOMAINS = {
    "https://api.example.com",
    "https://service.anotherdomain.org",
}

# Allowed endpoints (relative paths)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #

def _normalize_base_url(base_url: str) -> str:
    """
    Normalise the base URL to ensure it ends with a trailing slash and
    has a valid scheme.
    """
    parsed = urllib.parse.urlparse(base_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")
    # Rebuild with trailing slash
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    normalized = f"{parsed.scheme}://{netloc}{path}/"
    return normalized

def _validate_domain(base_url: str) -> None:
    """
    Ensure the base URL belongs to an approved domain.
    """
    if not any(base_url.startswith(approved) for approved in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain not approved: {base_url!r}")

def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is within the list of allowed endpoints.
    """
    if not any(endpoint == ep or endpoint.startswith(ep.rstrip('/') + "/")
               for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint not allowed: {endpoint!r}")

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: dict | None = None
) -> str:
    """
    Construct a safe redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The relative endpoint path (e.g. "/v1/users").
    query_options : dict, optional
        Mapping of query parameter names to values.

    Returns
    -------
    str
        The fully constructed URL ready for use as a redirect target.

    Raises
    ------
    ValueError
        If the base URL is not in the approved domain list,
        or if the endpoint is disallowed.
    """
    # Normalise and validate base URL
    normalized_base = _normalize_base_url(base_api_url)
    _validate_domain(normalized_base)

    # Ensure endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {api_endpoint!r}")

    # Validate endpoint against allowed list
    _validate_endpoint(api_endpoint)

    # Construct the full path (urljoin handles trailing slashes correctly)
    full_url = urllib.parse.urljoin(normalized_base, api_endpoint.lstrip("/"))

    # Append query parameters if provided
    if query_options:
        # Filter out None values and encode properly
        filtered = {k: v for k, v in query_options.items() if v is not None}
        query_string = urllib.parse.urlencode(filtered, doseq=True)
        full_url = f"{full_url}?{query_string}"

    return full_url

# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove in production)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     url = construct_api_redirect(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": 2, "limit": 50}
#     )
#     print(url)