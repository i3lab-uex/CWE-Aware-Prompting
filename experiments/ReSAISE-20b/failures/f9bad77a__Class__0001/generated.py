import urllib.parse

# Trusted API domains and endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.safe.org",
    "secure.api.net",
}
ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "status",
}

def construct_redirect_url(main_url: str,
                           endpoint_name: str,
                           params_dict: dict | None = None) -> str:
    """
    Construct a full redirect URL for API requests.

    Parameters
    ----------
    main_url : str
        Base API URL (e.g., "https://api.example.com").
    endpoint_name : str
        Endpoint to append (e.g., "users").
    params_dict : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base URL is not from an approved domain,
        or if the endpoint is not allowed.
    """
    # Parse the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("Invalid base URL")

    # Ensure the domain is approved
    if parsed_main.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_main.hostname}' is not approved")

    # Validate the endpoint
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_name}' is not allowed")

    # Build the path safely
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = urllib.parse.quote(endpoint_name, safe="")
    full_path = f"{base_path}/{endpoint_path}"

    # Build query string
    query_string = ""
    if params_dict:
        # Ensure keys and values are strings to avoid injection issues
        safe_params = {
            str(k): str(v) for k, v in params_dict.items()
        }
        query_string = urllib.parse.urlencode(safe_params)

    # Reconstruct the full URL
    new_url = urllib.parse.urlunparse((
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    ))
    return new_url