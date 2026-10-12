import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------
# Configuration – replace these with your actual values.
# --------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _validate_domain(base_url: str) -> None:
    """
    Ensure that the base URL belongs to an approved domain.
    Raises ValueError if not.
    """
    parsed = urllib.parse.urlparse(base_url)
    domain = parsed.netloc.lower()
    if not any(domain == approved or domain.endswith(f".{approved}") for approved in APPROVED_API_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not an approved API domain.")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure that the endpoint is in the allowed list.
    Raises ValueError if not.
    """
    # Normalise: ensure leading slash and case‑insensitive comparison
    endpoint_norm = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    if endpoint_norm.lower() not in (e.lower() for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not an allowed API endpoint.")


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API redirect URL from the given base, endpoint,
    and optional query parameters.

    Parameters
    ----------
    base_url_api : str
        The base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint to call (e.g., "/v1/users").
    opts : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain or endpoint is not approved.
    """
    # Validate inputs for security
    _validate_domain(base_url_api)
    _validate_endpoint(api_endpoint)

    # Build the base URL + endpoint
    full_url = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", api_endpoint.lstrip("/"))

    # Append query parameters if provided
    if opts:
        query_string = urllib.parse.urlencode(opts, doseq=True)
        full_url = f"{full_url}?{query_string}"

    return full_url


# --------------------------------------------------------------------
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "50"}
        )
        print(url)  # https://api.example.com/v1/users?page=2&limit=50
    except ValueError as e:
        print(f"Invalid URL configuration: {e}")