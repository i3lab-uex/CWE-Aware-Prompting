import urllib.parse
from typing import Dict, Optional

# Pre‑approved base API domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.internal.company",
}

# Safe, allowable API endpoints (example values)
ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]


def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        The base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint path to append (e.g., "/users").
    query_options : dict, optional
        Query parameters as a dictionary.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is not allowed.
    """
    # Parse the base URL to extract scheme and network location
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("base_api_url must be a valid absolute URL")

    # Validate domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize and validate endpoint
    if not api_endpoint.startswith("/"):
        raise ValueError("api_endpoint must start with '/'")
    # Prevent path traversal
    if ".." in api_endpoint.split("/"):
        raise ValueError("api_endpoint contains forbidden path traversal components")
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Build the full path
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = api_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}".replace("//", "/")

    # Encode query parameters
    query_string = ""
    if query_options:
        # Ensure all values are strings and non-empty
        cleaned_query = {
            k: str(v)
            for k, v in query_options.items()
            if isinstance(k, str) and isinstance(v, (str, int, float))
        }
        query_string = urllib.parse.urlencode(cleaned_query)

    # Assemble the final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return redirect_url


# Example usage:
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/users",
        {"page": 2, "limit": 50},
    )
    print(url)   # https://api.example.com/users?page=2&limit=50