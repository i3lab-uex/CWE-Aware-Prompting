import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------
# Configuration: trusted domains and endpoints.
# --------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}


def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the URL's netloc is one of the approved domains.
    """
    domain = parsed_url.netloc.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")


def _validate_endpoint(endpoint: str) -> None:
    """
    Ensure the endpoint is in the list of allowed endpoints.
    The comparison is case‑sensitive and assumes a leading slash.
    """
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed API endpoint: {endpoint}")


def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The endpoint to call (e.g., "/v1/users").
    optional_params : dict, optional
        Query string parameters to include.

    Returns
    -------
    str
        The fully qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the base URL's domain is not approved or if the endpoint is disallowed.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL: missing scheme or netloc")

    _validate_domain(parsed_base)

    # Validate the endpoint
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")
    _validate_endpoint(desired_endpoint)

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path or "/", desired_endpoint)

    # Encode query parameters if provided
    query = ""
    if optional_params:
        # Ensure all keys and values are strings; otherwise, convert them
        encoded_params = {
            str(k): str(v) for k, v in optional_params.items()
        }
        query = urllib.parse.urlencode(encoded_params)

    # Assemble the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params (deprecated)
            query,       # query
            "",          # fragment
        )
    )

    return final_url