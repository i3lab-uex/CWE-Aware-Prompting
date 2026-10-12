import urllib.parse
from typing import Dict, Optional

# Pre‑approved domains and endpoints – adjust as needed for your environment
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/status",
]

def construct_api_redirect(
    base_api_url: str,
    api_endpoint: str,
    query_options: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully qualified redirect URL for an API call.

    Parameters
    ----------
    base_api_url : str
        Base address of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path (must start with a leading slash).
    query_options : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Parse and validate base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base API URL")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' not in approved list")

    # Ensure the endpoint is allowed
    if not api_endpoint.startswith("/"):
        raise ValueError("API endpoint must start with '/'")
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # Construct the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))

    # Encode query parameters safely
    if query_options:
        # Filter out None values and convert all to strings
        safe_params = {
            str(k): str(v) for k, v in query_options.items() if v is not None
        }
        query_string = urllib.parse.urlencode(safe_params, doseq=True)
    else:
        query_string = ""

    # Rebuild the final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",  # params
        query_string,
        ""   # fragment
    ))

    return final_url

# Example usage:
if __name__ == "__main__":
    url = construct_api_redirect(
        "https://api.example.com",
        "/v1/users",
        {"page": 2, "sort": "asc"}
    )
    print(url)   # https://api.example.com/v1/users?page=2&sort=asc