import urllib.parse
from typing import Dict, Optional

# Example approved domains and endpoints – replace with real values as needed
APPROVED_API_DOMAINS = {"api.example.com", "services.example.org"}
ALLOWED_ENDPOINTS = [
    "/users",
    "/posts",
    "/comments",
    "/products",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        Base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        Specific API endpoint to call (e.g. "/users").
    query_params : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        Fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Parse the base URL and validate its scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure the domain is approved
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Normalize and validate the endpoint
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"
    # Avoid directory traversal or relative paths
    if ".." in endpoint.split("/"):
        raise ValueError("Endpoint contains disallowed path traversal components")

    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint.lstrip("/"))

    # Append query parameters if provided
    query_string = ""
    if query_params:
        # Encode only string values; raise error otherwise
        for k, v in query_params.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("Query parameters must be string key/value pairs")
        query_string = urllib.parse.urlencode(query_params)

    # Reconstruct the full URL
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
    url = build_api_redirect_url(
        "https://api.example.com",
        "/users",
        {"page": "2", "limit": "50"},
    )
    print(url)  # https://api.example.com/users?page=2&limit=50