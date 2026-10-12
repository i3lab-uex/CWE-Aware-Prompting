import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – replace these with the real values for your project
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
    # add other approved domains here
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/data",
    # add other safe endpoints here
]

# ----------------------------------------------------------------------
def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure redirect URL for an API call.

    Parameters
    ----------
    base_url_api : str
        The base URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The specific endpoint to hit (e.g. "/v1/users").
    opts : dict[str, str] | None
        Optional query parameters to include in the URL.

    Returns
    -------
    str
        The fully formed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # 1. Parse the base URL and verify domain
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url_api}")

    domain = parsed_base.hostname
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not an approved API domain")

    # 2. Validate endpoint
    # Normalise the endpoint to ensure it starts with a slash
    normalized_endpoint = api_endpoint if api_endpoint.startswith("/") else f"/{api_endpoint}"
    if normalized_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed")

    # 3. Build the full path
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = normalized_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}".replace("//", "/")

    # 4. Assemble the URL
    url_parts = list(parsed_base)
    url_parts[2] = full_path  # path
    if opts:
        query_string = urllib.parse.urlencode(opts, doseq=True)
        url_parts[4] = query_string  # query
    else:
        url_parts[4] = ""

    redirect_url = urllib.parse.urlunparse(url_parts)

    # 5. Final safety check: ensure the URL still uses an approved domain
    final_parsed = urllib.parse.urlparse(redirect_url)
    if final_parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError("Resulting URL domain is not approved")

    return redirect_url