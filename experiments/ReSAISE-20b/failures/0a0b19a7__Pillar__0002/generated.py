import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – adjust these to your environment
# --------------------------------------------------------------------------- #

# Set of domains that are allowed for API redirects.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
    "v1.myservice.io",
}

# List of endpoint paths that are permitted.  Each path should start with a
# leading slash, e.g., "/users", "/orders/list".
ALLOWED_ENDPOINTS = [
    "/status",
    "/health",
    "/users",
    "/orders/list",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_approved_domain(url: str) -> bool:
    """
    Return True if the netloc of *url* is in APPROVED_API_DOMAINS.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        # Remove port if present for comparison
        host, _, _ = parsed.netloc.partition(":")
        return host in APPROVED_API_DOMAINS
    except Exception:
        return False


def _is_allowed_endpoint(endpoint: str) -> bool:
    """
    Return True if *endpoint* is in ALLOWED_ENDPOINTS.
    The comparison is case-sensitive and requires a leading slash.
    """
    return endpoint in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main API redirect URL builder
# --------------------------------------------------------------------------- #

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API redirect URL.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API, e.g. "https://api.example.com".
    endpoint : str
        Specific endpoint path, must be in ALLOWED_ENDPOINTS.
    query_params : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        Fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or endpoint.
    """
    if not isinstance(api_base_url, str):
        raise TypeError("api_base_url must be a string")

    if not isinstance(endpoint, str):
        raise TypeError("endpoint must be a string")

    # Ensure the endpoint starts with a slash
    if not endpoint.startswith("/"):
        raise ValueError("endpoint must start with '/'")

    # Validate endpoint against the whitelist
    if not _is_allowed_endpoint(endpoint):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Combine base URL and endpoint safely
    combined = urllib.parse.urljoin(api_base_url.rstrip("/") + "/", endpoint.lstrip("/"))

    # Append query parameters if provided
    if query_params:
        if not isinstance(query_params, dict):
            raise TypeError("query_params must be a dictionary")
        # Encode parameters – urllib will handle percent-encoding
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        combined = f"{combined}?{query_string}"

    # Verify the domain is approved
    if not _is_approved_domain(combined):
        raise ValueError(f"Domain of URL '{combined}' is not approved")

    return combined