import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – only approved domains and endpoints are allowed.
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.test.org",
}

ALLOWED_ENDPOINTS = [
    "/users",
    "/orders",
    "/products",
    "/status",
]

# ------------------------------------------------------------------
# Helper: Normalise and validate the base URL
# ------------------------------------------------------------------
def _validate_and_normalise_base(base_url: str) -> urllib.parse.ParseResult:
    """
    Parse the base URL and ensure it contains a host that is approved.
    Returns a parsed result suitable for further manipulation.
    Raises ValueError if the domain is not approved.
    """
    parsed = urllib.parse.urlparse(base_url)

    # Basic sanity checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Base URL must be a full URL: {base_url!r}")

    # Reject URLs that point to unapproved domains
    host = parsed.hostname.lower()
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {host!r}")

    # Ensure the path ends with a slash so that endpoints are appended correctly
    if not parsed.path.endswith("/"):
        path = parsed.path + "/"
    else:
        path = parsed.path

    # Return a new ParseResult with the corrected path
    return parsed._replace(path=path)


# ------------------------------------------------------------------
# Main function – create a safe redirect link
# ------------------------------------------------------------------
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URL by combining a base URL, an endpoint,
    and optional query parameters.

    Parameters
    ----------
    base_url : str
        The base API URL (must include scheme and host).
    path : str
        The endpoint to append. Must be one of ALLOWED_ENDPOINTS.
    params : dict[str, str], optional
        Query parameters to include in the URL.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the base domain is not approved or if the endpoint is disallowed.
    """
    # ------------------------------------------------------------------
    # 1. Validate base URL and normalise it
    # ------------------------------------------------------------------
    parsed_base = _validate_and_normalise_base(base_url)

    # ------------------------------------------------------------------
    # 2. Validate the endpoint
    # ------------------------------------------------------------------
    if not path.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {path!r}")
    if path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {path!r}")

    # ------------------------------------------------------------------
    # 3. Construct the full path
    # ------------------------------------------------------------------
    # Avoid double slashes: parsed_base.path already ends with '/'
    full_path = urllib.parse.urljoin(parsed_base.path, path.lstrip("/"))

    # ------------------------------------------------------------------
    # 4. Encode query parameters
    # ------------------------------------------------------------------
    if params:
        # Ensure all keys/values are strings; otherwise urlencode will fail
        encoded_params = urllib.parse.urlencode(
            {str(k): str(v) for k, v in params.items()}
        )
    else:
        encoded_params = ""

    # ------------------------------------------------------------------
    # 5. Assemble the final URL
    # ------------------------------------------------------------------
    final_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params component (deprecated)
        encoded_params,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url


# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = create_api_redirect_link(
            base_url="https://api.example.com/v1",
            path="/users",
            params={"page": "2", "limit": "50"}
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Invalid configuration: {exc}")