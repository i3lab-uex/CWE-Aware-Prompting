import urllib.parse

# Pre‑approved API domains and endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.org",
    "data.somedomain.net",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

def construct_api_redirect(base_api_url: str,
                           api_endpoint: str,
                           query_options: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint to call (e.g. "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalize endpoint: strip leading/trailing whitespace, ensure it starts with '/'
    endpoint = api_endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Check that the endpoint is allowed
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path, endpoint)

    # Build query string if provided
    query = ""
    if query_options:
        if not isinstance(query_options, dict):
            raise ValueError("query_options must be a dictionary")
        query = urllib.parse.urlencode(query_options, doseq=True)

    # Assemble the final URL
    constructed_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",      # params
        query,   # query
        ""       # fragment
    ))

    return constructed_url

# Example usage:
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/v1/users",
        {"id": 123, "verbose": True}
    )
    print(url)   # https://api.example.com/v1/users?id=123&verbose=True