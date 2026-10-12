import urllib.parse
from typing import Dict, Optional

# Set of domains that are considered safe and approved for API calls
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.example.org",
}

# List of allowed endpoint paths (must start with a leading slash)
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/data",
    "/healthcheck",
]

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully qualified API URL by merging the base URI with an endpoint
    and optional query parameters, while ensuring that the resulting URL points
    to an approved domain and endpoint.

    Parameters:
        base_uri (str): The base URL of the API, e.g. "https://api.example.com".
        api_endpoint (str): The endpoint path to append, e.g. "/v1/users".
        query (dict, optional): Dictionary of query parameters.

    Returns:
        str: The fully constructed URL.

    Raises:
        ValueError: If the resulting URL points to an unapproved domain or
                    if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    # Parse base URI to validate its components
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_uri must be a valid absolute URL")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize and validate the endpoint
    normalized_endpoint = urllib.parse.urljoin("/", api_endpoint)
    if not any(normalized_endpoint.startswith(e) for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Build the path by joining base path with endpoint
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Construct the final URL components
    url_parts = list(parsed_base)
    url_parts[2] = combined_path  # path
    url_parts[3] = ""             # params (unused)
    if query:
        # Ensure all values are strings and encode safely
        encoded_query = urllib.parse.urlencode(
            {k: str(v) for k, v in query.items()}
        )
    else:
        encoded_query = ""
    url_parts[4] = encoded_query  # query
    url_parts[5] = ""             # fragment

    final_url = urllib.parse.urlunparse(url_parts)

    return final_url