import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – replace with real values in production code
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]

# ------------------------------------------------------------------
def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully qualified redirect URL for an API call.

    Parameters
    ----------
    base_api_url : str
        Base address of the target API (e.g., "https://api.example.com").
    api_endpoint : str
        Path component that identifies the API endpoint.
    query_options : dict[str, str] | None
        Optional dictionary of query string parameters.

    Returns
    -------
    str
        A safe, fully resolved URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the target domain is not approved or the endpoint is disallowed.
    """
    # Normalise base URL – ensure it ends with a slash so urljoin works
    if not base_api_url.endswith("/"):
        base_api_url += "/"

    # Normalise endpoint – strip leading slashes
    endpoint = api_endpoint.lstrip("/")

    # Construct preliminary URL without query parameters
    tentative_url = urllib.parse.urljoin(base_api_url, endpoint)

    # Parse the URL to inspect components
    parsed = urllib.parse.urlparse(tentative_url)

    # 1. Validate domain (netloc)
    if parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed.hostname}' is not in the list of approved API domains."
        )

    # 2. Validate endpoint path
    if parsed.path not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{parsed.path}' is not in the list of allowed endpoints."
        )

    # 3. Append query parameters if provided
    if query_options:
        query_string = urllib.parse.urlencode(query_options, doseq=True)
        # Rebuild URL with encoded query string
        final_url = parsed._replace(query=query_string).geturl()
    else:
        final_url = tentative_url

    return final_url