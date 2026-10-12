import urllib.parse

# Example sets – replace with real values in your application
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/health",
]


def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: dict | None = None,
) -> str:
    """
    Construct a full API redirect URL from the base URL, endpoint and optional
    query parameters.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        Specific API endpoint to call (e.g. "/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully-qualified URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed
        endpoint.
    """
    # Normalise base URL and endpoint to avoid double slashes
    parsed_base = urllib.parse.urlparse(api_base_url.rstrip("/"))
    endpoint_path = endpoint.lstrip("/")
    full_path = f"/{endpoint_path}"

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Unapproved API domain: {parsed_base.netloc!r}. "
            f"Approved domains are: {', '.join(sorted(APPROVED_API_DOMAINS))}"
        )

    # Validate endpoint
    if full_path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Disallowed endpoint: {full_path!r}. "
            f"Allowed endpoints are: {', '.join(ALLOWED_ENDPOINTS)}"
        )

    # Build query string if provided
    query_string = ""
    if query_params:
        # Ensure all values are converted to strings for urlencode
        safe_query = {k: str(v) for k, v in query_params.items()}
        query_string = urllib.parse.urlencode(safe_query)

    # Assemble the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return redirect_url