import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: approved domains and endpoints.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.myapp.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ----------------------------------------------------------------------
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified API URL from a base, endpoint path,
    and optional query parameters while ensuring that the target
    domain and path are approved.

    Args:
        base_url: Base URL of the API (e.g., "https://api.example.com").
        path: Endpoint path to append (must start with '/').
        params: Optional dictionary of query parameters.

    Returns:
        A validated, absolute URL string ready for use as a redirect target.

    Raises:
        ValueError: If the resulting domain is not in `APPROVED_API_DOMAINS`
                    or if the path is not in `ALLOWED_ENDPOINTS`.
    """
    # Validate that base_url contains a scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Ensure the domain is approved
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Normalise and validate the path
    if not path.startswith("/"):
        raise ValueError("Endpoint path must start with '/'")
    # Prevent traversal or double slashes
    clean_path = urllib.parse.normpath(path)
    if clean_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {clean_path}")

    # Build the final URL
    # urljoin will handle trailing slashes correctly
    joined = urllib.parse.urljoin(base_url.rstrip("/") + "/", clean_path.lstrip("/"))
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        joined = f"{joined}?{query}"

    return joined