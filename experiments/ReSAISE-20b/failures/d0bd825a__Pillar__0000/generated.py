import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be defined elsewhere in your application.
# They are kept here for completeness of this example.

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.foo.org",
    "backend.bar.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/auth/login",
]

# --------------------------------------------------------------------------- #
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        Base address of the target API (e.g. 'https://api.example.com').
    api_endpoint : str
        Endpoint path to be appended (e.g. '/v1/users').
    opts : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        Fully qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """

    # 1. Parse the base URL and ensure it uses HTTP/HTTPS
    parsed_base = urllib.parse.urlparse(base_url_api)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed_base.scheme}'. Only http/https are allowed.")

    # 2. Validate the host against approved domains
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not in the list of approved API domains.")

    # 3. Normalize and validate endpoint
    # Ensure it starts with a slash and does not contain '..' or multiple slashes.
    normalized_endpoint = urllib.parse.urljoin("/", api_endpoint)
    if not any(normalized_endpoint == allowed or normalized_endpoint.startswith(allowed + "/") for allowed in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed.")

    # 4. Build the full path
    # urljoin handles trailing slashes correctly.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint)

    # 5. Assemble query string if provided
    query = urllib.parse.urlencode(opts) if opts else ""

    # 6. Reconstruct the final URL
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",          # params
        query,       # query
        ""           # fragment
    ))

    return redirect_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# try:
#     url = create_api_redirect_url(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": "2", "sort": "asc"}
#     )
#     print(url)
# except ValueError as e:
#     print(f"Error: {e}")