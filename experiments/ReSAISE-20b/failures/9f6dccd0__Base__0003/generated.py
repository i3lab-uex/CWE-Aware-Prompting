import urllib.parse

# Pre‑approved API domains and endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/data",
    "/healthcheck",
]

def generate_api_redirect(base_url: str, api_path: str,
                          params: dict | None = None) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        Base address of the target API (e.g. "https://api.example.com").
    api_path : str
        Endpoint path to append to the base URL (e.g. "/v1/users").
    params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        Fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or uses a disallowed
        endpoint.
    """
    # Parse the base URL to isolate its components.
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base_url: missing scheme or netloc")

    # Ensure the domain is approved.
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize the endpoint path.
    api_path = urllib.parse.urljoin("/", api_path)  # ensures leading slash
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Build the path component.
    full_path = urllib.parse.urljoin(parsed_base.path, api_path)

    # Encode query parameters safely.
    query_string = urllib.parse.urlencode(params or {}, doseq=True)

    # Reconstruct the full URL.
    safe_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    ))

    return safe_url


# Example usage (for demonstration only; remove or guard under __main__ in production)
if __name__ == "__main__":
    url = generate_api_redirect(
        base_url="https://api.example.com",
        api_path="/v1/users",
        params={"id": 42, "verbose": True}
    )
    print(url)   # => https://api.example.com/v1/users?id=42&verbose=True