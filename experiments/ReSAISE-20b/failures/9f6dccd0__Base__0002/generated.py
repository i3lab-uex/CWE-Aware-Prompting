import urllib.parse
from pathlib import Path

# Pre‑approved base domains and allowed endpoints
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.foo.org",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/status",
]

def _is_valid_domain(netloc: str) -> bool:
    """
    Check that the network location (host[:port]) is in the approved set.
    Ports are ignored for validation purposes.
    """
    host = netloc.split(":")[0].lower()
    return host in APPROVED_API_DOMAINS

def _is_allowed_endpoint(path: str) -> bool:
    """
    Ensure the endpoint path matches one of the allowed endpoints.
    The comparison is case‑sensitive and requires an exact match.
    """
    return path in ALLOWED_ENDPOINTS

def _normalize_path(api_path: str) -> str:
    """
    Normalise the API path to avoid traversal or malformed URLs.
    Reject paths that attempt directory traversal (contain '..') or
    are absolute but not matching an allowed endpoint.
    """
    # Resolve leading slashes and eliminate multiple slashes
    path = str(Path(api_path).resolve())
    # Path.resolve will turn the string into an absolute filesystem path;
    # we just need to ensure it starts with a slash and does not contain '..'.
    if ".." in Path(api_path).parts:
        raise ValueError("Endpoint path contains prohibited traversal components")
    # Ensure it starts with a single slash
    if not path.startswith("/"):
        path = "/" + path.lstrip("/")
    return path

def generate_api_redirect(base_url: str, api_path: str, params: dict | None = None) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        Base address of the API (e.g. 'https://api.example.com')
    api_path : str
        Endpoint path (e.g. '/v1/users')
    params : dict, optional
        Dictionary of query parameters

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Parse and validate base URL
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    if not _is_valid_domain(parsed_base.netloc):
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Normalise and validate API path
    normalized_path = _normalize_path(api_path)
    if not _is_allowed_endpoint(normalized_path):
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Build the final URL
    path = urllib.parse.urljoin(parsed_base.path + "/", normalized_path.lstrip("/"))
    query = urllib.parse.urlencode(params or {}, doseq=True)

    redirect_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        path,
        "",          # params
        query,
        ""           # fragment
    ))
    return redirect_url