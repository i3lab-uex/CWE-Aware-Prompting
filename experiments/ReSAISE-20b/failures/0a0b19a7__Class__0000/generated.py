import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints.  In a real system these would
# be imported from configuration or constants modules.
APPROVED_API_DOMAINS = {"api.example.com", "services.mydomain.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/search",
]


def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        The specific endpoint to append (e.g. "/users").
    query_params : dict, optional
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully qualified URL ready for redirecting the client.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain or endpoint that is not approved.
    """
    # Normalize and parse the base URL
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("api_base_url must be a valid absolute URL")

    # Ensure the endpoint is relative and does not start with scheme or domain
    if urllib.parse.urlparse(endpoint).scheme:
        raise ValueError("endpoint must be a relative path")

    # Clean endpoint: ensure it starts with a single slash and remove any
    # leading slashes beyond the first to avoid double slashes when joining.
    cleaned_endpoint = endpoint.lstrip("/")
    if not cleaned_endpoint:
        raise ValueError("endpoint cannot be empty")
    cleaned_endpoint = "/" + cleaned_endpoint

    # Validate the endpoint against the whitelist
    if cleaned_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{cleaned_endpoint}' is not allowed")

    # Build the path by combining base and endpoint
    full_path = urllib.parse.urljoin(parsed_base.path + "/", cleaned_endpoint.lstrip("/"))

    # Assemble the final URL components
    url_parts = parsed_base._replace(path=full_path)

    # Add query parameters if provided
    if query_params:
        # Ensure all values are strings to avoid unexpected encoding issues
        safe_query = {k: str(v) for k, v in query_params.items()}
        url_parts = url_parts._replace(query=urllib.parse.urlencode(safe_query))

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate that the domain is approved
    if url_parts.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{url_parts.netloc}' is not approved")

    return final_url