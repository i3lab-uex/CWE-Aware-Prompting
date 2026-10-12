import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and safe endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.com",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/posts",
    "/v2/analytics",
]


def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a safe redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path, e.g. "/v1/users".
    query_options : dict[str, str] | None
        Optional mapping of query parameters.

    Returns
    -------
    str
        Fully constructed, validated URL.

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS`` or if the endpoint
        is not in ``ALLOWED_ENDPOINTS``.
    """

    # ------------------------------------------------------------------
    # 1. Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL: missing scheme or host")

    # Normalize the netloc (lowercase, strip port if default)
    host = parsed_base.hostname.lower()
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the base URL without query or fragment
    cleaned_base = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            parsed_base.path.rstrip("/"),
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # ------------------------------------------------------------------
    # 2. Validate and normalize the endpoint
    if not api_endpoint.startswith("/"):
        raise ValueError("API endpoint must start with '/'")

    # Prevent path traversal
    if ".." in urllib.parse.unquote(api_endpoint):
        raise ValueError("API endpoint contains forbidden path traversal")

    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # ------------------------------------------------------------------
    # 3. Build the final URL
    full_path = urllib.parse.urljoin(cleaned_base + "/", api_endpoint.lstrip("/"))
    if query_options:
        # Ensure all keys/values are strings
        safe_query = {str(k): str(v) for k, v in query_options.items()}
        encoded_qs = urllib.parse.urlencode(safe_query)
        final_url = f"{full_path}?{encoded_qs}"
    else:
        final_url = full_path

    # ------------------------------------------------------------------
    # 4. Final sanity check: ensure the result is still in an approved domain
    parsed_final = urllib.parse.urlparse(final_url)
    final_host = parsed_final.hostname.lower()
    if final_host not in APPROVED_API_DOMAINS:
        raise ValueError("Constructed URL points to an unapproved domain")

    return final_url