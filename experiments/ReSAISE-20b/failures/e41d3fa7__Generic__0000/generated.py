import urllib.parse
from typing import Dict, Optional

# Trusted domains and allowed endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.myapp.org",
}
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/health",
}

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Create a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g., "/users").
    query_info : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is not allowed.
    """
    # Parse base URL to validate scheme and domain
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Ensure the domain is approved
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Ensure the endpoint path is allowed
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # Encode query parameters if provided
    query_string = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        query_string = urllib.parse.urlencode(query_info, doseq=True)

    # Construct the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            ""   # fragment
        )
    )

    return redirect_url