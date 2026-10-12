import urllib.parse
from typing import Dict, Optional

# Trusted API domains and allowed endpoints (example values)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/public/info",
]

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully qualified redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g., "https://api.example.com").
    endpoint_path : str
        The API endpoint path (e.g., "/v1/users").
    query_info : dict, optional
        Query string parameters to append.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in APPROVED_API_DOMAINS or
        if endpoint_path is not one of ALLOWED_ENDPOINTS.
    """
    # Normalise and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    domain = parsed_base.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not approved")

    # Validate endpoint
    if not endpoint_path.startswith("/"):
        endpoint_path = "/" + endpoint_path
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {endpoint_path!r} is not allowed")

    # Build the path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint_path.lstrip("/"))

    # Encode query parameters
    query_string = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        query_string = urllib.parse.urlencode(query_info, doseq=True)

    # Assemble the final URL
    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        domain,
        full_path,
        "",          # params
        query_string,
        ""           # fragment
    ))

    return redirect_url

# Example usage:
if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            base_url="https://api.example.com",
            endpoint_path="/v1/users",
            query_info={"id": "123", "active": "true"}
        )
        print(url)  # https://api.example.com/v1/users?id=123&active=true
    except ValueError as exc:
        print(f"URL generation failed: {exc}")