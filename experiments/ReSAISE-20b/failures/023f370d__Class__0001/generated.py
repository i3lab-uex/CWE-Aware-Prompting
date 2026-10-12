import urllib.parse

# --------------------------------------------------------------------------- #
# Configuration – replace or extend these with your real values.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.internal.local",
    "secure.api.company.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
    "/public/info",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_approved_domain(url: str) -> bool:
    """
    Verify that the netloc of the given URL belongs to an approved domain.
    The comparison is case‑insensitive and ignores leading www.
    """
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    # Strip common subdomains like www.
    if domain.startswith("www."):
        domain = domain[4:]
    return domain in APPROVED_API_DOMAINS


def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Check that the endpoint is in the whitelist.
    Normalise leading/trailing slashes for comparison.
    """
    # Ensure endpoint starts with a single slash
    normalized = "/" + endpoint.lstrip("/")
    return normalized in ALLOWED_ENDPOINTS


def _build_query_string(params: dict | None) -> str:
    """
    Encode query parameters safely.
    If params is None or empty, return an empty string.
    """
    if not params:
        return ""
    # urllib.parse.urlencode handles proper escaping
    return urllib.parse.urlencode(params, doseq=True)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: dict | None = None
) -> str:
    """
    Construct a full redirect URL for an API call.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g., "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL uses an unapproved domain or an endpoint that is not in
        the whitelist. This protects against CWE‑610 (Externally Controlled Reference).
    """
    # Normalise base URL to ensure it ends with a slash
    if not base_api_url.endswith("/"):
        base_api_url += "/"

    # Normalise endpoint to avoid double slashes
    api_endpoint = api_endpoint.lstrip("/")

    # Build the full URL before validation to catch any malformed input
    full_url = urllib.parse.urljoin(base_api_url, api_endpoint)

    # Validate domain
    if not _is_approved_domain(full_url):
        raise ValueError(f"Unapproved domain in URL: {full_url}")

    # Validate endpoint
    if not _is_allowed_endpoint(api_endpoint):
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Append query string if provided
    query_string = _build_query_string(query_options)
    if query_string:
        full_url += f"?{query_string}"

    return full_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         url = construct_api_redirect(
#             "https://api.example.com",
#             "/v1/users",
#             {"page": 2, "sort": "asc"}
#         )
#         print(url)
#     except ValueError as e:
#         print(f"Error: {e}")