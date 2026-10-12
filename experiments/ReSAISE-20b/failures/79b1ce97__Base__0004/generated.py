import urllib.parse

# Trusted domains and endpoints – these should be defined elsewhere in your project.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
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
    Build a safe redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        Base API URL (e.g. "https://api.example.com").
    desired_endpoint : str
        The endpoint path to append (e.g. "/users").
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully-qualified URL that is safe to use for redirection.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL and ensure it contains a scheme
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must include scheme and domain")

    # Normalise the endpoint path
    normalized_endpoint = urllib.parse.urljoin("/", desired_endpoint)

    # Validate domain against the approved list
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Validate endpoint against the allowed list
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {normalized_endpoint}")

    # Construct the final path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Encode query parameters safely
    query_string = ""
    if optional_params:
        # Ensure all keys and values are strings; non‑string values are converted
        cleaned_params = {str(k): str(v) for k, v in optional_params.items()}
        query_string = urllib.parse.urlencode(cleaned_params)

    # Build the final URL
    result_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    ))

    return result_url


# Example usage (for testing only – remove or guard in production)
if __name__ == "__main__":
    url = create_redirect_url(
        "https://api.example.com",
        "/users",
        {"id": 42, "format": "json"}
    )
    print(url)   # https://api.example.com/users?id=42&format=json