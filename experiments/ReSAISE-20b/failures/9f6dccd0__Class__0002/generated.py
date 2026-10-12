import urllib.parse

# Pre‑approved domains and safe endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.otherdomain.org",
    "v1.internal.api.local",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]


def generate_api_redirect(base_url: str, api_path: str,
                          params: dict | None = None) -> str:
    """
    Build a fully qualified redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        Base address of the target API, e.g. "https://api.example.com".
    api_path : str
        Endpoint path relative to the base, e.g. "/users/123".
    params : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        A fully constructed URL ready for redirection.

    Raises
    ------
    ValueError
        If the target domain is not in `APPROVED_API_DOMAINS` or if the
        endpoint is not listed in `ALLOWED_ENDPOINTS`.  The function also
        guards against relative paths that could escape the intended domain.
    """
    # Parse the base URL and verify its scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL: missing scheme or netloc")

    # Normalise domain (case‑insensitive) and check against approved set
    base_domain = parsed_base.netloc.lower()
    if base_domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not approved")

    # Ensure the api_path is a safe relative path
    if not api_path.startswith("/"):
        raise ValueError("Endpoint must start with a leading slash")

    # Strip any fragment or query from the base URL
    sanitized_base = urllib.parse.urlunparse(
        (parsed_base.scheme, parsed_base.netloc, "", "", "", "")
    )

    # Build the full path
    full_path = urllib.parse.urljoin(sanitized_base, api_path)

    # Validate the endpoint against the allowed list
    if not any(full_path.endswith(ep) for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Append query parameters if provided
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        full_path = f"{full_path}?{query_string}"

    return full_path