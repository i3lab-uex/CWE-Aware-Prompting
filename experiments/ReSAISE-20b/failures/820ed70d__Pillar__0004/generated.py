import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – keep these sets up‑to‑date with your allowed domains
# and endpoints.  They are used to guard against open redirect or
# unintended API calls.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/items",
    "/status",
]

# ----------------------------------------------------------------------
def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a fully‑qualified API URL by combining the base URL, path,
    and optional query parameters while enforcing domain and endpoint
    restrictions.

    Parameters
    ----------
    base_api_url : str
        The API's base URL (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    query_dict : dict, optional
        A dictionary of query parameters to be appended.

    Returns
    -------
    str
        The validated, fully‑qualified URL.

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS`` or if the
        endpoint is not in ``ALLOWED_ENDPOINTS``.
    """
    # Parse and normalise the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalise the path – ensure it starts with a slash
    api_path = urllib.parse.urljoin("/", api_path.lstrip("/"))

    # Validate endpoint – exact match against the allowed list
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Construct the new URL components
    url_components = list(parsed_base)
    url_components[2] = api_path  # path
    url_components[3] = ""       # params (unused)
    url_components[4] = ""       # fragment (removed)

    # Encode query parameters if provided
    if query_dict:
        # Ensure all values are strings to avoid encoding issues
        safe_query = {k: str(v) for k, v in query_dict.items()}
        url_components[4] = urllib.parse.urlencode(safe_query)

    final_url = urllib.parse.urlunparse(url_components)
    return final_url