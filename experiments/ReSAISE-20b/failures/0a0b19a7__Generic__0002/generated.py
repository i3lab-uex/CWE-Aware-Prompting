import urllib.parse

# Example approved domains and endpoints (should be defined elsewhere in your codebase)
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/search",
]

def build_api_redirect_url(api_base_url: str,
                           endpoint: str,
                           query_params: dict | None = None) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API, e.g. "https://api.example.com".
    endpoint : str
        Specific endpoint to call, e.g. "/users".
    query_params : dict | None, optional
        Optional query parameters to include in the URL.

    Returns
    -------
    str
        The fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (http:// or https://).")

    # Ensure the endpoint starts with a slash
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Validate the endpoint is allowed
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed.")

    # Build the full path by joining base path and endpoint
    # If base URL has a path, join it with the endpoint correctly.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint.lstrip("/"))

    # Construct the full URL without query
    url_without_query = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            "",  # query (empty for now)
            "",  # fragment
        )
    )

    # Append query parameters if provided
    if query_params:
        encoded_query = urllib.parse.urlencode(query_params, doseq=True)
        url_without_query += f"?{encoded_query}"

    # Parse the final URL to validate domain
    parsed_final = urllib.parse.urlparse(url_without_query)

    # Domain validation: ensure the netloc (hostname) is approved
    hostname = parsed_final.hostname
    if not hostname or hostname.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for API redirects.")

    return url_without_query