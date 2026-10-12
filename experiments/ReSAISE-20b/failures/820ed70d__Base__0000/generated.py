import urllib.parse
from typing import Dict, Optional

# Allowed domains and endpoints for security
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a secure API redirect URL.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API, e.g. "https://api.example.com".
    api_path : str
        Path to the specific endpoint, e.g. "/v1/users".
    query_dict : dict, optional
        Dictionary of query parameters to be added to the URL.

    Returns
    -------
    str
        The fully assembled API URL.

    Raises
    ------
    ValueError
        If the domain is not in APPROVED_API_DOMAINS or if api_path is not
        an allowed endpoint.
    """
    # Parse the base URL to validate scheme and netloc
    parsed_base = urllib.parse.urlparse(base_api_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure the domain is approved
    if parsed_base.netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Validate the endpoint
    if api_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_path}' is not allowed")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Merge query parameters
    existing_query = urllib.parse.parse_qs(parsed_base.query)
    if query_dict:
        # Convert to list format expected by urlencode
        for key, value in query_dict.items():
            existing_query[key] = [value]
    final_query = urllib.parse.urlencode(existing_query, doseq=True)

    # Rebuild the URL
    assembled = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        final_query,
        ""   # fragment
    ))

    return assembled


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": "123", "verbose": "true"}
#     )
#     print(url)