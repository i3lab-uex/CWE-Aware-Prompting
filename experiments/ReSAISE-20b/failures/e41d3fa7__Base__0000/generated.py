import urllib.parse

# Trusted domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
}
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: dict | None = None
) -> str:
    """
    Build a full redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g. "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g. "/users").
    query_info : dict, optional
        Dictionary of query string parameters to append.

    Returns
    -------
    str
        A fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the target domain or endpoint is not approved.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must include scheme and host")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalize the endpoint path
    if not endpoint_path.startswith("/"):
        endpoint_path = "/" + endpoint_path

    # Ensure the endpoint is allowed
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # Encode query parameters
    query_string = ""
    if query_info:
        # Only allow string or numeric values to avoid injection
        safe_query = {
            str(k): str(v) for k, v in query_info.items()
            if isinstance(k, (str, int)) and isinstance(v, (str, int))
        }
        query_string = urllib.parse.urlencode(safe_query)

    # Assemble the final URL
    new_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    return urllib.parse.urlunparse(new_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            base_url="https://api.example.com",
            endpoint_path="/users",
            query_info={"id": 42, "verbose": True}
        )
        print(url)  # https://api.example.com/users?id=42&verbose=True
    except ValueError as e:
        print(f"Invalid redirect: {e}")