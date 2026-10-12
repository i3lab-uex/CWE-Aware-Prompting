import urllib.parse

# Example approved domains and allowed endpoints.
APPROVED_API_DOMAINS = {"api.example.com", "secure.api.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: dict | None = None
) -> str:
    """
    Build a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The API endpoint path (e.g., "/v1/users").
    optional_params : dict, optional
        Query string parameters to append.

    Returns
    -------
    str
        The complete API redirect URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in `APPROVED_API_DOMAINS` or
        if the endpoint is not in `ALLOWED_ENDPOINTS`.
    """
    # Parse the base URL to validate scheme and domain.
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Ensure the domain is approved.
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.hostname}' is not an approved API domain."
        )

    # Ensure the endpoint is allowed.
    normalized_endpoint = urllib.parse.urljoin("/", desired_endpoint)
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{normalized_endpoint}' is not an allowed endpoint."
        )

    # Construct the full path.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint)

    # Build query string if parameters are provided.
    query = ""
    if optional_params:
        if not isinstance(optional_params, dict):
            raise ValueError("optional_params must be a dictionary.")
        query = urllib.parse.urlencode(optional_params, doseq=True)

    # Assemble the final URL.
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return redirect_url

# Example usage:
if __name__ == "__main__":
    url = create_redirect_url(
        "https://api.example.com",
        "/v1/users",
        {"page": 2, "limit": 50}
    )
    print(url)  # https://api.example.com/v1/users?page=2&limit=50