import urllib.parse
from typing import Dict, Optional

# Pre‑approved base API domains (scheme + hostname)
APPROVED_API_DOMAINS = {
    "https://api.example.com",
    "https://services.anotherdomain.org",
}

# Safe, allowable API endpoints (relative paths)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The base address of the target API (e.g. "https://api.example.com").
    api_path : str
        The relative endpoint path (e.g. "/v1/users").
    params : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in APPROVED_API_DOMAINS,
        or if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    # Normalise base URL (ensure scheme and no trailing slash)
    parsed_base = urllib.parse.urlparse(base_url.rstrip("/"))
    base_netloc = f"{parsed_base.scheme}://{parsed_base.netloc}"
    if base_netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_netloc}' is not approved.")

    # Normalise and validate endpoint
    api_path = urllib.parse.unquote(api_path)
    if not api_path.startswith("/"):
        raise ValueError(f"Endpoint '{api_path}' must start with '/'.")

    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed.")

    # Build the full path
    joined = urllib.parse.urljoin(base_netloc + "/", api_path.lstrip("/"))

    # Append query string if provided
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        joined = f"{joined}?{query}"

    return joined