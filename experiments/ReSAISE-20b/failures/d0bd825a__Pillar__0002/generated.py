import urllib.parse
from typing import Dict, Optional

# Pre‑approved API domains (scheme + host)
APPROVED_API_DOMAINS = {
    "https://api.example.com",
    "https://api.anotherdomain.org",
}

# Allowed API endpoints (path components)
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/status",
]

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a safe redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. 'https://api.example.com').
    api_endpoint : str
        Endpoint path of the API (e.g. '/users').
    opts : dict, optional
        Query parameters to append.

    Returns
    -------
    str
        A fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an approved domain or the endpoint is disallowed.
    """
    # Normalise base URL: strip trailing slash for consistent comparison
    base_url_norm = base_url_api.rstrip("/")
    if not any(base_url_norm == domain for domain in APPROVED_API_DOMAINS):
        raise ValueError("Base URL not approved")

    # Validate endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError("Endpoint not allowed")

    # Construct the URL path
    full_path = urllib.parse.urljoin(base_url_norm + "/", api_endpoint.lstrip("/"))

    # Append query parameters if provided
    if opts:
        # Ensure all keys and values are strings to avoid injection issues
        safe_opts = {str(k): str(v) for k, v in opts.items()}
        query_string = urllib.parse.urlencode(safe_opts)
        full_url = f"{full_path}?{query_string}"
    else:
        full_url = full_path

    # Final sanity check: ensure the URL is still within an approved domain
    parsed = urllib.parse.urlparse(full_url)
    base_of_parsed = f"{parsed.scheme}://{parsed.netloc}"
    if base_of_parsed not in APPROVED_API_DOMAINS:
        raise ValueError("Resulting URL is outside approved domains")

    return full_url