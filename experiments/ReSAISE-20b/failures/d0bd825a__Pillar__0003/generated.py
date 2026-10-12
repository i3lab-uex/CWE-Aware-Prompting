import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: pre‑approved API domains and safe endpoints
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.foo.org",
    "data.bar.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/public/info",
]

# --------------------------------------------------------------------------- #
# Utility: normalize and validate the base URL
# --------------------------------------------------------------------------- #

def _validate_and_normalize_base(base_url: str) -> urllib.parse.ParseResult:
    """
    Parse the supplied base URL and ensure it points to an approved domain.
    Returns a ParseResult that can be used with urljoin().
    """
    parsed = urllib.parse.urlparse(base_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid base URL: '{base_url}'")

    # Strip port for domain comparison
    host = parsed.hostname.lower()
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for API redirects")

    # Ensure the base URL ends with a slash so that urljoin behaves correctly
    if not parsed.path.endswith("/"):
        base = urllib.parse.urlunparse(parsed._replace(path=parsed.path + "/"))
    else:
        base = urllib.parse.urlunparse(parsed)

    return urllib.parse.urlparse(base)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def create_api_redirect_url(
    base_url_api: str,
    api_endpoint: str,
    opts: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully qualified API redirect URL.

    Parameters
    ----------
    base_url_api : str
        The root address of the API (e.g. 'https://api.example.com').
    api_endpoint : str
        The specific endpoint to call (e.g. '/v1/users').
    opts : dict, optional
        Query parameters to append to the URL.

    Returns
    -------
    str
        A safe, fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # 1. Validate base URL domain
    normalized_base = _validate_and_normalize_base(base_url_api)

    # 2. Validate endpoint
    if not any(api_endpoint == ep or api_endpoint.startswith(ep + "/") for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Endpoint '{api_endpoint}' is not allowed")

    # 3. Build the full path
    full_path = urllib.parse.urljoin(normalized_base.geturl(), api_endpoint.lstrip("/"))

    # 4. Append query parameters if provided
    if opts:
        # Ensure all values are strings to avoid unexpected encoding issues
        encoded_opts = urllib.parse.urlencode(
            {k: str(v) for k, v in opts.items()}
        )
        full_path = f"{full_path}?{encoded_opts}"

    return full_path