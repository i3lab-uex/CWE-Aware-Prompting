import urllib.parse

# Example sets of approved domains and allowed endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
}

ALLOWED_ENDPOINTS = {
    "users",
    "orders",
    "products",
    "auth/login",
}

def construct_redirect_url(main_url: str, endpoint_name: str,
                           params_dict: dict | None = None) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        Base URL of the API (e.g. "https://api.example.com/").
    endpoint_name : str
        Endpoint to append (e.g. "users" or "auth/login").
    params_dict : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in ``APPROVED_API_DOMAINS`` or
        if ``endpoint_name`` is not in ``ALLOWED_ENDPOINTS``.
    """
    # Parse the main URL to ensure it is valid
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Verify domain is approved
    if parsed_main.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_main.hostname!r} is not approved")

    # Normalise endpoint (strip leading/trailing slashes)
    endpoint = endpoint_name.strip("/")
    if not endpoint:
        raise ValueError("Endpoint name cannot be empty")

    # Verify endpoint is allowed
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {endpoint!r} is not allowed")

    # Construct the path
    # Ensure we don't duplicate slashes when joining
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = f"{base_path}/{endpoint}"
    full_url = urllib.parse.urlunparse(
        parsed_main._replace(path=endpoint_path)
    )

    # Append query parameters if provided
    if params_dict:
        # Encode safely; avoid list or tuple values that could lead to duplicate keys
        query = urllib.parse.urlencode(params_dict, doseq=False)
        full_url = f"{full_url}?{query}"

    return full_url