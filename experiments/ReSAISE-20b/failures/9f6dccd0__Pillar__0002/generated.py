import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
    "data.partner.net",
}

# Allowed endpoints (example values)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/health",
]

def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        Base address of the API, e.g. "https://api.example.com".
    api_path : str
        Endpoint path, e.g. "/v1/users".
    params : dict | None, optional
        Optional query parameters.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the target domain is not in APPROVED_API_DOMAINS or the endpoint
        is not in ALLOWED_ENDPOINTS.
    """
    # Parse base URL to isolate scheme and network location
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_base.netloc}' is not approved for API redirects."
        )

    # Normalize endpoint: ensure it starts with a slash
    normalized_path = api_path if api_path.startswith("/") else f"/{api_path}"

    # Validate endpoint
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{normalized_path}' is not in the list of allowed endpoints."
        )

    # Build full path (base + endpoint)
    joined_path = urllib.parse.urljoin(parsed_base.path, normalized_path)

    # Assemble the new URL components
    url_parts = list(parsed_base)
    url_parts[2] = joined_path  # path
    url_parts[4] = urllib.parse.urlencode(params or {}, doseq=True)  # query

    redirect_url = urllib.parse.urlunparse(url_parts)

    return redirect_url