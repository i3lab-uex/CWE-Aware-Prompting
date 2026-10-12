import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – replace with real values in production
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
def _normalize_path(path: str) -> str:
    """
    Normalise a URL path by removing dot segments and ensuring it starts with a slash.
    This helps mitigate traversal attacks such as '/../../etc/passwd'.
    """
    # urllib.parse.urljoin normalises relative paths but we need a clean absolute path
    if not path.startswith("/"):
        path = "/" + path
    # Resolve dot segments
    return urllib.parse.urljoin("/", path)


def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the given network location (domain:port) is within the approved set.
    Ports are ignored for simplicity; adjust if needed.
    """
    domain = netloc.split(":")[0]  # strip port
    return domain in APPROVED_API_DOMAINS


def _is_allowed_endpoint(path: str) -> bool:
    """
    Verify that the path matches one of the allowed endpoints.
    Exact match is required; wildcards or prefixes can be added if desired.
    """
    return path in ALLOWED_ENDPOINTS


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        Base URL of the target API (e.g., "https://api.example.com").
    endpoint : str
        Endpoint path relative to the base URL (e.g., "/v1/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        A fully qualified URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    # 1. Resolve the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (http:// or https://).")

    # 2. Normalise and validate the endpoint
    normalized_endpoint = _normalize_path(endpoint)
    if not _is_allowed_endpoint(normalized_endpoint):
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed.")

    # 3. Construct the full URL path
    full_path = urllib.parse.urljoin(parsed_base.path, normalized_endpoint)

    # 4. Build query string
    query_string = urllib.parse.urlencode(query_params or {})

    # 5. Assemble the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    # 6. Validate the domain and endpoint again on the final URL
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not _is_approved_domain(parsed_redirect.netloc):
        raise ValueError(f"Domain '{parsed_redirect.netloc}' is not approved.")
    if not _is_allowed_endpoint(parsed_redirect.path):
        raise ValueError(f"Endpoint '{parsed_redirect.path}' is not allowed.")

    return redirect_url


# ------------------------------------------------------------------
# Example usage (commented out – remove in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = build_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "format": "json"},
        )
        print(url)
    except ValueError as e:
        print(f"Invalid URL: {e}")