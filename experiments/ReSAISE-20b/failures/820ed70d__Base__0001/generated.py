import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – define the domains and endpoints that are allowed to be
# referenced by this function.  In a real deployment these would likely come
# from a secure configuration store.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure-api.company.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/analytics/report",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain part of a URL so that comparisons are reliable.
    Strips port numbers and lower‑cases the domain name.
    """
    if ":" in domain:
        host, _ = domain.split(":", 1)
    else:
        host = domain
    return host.lower()


def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return _normalize_domain(domain) in APPROVED_API_DOMAINS


def _is_allowed_endpoint(path: str) -> bool:
    """Check if the endpoint path is in the allowed list."""
    # Ensure leading slash for comparison
    if not path.startswith("/"):
        path = "/" + path
    return path in ALLOWED_ENDPOINTS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a fully‑qualified API URL from the base URL, endpoint path and
    optional query parameters.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API, e.g. "https://api.example.com".
    api_path : str
        The endpoint path, e.g. "/v1/users".
    query_dict : dict[str, str], optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The complete, validated URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or endpoint.
    """
    # Parse base URL and validate domain
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not _is_approved_domain(parsed_base.netloc):
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Normalise and validate endpoint
    api_path = urllib.parse.urljoin("/", api_path)  # ensure leading slash
    if not _is_allowed_endpoint(api_path):
        raise ValueError(f"Unapproved endpoint: {api_path}")

    # Construct the full path
    full_path = urllib.parse.urljoin(parsed_base.path + "/", api_path.lstrip("/"))

    # Merge query parameters
    base_query = urllib.parse.parse_qs(parsed_base.query)
    # parse_qs returns lists; flatten for simplicity
    base_query = {k: v[0] for k, v in base_query.items()}
    if query_dict:
        base_query.update(query_dict)

    # Build final URL
    assembled = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        urllib.parse.urlencode(base_query, doseq=True),
        ""   # fragment
    ))

    return assembled


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove if running as part of a larger app)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "limit": "25"}
        )
        print("Assembled URL:", url)
    except ValueError as exc:
        print("Validation error:", exc)