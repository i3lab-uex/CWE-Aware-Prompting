import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration: allowed domains and endpoints
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/analytics",
]

# ----------------------------------------------------------------------
# Helper: validate domain and endpoint
# ----------------------------------------------------------------------
def _validate_domain_and_endpoint(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the URL's domain and path are within the approved lists.
    Raises ValueError if validation fails.
    """
    # Normalize netloc: strip port if present
    domain = parsed_url.netloc.split(":")[0].lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # Ensure the path starts with an allowed endpoint
    # Strip leading/trailing slashes for comparison
    path = parsed_url.path.rstrip("/")
    if not any(path == ep or path.startswith(ep + "/") for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{path}' is not allowed")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URI by merging the base URI with an
    endpoint and optional query parameters.

    Parameters:
        base_uri (str): The base API URL.
        api_endpoint (str): Target endpoint path (must be in ALLOWED_ENDPOINTS).
        query (dict, optional): Key-value pairs for query parameters.

    Returns:
        str: The fully assembled, validated URL.

    Raises:
        ValueError: If the domain or endpoint is not approved.
    """
    if not isinstance(base_uri, str) or not isinstance(api_endpoint, str):
        raise TypeError("base_uri and api_endpoint must be strings")

    # Parse base URI to validate domain
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URI")

    # Build the full path
    # Ensure exactly one slash between base and endpoint
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Merge components
    new_parsed = parsed_base._replace(path=combined_path)

    # Validate domain and endpoint
    _validate_domain_and_endpoint(new_parsed)

    # Add query parameters if provided
    if query:
        if not isinstance(query, dict):
            raise TypeError("query must be a dictionary")
        # Encode query parameters
        new_query = urllib.parse.urlencode(query, doseq=True)
        new_parsed = new_parsed._replace(query=new_query)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(new_parsed)

    return final_url

# ----------------------------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     url = generate_api_redirect_uri(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": "123", "active": "true"}
#     )
#     print(url)