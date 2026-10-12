import urllib.parse
from typing import Dict, Optional

# Pre‑approved base API domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.org",
}

# Allowed API endpoints (example values)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]


def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified API redirect URL.

    Parameters
    ----------
    base_url : str
        The base address of the API (e.g. "https://api.example.com").
    api_path : str
        The endpoint path (e.g. "/v1/users").
    params : dict, optional
        Query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within an approved domain or uses a disallowed endpoint.
    """
    # Parse the base URL to extract scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalise the API path
    cleaned_path = urllib.parse.urljoin("/", api_path.lstrip("/"))
    if not any(cleaned_path.startswith(endpoint) for endpoint in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{cleaned_path}' is not allowed")

    # Build the full path by joining base path and API path
    full_path = urllib.parse.urljoin(parsed_base.path, cleaned_path)

    # Construct the final URL
    url_parts = list(parsed_base)
    url_parts[2] = full_path  # path
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        url_parts[4] = query_string  # query
    else:
        url_parts[4] = ""

    redirect_url = urllib.parse.urlunparse(url_parts)

    # Final sanity check: ensure the resulting URL is still within an approved domain
    final_parsed = urllib.parse.urlparse(redirect_url)
    if final_parsed.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError("Redirect URL resolved to an unapproved domain")

    return redirect_url