import urllib.parse

# Allowed domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.com",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/items",
    "/status",
]

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: dict | None = None
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_uri : str
        The base API URL (e.g., "https://api.example.com").
    api_endpoint : str
        The target endpoint (e.g., "/v1/users").
    query : dict, optional
        Optional query parameters.

    Returns
    -------
    str
        The fully assembled URL.

    Raises
    ------
    ValueError
        If the base URI's domain is not approved or if the endpoint is disallowed.
    """
    # Parse the base URI
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri}")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Validate endpoint
    if not any(api_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Disallowed endpoint: {api_endpoint}")

    # Merge path
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = api_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}"

    # Encode query parameters if any
    encoded_query = urllib.parse.urlencode(query) if query else ""

    # Reconstruct the full URL
    new_parts = parsed_base._replace(path=full_path, query=encoded_query)
    final_url = urllib.parse.urlunparse(new_parts)

    return final_url