import urllib.parse

# Trusted API domains and endpoints – adjust these to your environment
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

def create_redirect_url(base_url_api: str,
                        desired_endpoint: str,
                        optional_params: dict | None = None) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The endpoint path to append (e.g., "/users").
    optional_params : dict, optional
        Query string parameters to include.

    Returns
    -------
    str
        A fully formed URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Normalize and parse base URL
    parsed_base = urllib.parse.urlparse(base_url_api.rstrip('/'))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Ensure the endpoint is allowed
    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {desired_endpoint}")

    # Build the path by joining base path and desired endpoint
    # The base path may already contain a trailing slash
    full_path = urllib.parse.urljoin(parsed_base.path + '/', desired_endpoint.lstrip('/'))

    # Build the query string
    query = urllib.parse.urlencode(optional_params or {}, doseq=True)

    # Reconstruct the full URL
    new_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        '',  # params
        query,
        ''   # fragment
    ))

    return new_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    url = create_redirect_url(
        base_url_api="https://api.example.com",
        desired_endpoint="/users",
        optional_params={"id": 42, "verbose": True}
    )
    print(url)   # https://api.example.com/users?id=42&verbose=True