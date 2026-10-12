import urllib.parse

# Allowed domains and endpoints – populate with real values in production.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


def create_api_redirect_link(base_url: str, path: str,
                             params: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    path : str
        The endpoint path to append (e.g., "/v1/users").
    params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL and ensure it contains a scheme
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Verify domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Normalise the path
    if not path.startswith("/"):
        path = "/" + path

    # Verify endpoint is allowed
    if path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {path}")

    # Merge the path with base URL
    joined = urllib.parse.urljoin(parsed_base.geturl(), path)

    # Add query parameters if provided
    if params:
        # Ensure all values are strings for proper encoding
        encoded_params = urllib.parse.urlencode(
            {k: str(v) for k, v in params.items()}
        )
        final_url = f"{joined}?{encoded_params}"
    else:
        final_url = joined

    return final_url