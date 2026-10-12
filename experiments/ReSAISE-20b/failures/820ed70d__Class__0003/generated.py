import urllib.parse
from typing import Dict, Optional

# Allowed domains and endpoints. In a real application these would be
# configured in a secure place, not hard‑coded.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a fully qualified API URL by combining the base API URL, an endpoint
    path and optional query parameters.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g. "https://api.example.com").
    api_path : str
        The endpoint path to append (e.g. "/v1/users").
    query_dict : dict[str, str], optional
        Mapping of query parameter names to values.

    Returns
    -------
    str
        The assembled URL ready for redirection or request.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed
        endpoint path.
    """
    if not base_api_url:
        raise ValueError("base_api_url must be a non-empty string")
    if not api_path:
        raise ValueError("api_path must be a non-empty string")

    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme:
        base_api_url = "https://" + base_api_url
        parsed_base = urllib.parse.urlparse(base_api_url)

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname}")

    # Normalise the endpoint path
    normalized_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))
    # Ensure the endpoint is allowed
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {normalized_path}")

    # Build the final URL
    scheme = parsed_base.scheme
    netloc = parsed_base.netloc
    path = normalized_path

    # Merge existing query parameters from the base URL (if any)
    existing_query = urllib.parse.parse_qs(parsed_base.query, keep_blank_values=True)

    # Merge with new query_dict
    if query_dict:
        for key, value in query_dict.items():
            existing_query[key] = [value]

    # Construct the final query string
    final_query = urllib.parse.urlencode(existing_query, doseq=True)

    assembled_url = urllib.parse.urlunparse(
        (scheme, netloc, path, "", final_query, "")
    )
    return assembled_url