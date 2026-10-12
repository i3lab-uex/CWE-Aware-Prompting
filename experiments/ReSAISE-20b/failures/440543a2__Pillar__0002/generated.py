import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
#  Configuration – adjust these sets/lists to match your security policy
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    # add more approved domains here
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    # add more allowed endpoints here
]


# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.
    - Lower‑case
    - Strip leading 'www.'
    """
    return domain.lower().lstrip("www.")


def _is_approved_domain(netloc: str) -> bool:
    """
    Verify that the network location (domain + optional port) belongs to an
    approved domain.  The port is ignored for the approval check.
    """
    if not netloc:
        return False
    host, _, _ = netloc.partition(":")
    return _normalize_domain(host) in APPROVED_API_DOMAINS


def _is_allowed_endpoint(path: str) -> bool:
    """
    Ensure the endpoint path is exactly one of the allowed endpoints.
    The comparison is case‑sensitive and requires a leading slash.
    """
    return path in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe API redirect URL by joining a base URL with an
    approved endpoint and optional query parameters.

    Parameters
    ----------
    base_url : str
        The base API URL (e.g. "https://api.example.com").
    path : str
        The target endpoint (must start with '/').
    params : dict[str, str] | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The fully assembled URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    if not path.startswith("/"):
        raise ValueError("Endpoint path must start with '/'")

    # Resolve the full URL
    joined = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    parsed = urllib.parse.urlparse(joined)

    # Domain check
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Unapproved domain: {parsed.netloc}")

    # Endpoint check
    if not _is_allowed_endpoint(parsed.path):
        raise ValueError(f"Unapproved endpoint: {parsed.path}")

    # Append query parameters if provided
    if params:
        # Ensure all values are strings to avoid unexpected encoding behaviour
        safe_params = {str(k): str(v) for k, v in params.items()}
        query_string = urllib.parse.urlencode(safe_params)
        # Merge with any existing query string from the base URL
        final_query = urllib.parse.urljoin(
            f"?{parsed.query}", f"?{query_string}"
        )[1:]  # strip leading '?'
    else:
        final_query = parsed.query

    # Rebuild the URL
    rebuilt = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            final_query,
            parsed.fragment,
        )
    )

    return rebuilt