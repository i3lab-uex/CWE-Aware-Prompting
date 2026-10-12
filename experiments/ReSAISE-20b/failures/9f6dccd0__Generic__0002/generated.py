import urllib.parse

# Pre-approved domains and safe endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
    "v1.backend.io"
}

ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/auth/login",
    "/status"
]


def generate_api_redirect(base_url: str, api_path: str,
                          params: dict | None = None) -> str:
    """
    Build a secure redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/users").
    params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL to extract scheme, netloc and path
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Verify domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' not approved")

    # Ensure api_path starts with a slash
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Verify endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Construct the full path
    # Preserve any existing path in base_url but replace it with api_path
    # Example: if base_url = https://api.example.com/v2, we want to use /users
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Build the full URL
    url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        urllib.parse.urlencode(params) if params else "",
        ""   # fragment
    )
    redirect_url = urllib.parse.urlunparse(url_parts)

    return redirect_url


# Example usage
if __name__ == "__main__":
    try:
        url = generate_api_redirect(
            "https://api.example.com/v2",
            "/users",
            {"id": 42, "verbose": True}
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")