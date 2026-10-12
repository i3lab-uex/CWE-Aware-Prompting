import urllib.parse
from typing import Dict, Optional

# Pre‑approved API domains (e.g. "api.example.com")
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

# Allowed endpoint paths (e.g. "/v1/users")
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/items",
    "/health",
]


def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        Base address of the API (e.g. "https://api.example.com").
    api_path : str
        Endpoint path to append (e.g. "/v1/users").
    params : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an approved domain or uses a disallowed endpoint.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_base.netloc} is not approved")

    # Normalize and validate the endpoint
    normalized_endpoint = urllib.parse.urljoin("/", api_path)
    if not any(normalized_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint {api_path} is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Encode query parameters if provided
    query = urllib.parse.urlencode(params or {}, doseq=True)

    # Reconstruct the final URL
    redirect = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return redirect