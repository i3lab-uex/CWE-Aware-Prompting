import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------
# Allowed domains and endpoints – normally populated from config.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.secure.net",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/items",
    "/orders",
]

# --------------------------------------------------------------------
def _is_allowed_domain(netloc: str) -> bool:
    """Return True if the hostname is in the approved list."""
    # Strip port if present
    host = netloc.split(":")[0].lower()
    return host in APPROVED_API_DOMAINS


def _is_allowed_endpoint(path: str) -> bool:
    """Return True if the endpoint is in the allowed list."""
    # Normalize path: strip trailing slash, ensure leading slash
    normalized = urllib.parse.urljoin("/", path.rstrip("/"))
    return normalized in ALLOWED_ENDPOINTS


def _sanitize_query(query: Dict[str, str]) -> urllib.parse.ParseResult:
    """Encode query parameters safely."""
    return urllib.parse.urlencode(
        {k: v for k, v in query.items() if isinstance(k, str) and isinstance(v, str)},
        doseq=True,
    )


def construct_api_redirect(
    base_api_url: str, api_endpoint: str, query_options: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g., "/users/123").
    query_options : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        A fully constructed, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not approved or the endpoint is disallowed.
    """
    # Parse and validate base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url!r}")

    if not _is_allowed_domain(parsed_base.netloc):
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved.")

    # Ensure endpoint starts with a slash and does not contain '..'
    if ".." in api_endpoint:
        raise ValueError("Endpoint contains disallowed path traversal sequence '..'.")

    # Join base and endpoint safely
    joined_url = urllib.parse.urljoin(parsed_base.geturl(), api_endpoint)

    # Parse the combined URL to inspect path
    parsed_combined = urllib.parse.urlparse(joined_url)
    if not _is_allowed_endpoint(parsed_combined.path):
        raise ValueError(f"Endpoint '{parsed_combined.path}' is not allowed.")

    # Encode query parameters if provided
    query_string = ""
    if query_options:
        query_string = _sanitize_query(query_options)

    # Rebuild the final URL with sanitized query string
    final_url = urllib.parse.urlunparse(
        (
            parsed_combined.scheme,
            parsed_combined.netloc,
            parsed_combined.path,
            parsed_combined.params,
            query_string,
            parsed_combined.fragment,
        )
    )

    return final_url