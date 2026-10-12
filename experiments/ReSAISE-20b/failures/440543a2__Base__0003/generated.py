import urllib.parse
from typing import Dict, Optional

# Define approved domains and allowed endpoints
APPROVED_API_DOMAINS = {"api.example.com", "service.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/auth/login",
    "/auth/logout"
]


def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure API redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    path : str
        The endpoint path to append (e.g., "/users").
    params : dict, optional
        Query parameters as key/value pairs.

    Returns
    -------
    str
        The fully assembled and validated URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse base URL to extract scheme and netloc
    parsed_base = urllib.parse.urlparse(base_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Validate domain
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalize and validate path
    cleaned_path = urllib.parse.urljoin("/", path)  # ensures leading slash
    if cleaned_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{cleaned_path}' is not allowed")

    # Build query string
    query_string = urllib.parse.urlencode(params or {})

    # Assemble final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        cleaned_path,
        "",          # params (deprecated)
        query_string,
        ""           # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            "https://api.example.com",
            "/users",
            {"id": "123", "detail": "full"}
        )
        print(url)
    except ValueError as e:
        print(f"Invalid URL: {e}")