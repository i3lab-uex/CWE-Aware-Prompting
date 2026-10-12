import urllib.parse

# Allowed domains and endpoints – replace with real values as needed
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.otherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def create_api_redirect_link(base_url: str, path: str, params: dict | None = None) -> str:
    """
    Build a fully-qualified API URL from a base, path and optional query parameters.
    
    Parameters
    ----------
    base_url : str
        The API's base URL (e.g. "https://api.example.com").
    path : str
        The endpoint path (must start with a '/').
    params : dict, optional
        Key/value pairs to be encoded as query parameters.
    
    Returns
    -------
    str
        The complete URL ready for use.
    
    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    if not path.startswith("/"):
        raise ValueError("Endpoint path must start with '/'")

    # Parse the base URL to extract its domain
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must be a valid absolute URL")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Ensure the endpoint is allowed
    if path.lower() not in [e.lower() for e in ALLOWED_ENDPOINTS]:
        raise ValueError(f"Endpoint '{path}' is not approved")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", path.lstrip("/"))

    # Build query string if parameters are supplied
    query = urllib.parse.urlencode(params or {}, doseq=True)

    # Assemble the final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",          # params component (deprecated)
        query,
        ""           # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": 2, "limit": 50}
        )
        print(url)
    except ValueError as exc:
        print(f"Invalid URL construction: {exc}")