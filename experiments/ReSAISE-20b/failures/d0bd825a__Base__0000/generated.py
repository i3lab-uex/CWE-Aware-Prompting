import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: replace these with the real values for your application
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

# ----------------------------------------------------------------------
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The base address of the API, e.g. "https://api.example.com".
    api_endpoint : str
        The endpoint to call, e.g. "/v1/users".
    opts : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        A fully constructed redirect URL that is guaranteed to point to an
        approved domain and endpoint.

    Raises
    ------
    ValueError
        If the base URL or endpoint is not in the approved lists.
    """
    # ---- Validate base domain -------------------------------------------------
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url_api must be a valid absolute URL")

    # Normalize the domain (strip port, convert to lower case)
    netloc = parsed_base.netloc.split(":")[0].lower()
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not approved")

    # ---- Validate endpoint ----------------------------------------------------
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # ---- Build the full URL ---------------------------------------------------
    # Merge base and endpoint
    url = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", api_endpoint.lstrip("/"))

    # Add query parameters if provided
    if opts:
        # Ensure all values are strings for safe URL encoding
        query = urllib.parse.urlencode({k: str(v) for k, v in opts.items()})
        url = f"{url}?{query}"

    return url