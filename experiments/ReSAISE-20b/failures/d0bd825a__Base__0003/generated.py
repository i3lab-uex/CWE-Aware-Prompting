import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – pre‑approved domains and safe endpoints
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    # add other trusted domains here
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/orders",
    # add other safe endpoints here
]

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _validate_domain(base_url: str) -> None:
    """
    Ensure that the base URL belongs to one of the approved domains.
    Raises ValueError if not.
    """
    parsed = urllib.parse.urlparse(base_url)
    domain = parsed.netloc.lower()
    if not any(domain == approved or domain.endswith("." + approved)
               for approved in APPROVED_API_DOMAINS):
        raise ValueError(f"Unapproved domain: {domain}")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure that the endpoint is in the list of allowed endpoints.
    Raises ValueError if not.
    """
    # Normalise endpoint – strip leading/trailing spaces
    ep = endpoint.strip()
    if not any(ep == allowed or ep.startswith(allowed + "/")
               for allowed in ALLOWED_ENDPOINTS):
        raise ValueError(f"Unapproved endpoint: {ep}")


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        The base address of the API (e.g., 'https://api.example.com')
    api_endpoint : str
        The endpoint path (e.g., '/v1/users')
    opts : dict, optional
        Query parameters to append to the URL

    Returns
    -------
    str
        The fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the base URL or endpoint is not approved.
    """
    # 1. Validate domain and endpoint
    _validate_domain(base_url_api)
    _validate_endpoint(api_endpoint)

    # 2. Build the path
    #   urljoin handles cases where base ends with or without a slash.
    full_path = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", api_endpoint.lstrip("/"))

    # 3. Append query parameters if any
    if opts:
        query = urllib.parse.urlencode(opts, doseq=True)
        full_path += f"?{query}"

    # 4. Normalise the URL (remove redundant slashes, etc.)
    parsed = urllib.parse.urlparse(full_path)
    normalized_url = urllib.parse.urlunparse(parsed)

    return normalized_url


# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = create_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": 123, "format": "json"}
        )
        print("Redirect URL:", url)
    except ValueError as e:
        print("Invalid redirect request:", e)