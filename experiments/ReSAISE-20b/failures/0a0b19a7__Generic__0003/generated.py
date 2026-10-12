import urllib.parse
from typing import Dict, Optional

# Example sets – replace with your actual approved domains and endpoints
APPROVED_API_DOMAINS = {"api.example.com", "secure.api.example.org"}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    # Add more allowed endpoints here
]


def build_api_redirect_url(
    api_base_url: str,
    endpoint: str,
    query_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for API responses.

    Parameters
    ----------
    api_base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    endpoint : str
        The specific API endpoint (e.g., "/v1/users").
    query_params : dict, optional
        A dictionary of query parameters to append to the URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL does not point to an approved domain or endpoint.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {api_base_url}")

    # Normalize the endpoint to start with a slash
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    # Ensure the endpoint is allowed
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint}' is not allowed")

    # Build the full path by joining base path and endpoint
    # Avoid double slashes while preserving any existing base path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint)

    # Assemble the URL components
    url_components = parsed_base._replace(path=full_path)

    # Append query parameters if provided
    if query_params:
        # Use urlencode to handle proper escaping
        encoded_qs = urllib.parse.urlencode(query_params, doseq=True)
        url_components = url_components._replace(query=encoded_qs)

    # Construct the final URL
    redirect_url = urllib.parse.urlunparse(url_components)

    # Validate domain against approved list
    netloc = url_components.netloc.split(":")[0]  # ignore port if present
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not approved")

    return redirect_url