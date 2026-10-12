import urllib.parse

# --------------------------------------------------------------------
# Configuration – keep these values up‑to‑date with your deployment.
# --------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.company.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------
# Helper – normalise endpoint path
# --------------------------------------------------------------------
def _normalise_endpoint(endpoint: str) -> str:
    """
    Ensure the endpoint starts with a single leading slash and has no
    trailing slashes (except for root '/').
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    # collapse multiple slashes, but preserve leading slash
    parts = [p for p in endpoint.split("/") if p]
    return "/" + "/".join(parts)

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: dict | None = None,
) -> str:
    """
    Build a safe API redirect URL.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g. "/v1/users").
    query : dict, optional
        Query parameters to append.

    Returns
    -------
    str
        A fully formed URL ready for use in a redirect.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Parse base URI to validate domain
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname!r}")

    # Normalise and validate endpoint
    endpoint = _normalise_endpoint(api_endpoint)
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed API endpoint: {endpoint!r}")

    # Merge paths safely
    combined_path = urllib.parse.urljoin(parsed_base.path or "/", endpoint)

    # Build query string
    query_string = urllib.parse.urlencode(query, doseq=True) if query else ""

    # Reconstruct final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        combined_path,
        "",          # params
        query_string,  # query
        ""           # fragment
    ))

    return final_url

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     print(generate_api_redirect_uri(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": 42, "verbose": True}
#     ))