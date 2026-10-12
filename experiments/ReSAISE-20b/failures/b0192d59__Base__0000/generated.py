import urllib.parse

# Domains that are allowed to be used as the base of an API URL.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

# Endpoints that are authorized for use.
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


def generate_api_redirect_uri(base_uri: str, api_endpoint: str,
                               query: dict | None = None) -> str:
    """
    Construct a secure API redirect URI by validating the base domain and
    endpoint, then appending optional query parameters.

    Parameters
    ----------
    base_uri : str
        Base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint to append (e.g. "/v1/users").
    query : dict, optional
        Key/value pairs to be encoded as query string parameters.

    Returns
    -------
    str
        Fully-qualified, validated URL.

    Raises
    ------
    ValueError
        If the base domain is not in `APPROVED_API_DOMAINS` or if the
        endpoint is not in `ALLOWED_ENDPOINTS`.
    """
    # Parse the base URI and verify the scheme
    parsed_base = urllib.parse.urlparse(base_uri)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed_base.scheme}")

    # Verify the domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Normalise the endpoint
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Ensure the endpoint is allowed
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {api_endpoint}")

    # Build the path by joining base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", api_endpoint.lstrip("/"))

    # Encode query parameters if provided
    encoded_query = urllib.parse.urlencode(query) if query else ""

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            encoded_query,
            "",          # fragment
        )
    )

    return final_url


# Example usage (uncomment to test):
# print(generate_api_redirect_uri(
#     "https://api.example.com",
#     "/v1/users",
#     {"id": 123, "active": True}
# ))