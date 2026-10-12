import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: approved domains and endpoints.  These should be kept up‑to‑date
# and never derived from user input to avoid CWE‑610.  The set/list can be
# replaced with a more sophisticated policy store if needed.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# --------------------------------------------------------------------------- #
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URL.

    Parameters
    ----------
    base_url : str
        Base API host, e.g. "https://api.example.com".
    path : str
        Endpoint path, e.g. "/v1/users".  Must start with a slash.
    params : dict[str, str] | None
        Optional query parameters.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the host is not in APPROVED_API_DOMAINS or if the path is not in
        ALLOWED_ENDPOINTS.
    """
    # ---- Validate base_url ----------------------------------------------- #
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Strip any path or query from the base to avoid injection
    cleaned_base = f"{parsed_base.scheme}://{parsed_base.netloc}"

    # Verify domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname!r}")

    # ---- Validate endpoint path ------------------------------------------ #
    if not path.startswith("/"):
        raise ValueError(f"Endpoint must start with '/': {path!r}")

    # Normalise path (remove trailing slash, collapse duplicates)
    normalized_path = urllib.parse.urljoin("/", path)

    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {normalized_path!r}")

    # ---- Assemble final URL ---------------------------------------------- #
    url = urllib.parse.urljoin(cleaned_base + "/", normalized_path.lstrip("/"))

    # Add query parameters safely
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}?{query_string}"

    return url