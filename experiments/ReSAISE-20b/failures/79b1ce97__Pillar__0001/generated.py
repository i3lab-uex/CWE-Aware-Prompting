import re
from urllib.parse import urlparse, urljoin, urlencode

# Example definitions – in real code these would be imported or defined elsewhere
APPROVED_API_DOMAINS = {"api.example.com", "secure.api.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/status",
}

def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: dict | None = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g. "https://api.example.com").
    desired_endpoint : str
        The specific endpoint to call (e.g. "/v1/users").
    optional_params : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully formed URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the base URL's domain is not in ``APPROVED_API_DOMAINS`` or
        if the endpoint is not listed in ``ALLOWED_ENDPOINTS``.
    """
    # Validate domain
    parsed_base = urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api!r}")

    # Normalize domain comparison (ignore port)
    netloc = parsed_base.hostname
    if netloc not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain {netloc!r} not in approved list: {sorted(APPROVED_API_DOMAINS)}"
        )

    # Validate endpoint
    if not desired_endpoint.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {desired_endpoint!r}")

    # Reject path traversal attempts
    if re.search(r"\.\./", desired_endpoint):
        raise ValueError("Endpoint contains forbidden path traversal patterns")

    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint {desired_endpoint!r} not in allowed list: {sorted(ALLOWED_ENDPOINTS)}"
        )

    # Build the full path
    base_with_path = urljoin(base_url_api.rstrip("/") + "/", desired_endpoint.lstrip("/"))
    # Append query string if provided
    if optional_params:
        if not isinstance(optional_params, dict):
            raise ValueError("optional_params must be a dictionary")
        query_string = urlencode(optional_params, doseq=True)
        full_url = f"{base_with_path}?{query_string}"
    else:
        full_url = base_with_path

    return full_url