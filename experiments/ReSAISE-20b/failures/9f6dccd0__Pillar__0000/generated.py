import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.secure.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/health",
]

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a safe redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    params : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Parse base URL to extract scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Domain validation
    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Endpoint validation
    if not api_path.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {api_path}")
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Construct the path component safely
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", api_path.lstrip("/"))

    # Assemble the URL without query string first
    url_parts = (
        parsed_base.scheme,
        domain,
        full_path,
        "",  # params
        "",  # fragment
    )
    url_without_query = urllib.parse.urlunparse(url_parts)

    # Append query parameters if provided
    if params:
        # Ensure all values are strings and encode them safely
        encoded_params = urllib.parse.urlencode(
            {k: str(v) for k, v in params.items()}
        )
        final_url = f"{url_without_query}?{encoded_params}"
    else:
        final_url = url_without_query

    return final_url