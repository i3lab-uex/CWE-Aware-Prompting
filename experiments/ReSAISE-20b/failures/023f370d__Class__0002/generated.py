import urllib.parse
from typing import Dict, Optional

# Pre‑approved base API domains (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}

# Safe, allowable API endpoints (example values)
ALLOWED_ENDPOINTS = [
    "v1/users",
    "v2/orders",
    "status",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API request.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint to append to the base URL (e.g., "v1/users").
    query_options : dict, optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Normalize and validate domain
    base_domain = parsed_base.netloc.lower()
    if base_domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{base_domain}' is not approved")

    # Sanitize and validate endpoint
    # Strip leading/trailing slashes to avoid duplicate separators
    clean_endpoint = api_endpoint.strip("/")
    if clean_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{clean_endpoint}' is not allowed")

    # Construct the path
    # Ensure there's exactly one slash between base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    full_path = f"{base_path}/{clean_endpoint}"

    # Encode query parameters if provided
    query_string = ""
    if query_options:
        # Ensure all values are strings to avoid injection issues
        safe_query = {
            str(k): str(v) for k, v in query_options.items()
        }
        query_string = urllib.parse.urlencode(safe_query)

    # Rebuild the full URL
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    ))

    return redirect_url

# Example usage:
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/v1/users/",
        {"id": 42, "verbose": "true"}
    )
    print(url)  # https://api.example.com/v1/users?id=42&verbose=true