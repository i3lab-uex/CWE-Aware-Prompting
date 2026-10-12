import urllib.parse

# Example approved domains and endpoints – replace with real values.
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

def generate_api_redirect(base_url: str, api_path: str,
                          params: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        Base address of the API (e.g., "https://api.example.com").
    api_path : str
        Endpoint path (must start with a slash, e.g., "/v1/users").
    params : dict | None
        Optional query parameters.

    Returns
    -------
    str
        Fully constructed, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not approved or the endpoint is disallowed.
    """
    # Normalize and parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must be absolute and include scheme")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Ensure endpoint starts with a slash and is allowed
    if not api_path.startswith("/"):
        raise ValueError("API path must start with '/'")
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Build the path by joining base path and endpoint
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Construct query string if parameters are provided
    query = urllib.parse.urlencode(params) if params else ""

    # Assemble final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        combined_path,
        "",  # params (deprecated)
        query,
        ""   # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    url = generate_api_redirect(
        "https://api.example.com",
        "/v1/users",
        {"id": 42, "verbose": True}
    )
    print(url)   # https://api.example.com/v1/users?id=42&verbose=True