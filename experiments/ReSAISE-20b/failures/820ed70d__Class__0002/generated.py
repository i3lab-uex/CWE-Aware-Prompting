import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – keep these lists/sets small and strictly controlled
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ------------------------------------------------------------------
# Utility
# ------------------------------------------------------------------
def _validate_domain(netloc: str) -> None:
    """
    Ensure the domain part of a URL is in the approved list.
    Raises ValueError if not approved.
    """
    # Strip port if present
    domain = netloc.split(":")[0].lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")


def _validate_endpoint(path: str) -> None:
    """
    Ensure the endpoint path is in the allowed list.
    Raises ValueError if not approved.
    """
    # Normalize to start with a single slash
    normalized = "/" + path.lstrip("/")
    if normalized not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {normalized}")


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a full API redirect URL from a base URL, endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g., "https://api.example.com")
    api_path : str
        Target endpoint path (e.g., "/v1/users")
    query_dict : dict, optional
        Dictionary of key/value pairs to be added as query string

    Returns
    -------
    str
        The fully constructed, validated URL.

    Raises
    ------
    ValueError
        If the resulting domain or endpoint is not approved.
    """
    # Parse base URL to validate domain
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base API URL must be a valid absolute URL")

    _validate_domain(parsed_base.netloc)

    # Normalize and validate endpoint
    normalized_endpoint = "/" + api_path.lstrip("/")
    _validate_endpoint(normalized_endpoint)

    # Build the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))
    # Construct the final URL components
    url_parts = parsed_base._replace(path=joined_path)

    # Append query parameters if provided
    if query_dict:
        query_string = urllib.parse.urlencode(query_dict, doseq=True)
        url_parts = url_parts._replace(query=query_string)

    final_url = urllib.parse.urlunparse(url_parts)
    return final_url


# ------------------------------------------------------------------
# Example usage (commented out – for demonstration only)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": "2", "sort": "name"}
#     )
#     print(url)  # https://api.example.com/v1/users?page=2&sort=name