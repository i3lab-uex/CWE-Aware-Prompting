import urllib.parse

# ------------------------------------------------------------------
# Configuration: allowed domains and endpoints.
# These should be populated with the real values used by your application.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/v1/status",
]


def assemble_api_redirect_link(base_api_url: str,
                               api_path: str,
                               query_dict: dict | None = None) -> str:
    """
    Build a fully qualified API URL from a base URL, endpoint path and optional query
    parameters. The resulting URL is validated against a whitelist of approved domains
    and endpoints to mitigate open‑redirect attacks (CWE‑601).

    Parameters
    ----------
    base_api_url : str
        The root URL of the API (e.g. "https://api.example.com").
    api_path : str
        The endpoint path to append (e.g. "/users" or "orders").
    query_dict : dict | None, optional
        Dictionary of key/value pairs to be encoded as query parameters.

    Returns
    -------
    str
        The fully assembled and validated URL.

    Raises
    ------
    ValueError
        If the constructed URL points to an unapproved domain or endpoint.
    """
    # Ensure base API URL has a scheme
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme:
        raise ValueError(f"Base API URL must include a scheme (http/https): {base_api_url}")

    # Resolve the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))
    full_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",  # params
        urllib.parse.urlencode(query_dict or {}, doseq=True),
        ""   # fragment
    ))

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Validate endpoint
    # Normalise the path to avoid double slashes or trailing slashes.
    normalized_path = urllib.parse.urljoin("/", joined_path)
    if not any(normalized_path.startswith(e.rstrip("/")) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint not allowed: {normalized_path}")

    return full_url


# ------------------------------------------------------------------
# Example usage (commented out – remove to use in production)
#
# try:
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/users",
#         {"page": 2, "active": True}
#     )
#     print(url)
# except ValueError as e:
#     print(f"Invalid URL: {e}")