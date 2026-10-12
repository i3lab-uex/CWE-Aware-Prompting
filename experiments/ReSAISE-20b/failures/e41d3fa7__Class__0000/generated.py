import urllib.parse
from typing import Dict, Optional

# Trusted domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.service.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/items",
    "/v2/data",
}


def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full redirect URL for API requests.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint (e.g., "/v1/users").
    query_info : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully qualified URL ready for redirect.

    Raises
    ------
    ValueError
        If the resulting domain is not in APPROVED_API_DOMAINS or
        if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    # Ensure base_url is absolute and parse it
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Clean and validate endpoint
    clean_endpoint = urllib.parse.quote(endpoint_path.strip())
    if not clean_endpoint.startswith("/"):
        clean_endpoint = "/" + clean_endpoint
    if clean_endpoint.lower() not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {clean_endpoint}")

    # Build path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", clean_endpoint.lstrip("/"))

    # Encode query parameters
    if query_info:
        encoded_query = urllib.parse.urlencode(query_info, doseq=True)
    else:
        encoded_query = ""

    # Assemble final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# Example usage (commented out)
# if __name__ == "__main__":
#     url = generate_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": "123", "format": "json"}
#     )
#     print(url)