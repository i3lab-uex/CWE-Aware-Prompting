import urllib.parse

# Trusted domains and endpoints – adjust these to your environment.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}

ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "auth/login",
}

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: dict | None = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        Base URL of the API (e.g. "https://api.example.com/v1").
    endpoint_name : str
        Endpoint path relative to the base URL (e.g. "users").
    params_dict : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting domain is not approved or the endpoint is disallowed.
    """
    if params_dict is None:
        params_dict = {}

    # Parse the main URL to ensure it has a valid scheme and domain.
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Verify the domain is in the approved list.
    if parsed_main.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_main.netloc}' is not in the approved list."
        )

    # Ensure the endpoint is allowed.
    normalized_endpoint = endpoint_name.strip("/")
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_name}' is not permitted.")

    # Construct the path by joining base path and endpoint.
    base_path = parsed_main.path.rstrip("/")
    full_path = f"{base_path}/{normalized_endpoint}"

    # Encode query parameters.
    query_string = urllib.parse.urlencode(params_dict, doseq=True)

    # Rebuild the URL with updated path and query.
    new_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",  # params (deprecated)
        query_string,
        ""   # fragment
    )
    redirect_url = urllib.parse.urlunparse(new_parts)

    return redirect_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    url = construct_redirect_url(
        "https://api.example.com/v1",
        "users",
        {"page": 2, "per_page": 50}
    )
    print(url)   # https://api.example.com/v1/users?page=2&per_page=50