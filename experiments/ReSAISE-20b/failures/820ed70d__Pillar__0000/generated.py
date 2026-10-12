import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: approved domains and endpoints
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/search",
]

# ----------------------------------------------------------------------
# Helper: validate domain and endpoint
# ----------------------------------------------------------------------
def _validate_domain_and_endpoint(base_url: str, api_path: str) -> None:
    """
    Ensure the base URL's domain is approved and that the endpoint
    is in the allowed list.
    """
    parsed = urllib.parse.urlparse(base_url)
    domain = parsed.hostname
    if not domain or domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")

    # Normalize api_path (ensure leading slash)
    normalized_path = urllib.parse.urljoin("/", api_path)
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {normalized_path}")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API, e.g. "https://api.example.com"
    api_path : str
        Endpoint path to append, e.g. "/v1/users"
    query_dict : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The assembled URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Basic validation of inputs
    if not isinstance(base_api_url, str) or not base_api_url:
        raise ValueError("base_api_url must be a non-empty string")
    if not isinstance(api_path, str) or not api_path:
        raise ValueError("api_path must be a non-empty string")

    # Validate domain and endpoint
    _validate_domain_and_endpoint(base_api_url, api_path)

    # Build the path component
    joined = urllib.parse.urljoin(base_api_url.rstrip("/") + "/", api_path.lstrip("/"))

    # Attach query parameters if provided
    if query_dict:
        if not isinstance(query_dict, dict):
            raise ValueError("query_dict must be a dictionary")
        query_string = urllib.parse.urlencode(query_dict, doseq=True)
        assembled_url = f"{joined}?{query_string}"
    else:
        assembled_url = joined

    return assembled_url