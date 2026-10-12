import urllib.parse
from typing import Dict, Optional

# Allowed domains and endpoints (example values)
APPROVED_API_DOMAINS = {"api.example.com", "service.internal.local"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/health",
]

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a safe API redirect URL by validating the domain and endpoint.

    Args:
        base_url: The base API URL (e.g., "https://api.example.com")
        path:    The endpoint path to append (e.g., "/users")
        params:  Optional query parameters

    Returns:
        A fully constructed URL string.

    Raises:
        ValueError: If the domain or endpoint is not approved.
    """
    # Parse base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Domain check
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Endpoint check – allow exact match or prefix (e.g., /users/123)
    if not any(path == ep or path.startswith(f"{ep}/") for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{path}' is not allowed")

    # Build the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", path.lstrip("/"))

    # Encode query parameters if provided
    query = urllib.parse.urlencode(params) if params else ""

    # Assemble final URL components
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            joined_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return final_url