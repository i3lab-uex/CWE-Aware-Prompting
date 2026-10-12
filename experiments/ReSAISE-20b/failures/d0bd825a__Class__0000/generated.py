import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to append (e.g. "/v1/users").
    opts : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        Fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse the base URL and validate domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Normalise the domain (strip port if present)
    netloc = parsed_base.netloc.split(":")[0]
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not approved")

    # Ensure the endpoint starts with a slash and is allowed
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Build the full path
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", api_endpoint.lstrip("/"))

    # Construct query string if options provided
    query = urllib.parse.urlencode(opts or {}, doseq=True)

    # Assemble the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            netloc,
            full_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return redirect_url