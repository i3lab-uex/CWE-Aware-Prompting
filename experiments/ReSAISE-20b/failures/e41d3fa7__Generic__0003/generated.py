import urllib.parse

# Trusted API domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
}

# Allowed endpoint paths (example values)
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}


def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: dict | None = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint (e.g., "/users").
    query_info : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the domain is not in APPROVED_API_DOMAINS or the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL to validate domain and scheme
    parsed_base = urllib.parse.urlparse(base_url)

    # Ensure the URL has http or https scheme
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Validate domain
    netloc = parsed_base.netloc.lower()
    if not any(netloc.endswith(domain) for domain in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not approved")

    # Normalize and validate endpoint path
    normalized_endpoint = urllib.parse.urljoin("/", endpoint_path)
    if not any(normalized_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed")

    # Merge path components
    full_path = urllib.parse.urljoin(parsed_base.path, normalized_endpoint)

    # Encode query parameters
    query_string = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        query_string = urllib.parse.urlencode(query_info, doseq=True)

    # Build the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            netloc,
            full_path,
            "",          # params
            query_string,
            "",          # fragment
        )
    )

    return final_url


# Example usage:
if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            base_url="https://api.example.com",
            endpoint_path="/users",
            query_info={"page": 2, "active": True}
        )
        print(url)  # https://api.example.com/users?page=2&active=True
    except ValueError as e:
        print(f"Invalid URL: {e}")