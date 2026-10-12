import urllib.parse
from typing import Dict, Optional

# Pre‑approved base API domains (e.g. only trusted third‑party services)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.com",
    "trusted.api.org",
}

# List of safe, allowable API endpoints
ALLOWED_ENDPOINTS = [
    "users",
    "posts",
    "comments",
    "auth/login",
    "status/health",
]

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint to be appended to the base URL (e.g. "users").
    opts : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is not allowed.
    """
    # ---- Validate the base URL ----
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url_api must be a valid URL with scheme and netloc")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not an approved API domain")

    # ---- Sanitize and validate the endpoint ----
    # Remove leading/trailing slashes to avoid accidental double slashes or traversal
    cleaned_endpoint = api_endpoint.strip("/")
    if cleaned_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not an allowed API endpoint")

    # ---- Build the full path ----
    # Ensure we combine paths correctly regardless of trailing slashes in base_url_api
    full_path = urllib.parse.urljoin(parsed_base.path + "/", cleaned_endpoint)

    # ---- Assemble query parameters ----
    query = urllib.parse.urlencode(opts) if opts else ""

    # ---- Construct the final URL ----
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    ))

    return redirect_url

# Example usage (uncomment to test):
# url = create_api_redirect_url(
#     "https://api.example.com",
#     "/users",
#     {"id": "123", "format": "json"}
# )
# print(url)  # https://api.example.com/users?id=123&format=json