import urllib.parse
from typing import Dict, Optional

# Allowed API domains and endpoints – populate with real values in production
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/data",
    "/health",
]


def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full API URL by safely combining a base URL, an endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g., "https://api.example.com").
    api_path : str
        Endpoint path to append (e.g., "/v1/users").
    query_dict : dict, optional
        Dictionary of key/value pairs to encode as query string.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL contains an unapproved domain or endpoint.
    """
    # Normalize base URL: strip trailing slash for consistency
    base_api_url = base_api_url.rstrip("/")

    # Validate domain
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base API URL must include scheme and netloc")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Ensure api_path starts with a single slash
    if not api_path.startswith("/"):
        api_path = "/" + api_path

    # Validate endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Build the full URL
    full_url = urllib.parse.urljoin(base_api_url + "/", api_path.lstrip("/"))

    # Append query parameters if provided
    if query_dict:
        # Ensure all keys/values are strings; convert others to string
        safe_query = {str(k): str(v) for k, v in query_dict.items()}
        query_string = urllib.parse.urlencode(safe_query)
        full_url += f"?{query_string}"

    # Final safety check: ensure the resulting URL still uses an approved domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() != domain:
        raise ValueError("URL manipulation resulted in a different domain")

    return full_url