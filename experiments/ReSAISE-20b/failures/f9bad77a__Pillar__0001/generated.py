import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Trusted domains and allowed endpoints – these would normally be
# defined elsewhere in the application configuration.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
    "data.service.net"
}

ALLOWED_ENDPOINTS = {
    "users",
    "orders",
    "products",
    "search"
}

# ------------------------------------------------------------------
# Helper function to ensure a domain is approved.
# ------------------------------------------------------------------
def _is_approved_domain(domain: str) -> bool:
    return domain in APPROVED_API_DOMAINS

# ------------------------------------------------------------------
# Helper function to ensure an endpoint is allowed.
# ------------------------------------------------------------------
def _is_allowed_endpoint(endpoint: str) -> bool:
    return endpoint in ALLOWED_ENDPOINTS

# ------------------------------------------------------------------
# Main function to construct a redirect URL.
# ------------------------------------------------------------------
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a full API redirect URL from a base URL, endpoint and optional
    query parameters. Validates that the domain and endpoint are approved.

    Parameters
    ----------
    main_url : str
        Base API URL, e.g. "https://api.example.com".
    endpoint_name : str
        Endpoint path component, e.g. "users".
    params_dict : dict[str,str] | None
        Optional dictionary of query string parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL to extract its components
    parsed_main = urllib.parse.urlparse(main_url)

    # Validate domain
    if not _is_approved_domain(parsed_main.netloc):
        raise ValueError(f"Domain '{parsed_main.netloc}' is not approved.")

    # Validate endpoint
    if not _is_allowed_endpoint(endpoint_name):
        raise ValueError(f"Endpoint '{endpoint_name}' is not allowed.")

    # Build the path by normalising slashes
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = endpoint_name.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}"

    # Encode query parameters if provided
    query_string = ""
    if params_dict:
        # Ensure all values are strings to avoid encoding issues
        safe_params = {k: str(v) for k, v in params_dict.items()}
        query_string = urllib.parse.urlencode(safe_params)

    # Reconstruct the full URL
    final_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# ------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     url = construct_redirect_url(
#         "https://api.example.com",
#         "users",
#         {"id": 42, "active": "true"}
#     )
#     print(url)