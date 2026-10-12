import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.another.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/items",
    "/health",
]

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g. "https://api.example.com").
    api_path : str
        The endpoint path (e.g. "/v1/users").
    params : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Normalize and parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Validate domain
    domain = parsed_base.hostname
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Normalize endpoint path
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Validate endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Encode query parameters
    query = urllib.parse.urlencode(params or {})

    # Reconstruct the URL
    redirect_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query,
        ""   # fragment
    )
    redirect_url = urllib.parse.urlunparse(redirect_parts)

    return redirect_url