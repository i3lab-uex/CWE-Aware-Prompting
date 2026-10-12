import urllib.parse
from typing import Dict, Optional

# Example approved domains and allowed endpoints.
# In a real application these would be defined elsewhere or loaded from config.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
}

ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}


def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a full redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g., "https://api.example.com").
    endpoint_path : str
        The desired API endpoint path (e.g., "/users").
    query_info : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The complete redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is not allowed.
    """
    # Parse the base URL to extract components
    parsed_base = urllib.parse.urlparse(base_url)

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved.")

    # Validate endpoint path
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed.")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # Encode query parameters if provided
    query_string = ""
    if query_info:
        # Ensure all values are strings to avoid unexpected types in URL
        safe_query = {str(k): str(v) for k, v in query_info.items()}
        query_string = urllib.parse.urlencode(safe_query)

    # Reassemble the URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            ""   # fragment
        )
    )

    return redirect_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = generate_redirect_link(
#         base_url="https://api.example.com",
#         endpoint_path="/users",
#         query_info={"id": "123", "verbose": "true"}
#     )
#     print(url)