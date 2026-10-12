import urllib.parse

# Trusted API domains (example entries)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
}

# Allowed endpoints (example entries)
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/analytics",
}

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: dict | None = None
) -> str:
    """
    Construct a full API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The specific endpoint to append (e.g., "/v1/users").
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the base URL domain is not approved or the endpoint is disallowed.
    """
    # 1. Parse the base URL and validate domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Normalise the netloc to lower case for comparison
    base_domain = parsed_base.netloc.lower()
    if base_domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not approved for API requests")

    # 2. Validate the endpoint
    # Ensure it starts with a slash and is in the allowed list
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with a leading slash '/'")
    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{desired_endpoint}' is not permitted")

    # 3. Construct the full path
    # urljoin handles leading/trailing slashes appropriately
    full_path = urllib.parse.urljoin(parsed_base.path + "/", desired_endpoint.lstrip("/"))

    # 4. Encode optional query parameters
    query = urllib.parse.urlencode(optional_params or {}, doseq=True)

    # 5. Rebuild the URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",          # params
        query,       # query
        ""           # fragment
    ))

    return final_url

# Example usage (uncomment to test):
# print(create_redirect_url(
#     "https://api.example.com",
#     "/v1/users",
#     {"page": 2, "sort": "name"}
# ))