import urllib.parse
from typing import Dict, Optional

# Example allowed domains and endpoints – replace with real values in production
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/health",
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
        The base URL of the API (e.g. "https://api.example.com").
    endpoint : str
        The specific endpoint to call (e.g. "/v1/users").
    query_params : dict, optional
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or the endpoint is disallowed.
    """
    # Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(api_base_url)
    if not parsed_base.scheme or parsed_base.scheme.lower() not in {"http", "https"}:
        raise ValueError("Base URL must use http or https scheme")

    base_domain = parsed_base.hostname
    if not base_domain or base_domain.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Unapproved API domain: {base_domain}")

    # Normalize endpoint
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    # Validate the endpoint against allowed list (case-sensitive)
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed API endpoint: {endpoint}")

    # Build the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", endpoint.lstrip("/"))

    # Construct the full URL
    url_parts = list(parsed_base)
    url_parts[2] = joined_path  # path
    if query_params:
        url_parts[4] = urllib.parse.urlencode(query_params, doseq=True)
    full_url = urllib.parse.urlunparse(url_parts)

    # Final safety check: ensure the resolved domain is still approved
    final_domain = urllib.parse.urlparse(full_url).hostname
    if final_domain.lower() not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError("Resulting URL points to an unapproved domain")

    return full_url