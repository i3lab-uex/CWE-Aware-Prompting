import urllib.parse
from typing import Dict, Optional

# Example sets – replace with the actual values used in your application
APPROVED_API_DOMAINS = {"api.example.com", "api.secure.org"}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v1/products",
    # add other allowed endpoints here
}


def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully qualified redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The base URL of the API (e.g., "https://api.example.com").
    desired_endpoint : str
        The specific API endpoint (e.g., "/v1/users").
    optional_params : dict, optional
        A dictionary of query parameters to append.

    Returns
    -------
    str
        The complete, validated redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not in APPROVED_API_DOMAINS or the endpoint is not allowed.
    """
    # ---- Validate base URL and domain ----
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL: missing scheme or netloc")

    # Normalize the domain (strip port if present)
    domain = parsed_base.hostname
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")

    # ---- Validate endpoint ----
    # Ensure the endpoint starts with a slash for consistency
    normalized_endpoint = desired_endpoint if desired_endpoint.startswith("/") else f"/{desired_endpoint}"
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {normalized_endpoint}")

    # ---- Build the full path ----
    base_path = parsed_base.path.rstrip("/")
    full_path = urllib.parse.urljoin(base_path + "/", normalized_endpoint.lstrip("/"))

    # ---- Append query parameters if provided ----
    query = urllib.parse.urlencode(optional_params) if optional_params else ""

    # ---- Construct the final URL ----
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return redirect_url