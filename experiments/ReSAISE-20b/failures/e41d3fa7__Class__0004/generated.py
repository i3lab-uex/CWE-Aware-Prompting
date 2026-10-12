import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Trusted configuration
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "v1.api.trustedservice.net",
}

ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/inventory",
    "/auth/login",
}

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API endpoint (e.g., "/users").
    query_info : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The complete URL ready for redirection.

    Raises
    ------
    ValueError
        If the target domain or endpoint is not approved.
    """
    # Validate and normalize base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_url must be a valid absolute URL")

    # Ensure domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Ensure endpoint is allowed
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path or "/", endpoint_path)

    # Encode query parameters
    query_string = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        query_string = urllib.parse.urlencode(query_info, doseq=True)

    # Reconstruct the full URL
    constructed_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            query_string,  # query
            "",          # fragment
        )
    )

    return constructed_url


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         url = generate_redirect_link(
#             "https://api.example.com",
#             "/users",
#             {"page": "2", "limit": "50"},
#         )
#         print(url)
#     except ValueError as e:
#         print(f"Error: {e}")