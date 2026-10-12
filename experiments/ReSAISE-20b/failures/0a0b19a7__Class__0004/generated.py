import urllib.parse
from typing import Dict, Optional

# Example sets/lists – in real code these would be defined elsewhere
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/auth/login",
    "/auth/logout"
]


def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g., "https://api.example.com").
    endpoint : str
        Specific endpoint path (e.g., "/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the target domain is not approved or the endpoint is disallowed.
    """
    # Parse base URL
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("api_base_url must be a valid absolute URL")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize endpoint
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Validate endpoint
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build path
    # Use urljoin to correctly combine base and endpoint, preserving scheme/host
    full_path = urllib.parse.urljoin(parsed_base.geturl(), endpoint)

    # Append query parameters if provided
    if query_params:
        # Ensure values are strings; urlencode will handle proper escaping
        encoded_qs = urllib.parse.urlencode(
            {k: str(v) for k, v in query_params.items()}
        )
        full_path = f"{full_path}?{encoded_qs}"

    # Final safety check: parse again to ensure domain hasn't changed
    final_parsed = urllib.parse.urlparse(full_path)
    if final_parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError("Resulting URL points to an unapproved domain")

    return full_path