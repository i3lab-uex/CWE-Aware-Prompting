import urllib.parse

# Pre‑approved API domains and endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.internal.org",
    "data.company.net",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/status",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: dict | None = None
) -> str:
    """
    Build a safe API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g. 'https://api.example.com')
    api_endpoint : str
        Endpoint path to append (e.g. '/v1/users')
    query_options : dict, optional
        Dictionary of query parameters to add

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the target domain is not in APPROVED_API_DOMAINS or
        if the endpoint is not listed in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Ensure endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Validate endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path, api_endpoint)

    # Build query string
    if query_options:
        query_string = urllib.parse.urlencode(query_options, doseq=True)
    else:
        query_string = ""

    # Reconstruct the URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            query_string,
            "",          # fragment
        )
    )

    return redirect_url

# Example usage (for testing purposes)
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/v1/users",
        {"page": 2, "sort": "name"}
    )
    print(url)   # https://api.example.com/v1/users?page=2&sort=name