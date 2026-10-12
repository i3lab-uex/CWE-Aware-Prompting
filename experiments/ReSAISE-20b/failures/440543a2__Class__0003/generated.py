import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – set of approved domains and allowed endpoint paths
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.example.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_domain_approved(url: str) -> bool:
    """
    Check if the domain of the given URL is in APPROVED_API_DOMAINS.
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.hostname in APPROVED_API_DOMAINS


def _is_endpoint_allowed(path: str) -> bool:
    """
    Check if the endpoint path is in ALLOWED_ENDPOINTS.
    The check is strict: it must match exactly an entry in the list.
    """
    # Normalize path to start with a single leading slash
    norm_path = "/" + path.lstrip("/")
    return norm_path in ALLOWED_ENDPOINTS


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a full API URL by combining the base URL, endpoint path,
    and optional query parameters. The function validates that the
    resulting URL belongs to an approved domain and uses a permitted
    endpoint.

    Parameters
    ----------
    base_url : str
        Base URL of the API (e.g., "https://api.example.com").
    path : str
        Endpoint path to append (e.g., "v1/users").
    params : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the domain is not approved or the endpoint is disallowed.
    """
    # Validate base URL domain
    if not _is_domain_approved(base_url):
        raise ValueError(f"Unapproved domain in base URL: {base_url}")

    # Validate endpoint
    if not _is_endpoint_allowed(path):
        raise ValueError(f"Disallowed endpoint path: {path}")

    # Parse base URL and build the new path
    parsed_base = urllib.parse.urlparse(base_url)
    # Ensure base URL ends with a slash to avoid accidental concatenation
    base_path = parsed_base.path.rstrip("/")
    # Combine paths safely
    combined_path = urllib.parse.urljoin(base_path + "/", path.lstrip("/"))

    # Encode query parameters if provided
    query = urllib.parse.urlencode(params) if params else ""

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            combined_path,
            "",  # params (unused)
            query,
            ""   # fragment
        )
    )

    return final_url


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         url = create_api_redirect_link(
#             "https://api.example.com",
#             "/v1/users",
#             {"id": "123", "active": "true"}
#         )
#         print(url)
#     except ValueError as e:
#         print(f"Error: {e}")