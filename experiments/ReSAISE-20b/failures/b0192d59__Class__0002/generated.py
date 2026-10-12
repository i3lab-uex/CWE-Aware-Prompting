import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – modify these sets/lists to suit your deployment environment
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    # add additional approved domains here
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/analytics/report",
    # add additional allowed endpoints here
]

# --------------------------------------------------------------------------- #
# Helper functions – keep them internal to avoid accidental misuse
# --------------------------------------------------------------------------- #

def _is_valid_domain(netloc: str) -> bool:
    """
    Verify that the hostname part of a URL is in the approved domain list.
    """
    # Remove port if present
    hostname = netloc.split(":")[0]
    return hostname in APPROVED_API_DOMAINS


def _is_valid_endpoint(path: str) -> bool:
    """
    Verify that the path is in the list of allowed endpoints.
    The check is strict: an exact match is required.
    """
    return path in ALLOWED_ENDPOINTS


def _canonicalize_path(path: str) -> str:
    """
    Normalise a URL path to prevent directory traversal or other
    manipulation. We reject any component that is '.' or '..'.
    """
    parts = [p for p in path.split("/") if p not in (".", "..")]
    return "/" + "/".join(parts)


# --------------------------------------------------------------------------- #
# Main public function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure API redirect URI by merging the base URL with an
    approved endpoint and optional query parameters.

    Parameters
    ----------
    base_uri : str
        The root API URL, e.g. "https://api.example.com".
    api_endpoint : str
        The target endpoint, e.g. "/v1/users".
    query : dict, optional
        Key/value pairs to be appended as URL‑encoded query string.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the resulting domain or endpoint is not approved.
    """
    if not isinstance(base_uri, str) or not isinstance(api_endpoint, str):
        raise TypeError("base_uri and api_endpoint must be strings")

    # Parse the base URL to extract scheme, netloc, path
    parsed_base = urllib.parse.urlparse(base_uri)
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError("base_uri must use http or https scheme")

    # Ensure the domain is approved
    if not _is_valid_domain(parsed_base.netloc):
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Canonicalise and validate the endpoint
    canonical_endpoint = _canonicalize_path(api_endpoint)
    if not _is_valid_endpoint(canonical_endpoint):
        raise ValueError(f"Unapproved endpoint: {canonical_endpoint}")

    # Merge base path with endpoint
    merged_path = urllib.parse.urljoin(parsed_base.path, canonical_endpoint)

    # Build query string if provided
    query_string = urllib.parse.urlencode(query or {}, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            merged_path,
            "",  # params
            query_string,
            ""   # fragment
        )
    )

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     url = generate_api_redirect_uri(
#         "https://api.example.com",
#         "/v1/users",
#         {"page": "2", "limit": "50"}
#     )
#     print(url)