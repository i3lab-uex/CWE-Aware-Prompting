import urllib.parse
from typing import Dict, Optional

# Domains and endpoints that are considered safe to call.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API URL from the base URI, endpoint and optional query parameters.
    
    Parameters
    ----------
    base_uri : str
        Base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        Endpoint path to append (e.g. "/v1/users").
    query : dict, optional
        Mapping of query parameter names to values.
    
    Returns
    -------
    str
        Fully qualified URL ready for use in an HTTP request.
    
    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Normalise base_uri to ensure it contains scheme and no trailing slash
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme:
        raise ValueError(f"Base URI must include scheme (http:// or https://): {base_uri}")
    base_netloc = parsed_base.netloc.lower()
    
    if base_netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {base_netloc}")

    # Ensure the endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {api_endpoint}")

    # Check that the endpoint is allowed
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {api_endpoint}")

    # Join the base path with the endpoint
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Build the final URL components
    url_components = parsed_base._replace(path=full_path)

    # Append query parameters if provided
    if query:
        # Ensure all values are strings; convert None to empty string
        safe_query = {k: str(v) if v is not None else "" for k, v in query.items()}
        encoded_query = urllib.parse.urlencode(safe_query)
        url_components = url_components._replace(query=encoded_query)

    final_url = urllib.parse.urlunparse(url_components)
    return final_url