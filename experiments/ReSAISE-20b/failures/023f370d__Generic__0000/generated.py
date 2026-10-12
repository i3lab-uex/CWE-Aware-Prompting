import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/search",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_api_url : str
        The base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint to call (e.g. "/users").
    query_options : dict, optional
        Query parameters to include.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base API URL: {base_api_url}")

    # Validate domain
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalise and validate endpoint
    endpoint = api_endpoint.strip()
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    if endpoint.lower() not in (e.lower() for e in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the path
    path = urllib.parse.urljoin(parsed_base.path + "/", endpoint.lstrip("/"))

    # Encode query parameters
    query = ""
    if query_options:
        # Ensure all values are strings and encode properly
        encoded_params = urllib.parse.urlencode(
            {str(k): str(v) for k, v in query_options.items()}
        )
        query = encoded_params

    # Reconstruct the full URL
    constructed_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return constructed_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = construct_api_redirect(
#         "https://api.example.com",
#         "/users",
#         {"page": "2", "sort": "asc"},
#     )
#     print(url)