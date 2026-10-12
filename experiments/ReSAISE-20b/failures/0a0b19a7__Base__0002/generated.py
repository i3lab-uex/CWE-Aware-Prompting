import urllib.parse
from typing import Dict, Optional

# Example approved domains and allowed endpoints. Replace with real values.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.otherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/posts",
    "/v2/status",
]

def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    api_base_url : str
        Base URL of the target API (e.g., "https://api.example.com").
    endpoint : str
        Specific API endpoint, must start with a leading slash.
    query_params : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully-qualified URL to redirect to.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # Normalize the base URL
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid api_base_url: must include scheme and netloc")

    # Ensure the domain is approved
    if parsed_base.netloc.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalize and validate the endpoint
    if not endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")
    # Endpoint comparison is case-sensitive; adjust if needed
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the full path
    # Remove any trailing slash from base to avoid double slashes
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", endpoint.lstrip("/"))

    # Construct query string
    query_string = ""
    if query_params:
        # Ensure all keys and values are strings
        sanitized_params = {str(k): str(v) for k, v in query_params.items()}
        query_string = urllib.parse.urlencode(sanitized_params)

    # Assemble the final URL
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

# Example usage:
if __name__ == "__main__":
    try:
        url = build_api_redirect_url(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "detail": "full"}
        )
        print(url)
    except ValueError as e:
        print(f"Invalid redirect: {e}")