import urllib.parse
from typing import Dict, Optional

# Example allowed domains and endpoints – replace with real values in production
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/public/info",
]

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        Base address of the target API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint to append to the base URL (e.g. "/v1/users").
    opts : dict, optional
        Dictionary of query parameters to add.

    Returns
    -------
    str
        A fully formed, validated URL.

    Raises
    ------
    ValueError
        If the target domain is not approved or the endpoint is disallowed.
    """
    # Normalize and parse base URL
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Verify domain is approved
    if parsed_base.netloc.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Verify endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Build the path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Build query string
    query = urllib.parse.urlencode(opts or {}, doseq=True)

    # Assemble final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",  # params
        query,
        ""   # fragment
    ))

    return final_url