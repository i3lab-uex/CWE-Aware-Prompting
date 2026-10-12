import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration: define the set of approved domains and allowed paths.
# These should be populated with real values in your application.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.partner.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]


def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified API URL by combining the base URL, path,
    and optional query parameters. The resulting URL is validated against
    a whitelist of approved domains and endpoints.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path to be appended (e.g., "/v1/users").
    query_dict : Optional[Dict[str, str]]
        Dictionary of query parameters to include.

    Returns
    -------
    str
        The assembled, validated URL.

    Raises
    ------
    ValueError
        If the constructed URL points to an unapproved domain or endpoint.
    """
    # Normalise base URL (remove trailing slash if present)
    base_api_url = base_api_url.rstrip("/")

    # Ensure the path starts with a slash
    if not api_path.startswith("/"):
        raise ValueError(f"api_path must start with '/': {api_path}")

    # Construct the full URL
    url = urllib.parse.urljoin(base_api_url + "/", api_path.lstrip("/"))

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(url)

    # Validate domain (netloc may include port)
    host = parsed.hostname
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")

    # Validate endpoint path (strip query part)
    path = parsed.path
    if path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {path}")

    # Encode query parameters if provided
    if query_dict:
        encoded_query = urllib.parse.urlencode(query_dict, doseq=True)
        url = parsed._replace(query=encoded_query).geturl()

    return url