import urllib.parse

# Example approved domains and allowed endpoints.
APPROVED_API_DOMAINS = {"api.example.com", "api2.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/likes",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: dict | None = None,
) -> str:
    """
    Construct a secure redirect URL for an API response.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        The specific API endpoint (e.g. "/users").
    query_params : dict, optional
        A dictionary of query parameters to append to the URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in ``APPROVED_API_DOMAINS`` or if the
        endpoint is not in ``ALLOWED_ENDPOINTS``.
    """
    # Parse the base URL to validate scheme and domain
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("api_base_url must be a valid absolute URL")

    # Validate domain
    base_domain = parsed_base.netloc.split(":")[0]  # ignore port if present
    if base_domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not approved")

    # Ensure endpoint starts with a slash
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Validate endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the path by joining base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", endpoint.lstrip("/"))

    # Build query string
    query_string = ""
    if query_params:
        if not isinstance(query_params, dict):
            raise ValueError("query_params must be a dictionary")
        # Encode parameters safely
        query_string = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return final_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    url = build_api_redirect_url(
        "https://api.example.com",
        "/users",
        {"page": 2, "limit": 50},
    )
    print(url)   # https://api.example.com/users?page=2&limit=50