import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------
# Configuration:  Trusted domains and allowed endpoint paths.
# These should be populated with the real values for your deployment.
# --------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.example.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _is_domain_approved(url: str) -> bool:
    """
    Check if the netloc of a URL is in the approved domain list.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc.lower() in APPROVED_API_DOMAINS
    except Exception:
        return False


def _is_endpoint_allowed(path: str) -> bool:
    """
    Ensure the endpoint path is one of the permitted endpoints.
    Normalise leading slash for comparison.
    """
    normalized = urllib.parse.urljoin("/", path)
    return normalized in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint (e.g., "/v1/users").
    query_info : dict, optional
        Dictionary of query string parameters to be encoded.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the base URL's domain is not approved or the endpoint path is disallowed.
    """
    # 1. Validate base URL domain
    if not _is_domain_approved(base_url):
        raise ValueError(f"Unapproved domain in base URL: {base_url}")

    # 2. Validate endpoint path
    if not _is_endpoint_allowed(endpoint_path):
        raise ValueError(f"Disallowed endpoint path: {endpoint_path}")

    # 3. Build the base URL with endpoint
    # Ensure no double slashes: use urljoin on a normalized base.
    base = urllib.parse.urlparse(base_url)._replace(path="/")
    full_base = base.geturl()
    joined_path = urllib.parse.urljoin(full_base, endpoint_path)

    # 4. Encode query parameters if provided
    if query_info:
        # Ensure all keys and values are strings to avoid surprises.
        safe_query = {str(k): str(v) for k, v in query_info.items()}
        encoded_qs = urllib.parse.urlencode(safe_query)
        final_url = f"{joined_path}?{encoded_qs}"
    else:
        final_url = joined_path

    # 5. Final sanity check: the result should still be on an approved domain.
    if not _is_domain_approved(final_url):
        raise ValueError(f"Generated URL points to an unapproved domain: {final_url}")

    return final_url