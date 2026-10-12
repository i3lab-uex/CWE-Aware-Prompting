import urllib.parse
from typing import Dict, Optional

# Trusted domains and allowed endpoints for security
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v2/items",
    "/status",
}

class InvalidRedirectError(ValueError):
    """Raised when the redirect URL is not allowed."""
    pass

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully-qualified redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base of the API (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint (e.g., "/v1/users").
    query_info : dict, optional
        Mapping of query string parameters.

    Returns
    -------
    str
        The fully-formed redirect URL.

    Raises
    ------
    InvalidRedirectError
        If the resulting domain is not in APPROVED_API_DOMAINS or
        the endpoint_path is not in ALLOWED_ENDPOINTS.
    """
    # Normalise and parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise InvalidRedirectError("Invalid base URL")

    # Ensure the domain is approved
    host = parsed_base.hostname or ""
    if host not in APPROVED_API_DOMAINS:
        raise InvalidRedirectError(f"Domain '{host}' is not approved")

    # Validate endpoint path
    if not endpoint_path.startswith("/"):
        endpoint_path = "/" + endpoint_path
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise InvalidRedirectError(f"Endpoint '{endpoint_path}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path or "/", endpoint_path.lstrip("/"))

    # Encode query parameters
    if query_info:
        encoded_query = urllib.parse.urlencode(query_info, doseq=True)
    else:
        encoded_query = ""

    # Reconstruct the final URL
    final_url_parts = (
        parsed_base.scheme,
        host,
        full_path,
        "",  # params
        encoded_query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            base_url="https://api.example.com",
            endpoint_path="/v1/users",
            query_info={"id": "123", "verbose": "true"}
        )
        print(url)  # https://api.example.com/v1/users?id=123&verbose=true
    except InvalidRedirectError as exc:
        print(f"Redirect blocked: {exc}")