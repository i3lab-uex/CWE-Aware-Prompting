import urllib.parse
from typing import Dict, Optional

# Trusted API domains and allowed endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.example.org",
}
ALLOWED_ENDPOINTS = {
    "users",
    "orders",
    "products",
    "search",
}

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_name : str
        The desired API endpoint (e.g., "users").
    params_dict : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resolved domain is not in APPROVED_API_DOMAINS or if
        endpoint_name is not in ALLOWED_ENDPOINTS.
    """
    # Parse the base URL to extract scheme and netloc
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("main_url must be a valid absolute URL")

    # Validate domain
    if parsed_main.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_main.netloc}' is not approved")

    # Validate endpoint
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_name}' is not allowed")

    # Ensure the endpoint is a single path component
    if "/" in endpoint_name or "\\" in endpoint_name:
        raise ValueError("endpoint_name must not contain path separators")

    # Build the full path
    endpoint_path = urllib.parse.urljoin(parsed_main.path + "/", endpoint_name)

    # Construct the final URL without query
    base_url = urllib.parse.urlunparse(
        (
            parsed_main.scheme,
            parsed_main.netloc,
            endpoint_path,
            "",  # params
            "",  # query (empty for now)
            "",  # fragment
        )
    )

    # Add query parameters if provided
    if params_dict:
        encoded_query = urllib.parse.urlencode(params_dict, doseq=True)
        full_url = f"{base_url}?{encoded_query}"
    else:
        full_url = base_url

    return full_url