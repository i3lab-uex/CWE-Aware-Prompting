import urllib.parse
from typing import Dict, Optional

# Example approved domains and allowed endpoints. In real usage these should be defined elsewhere.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.another.com",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/data",
]


def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a secure API redirect URL.

    Parameters
    ----------
    base_api_url : str
        The base address of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path (e.g. "/v1/users").
    query_options : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        A fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the target domain is not in ``APPROVED_API_DOMAINS`` or if
        ``api_endpoint`` is not in ``ALLOWED_ENDPOINTS``.
    """
    # Ensure the endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        api_endpoint = "/" + api_endpoint

    # Validate endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed.")

    # Parse base URL to validate domain
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Base URL '{base_api_url}' is malformed.")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved.")

    # Construct the path
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", api_endpoint.lstrip("/"))

    # Build query string
    if query_options:
        # Ensure all keys/values are strings and percent-encode them
        encoded_params = urllib.parse.urlencode(
            {str(k): str(v) for k, v in query_options.items()}
        )
    else:
        encoded_params = ""

    # Assemble the final URL
    result_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            domain,
            full_path,
            "",  # params
            encoded_params,
            "",  # fragment
        )
    )

    return result_url


# Example usage:
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/v1/users",
        {"page": 2, "sort": "asc"},
    )
    print(url)  # https://api.example.com/v1/users?page=2&sort=asc