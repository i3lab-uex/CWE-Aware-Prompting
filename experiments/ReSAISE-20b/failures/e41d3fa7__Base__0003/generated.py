import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – in a real project these would come from secure settings
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.example.org",
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_endpoint(endpoint: str) -> str:
    """
    Normalise an endpoint path:
      * Ensure it starts with a single slash.
      * Remove trailing slashes for consistency.
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return endpoint.rstrip("/") or "/"

def _validate_domain(netloc: str) -> None:
    """
    Raise ValueError if the domain is not in APPROVED_API_DOMAINS.
    """
    # netloc may contain port; strip it
    domain = netloc.split(":")[0]
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {domain}")

def _validate_endpoint(endpoint: str) -> None:
    """
    Raise ValueError if the endpoint is not in ALLOWED_ENDPOINTS.
    """
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {endpoint}")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a safe redirect URL for an API request.

    Parameters
    ----------
    base_url : str
        The root API URL (e.g., "https://api.example.com").
    endpoint_path : str
        The specific API path (e.g., "/v1/users").
    query_info : dict, optional
        Mapping of query parameters to include.

    Returns
    -------
    str
        A fully formed URL that is guaranteed to target an approved domain
        and endpoint.

    Raises
    ------
    ValueError
        If the constructed URL resolves to an unapproved domain or endpoint.
    """
    # Parse the base URL and validate its domain
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")
    _validate_domain(parsed_base.netloc)

    # Normalise and validate the endpoint
    normalized_endpoint = _normalize_endpoint(endpoint_path)
    _validate_endpoint(normalized_endpoint)

    # Construct the new path by combining base path and endpoint
    # Use urljoin to correctly handle slashes
    combined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_endpoint.lstrip("/"))

    # Merge query parameters if provided
    if query_info:
        encoded_query = urllib.parse.urlencode(query_info, doseq=True)
    else:
        encoded_query = parsed_base.query

    # Rebuild the full URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        combined_path,
        "",  # params (rarely used)
        encoded_query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or guard under __name__ == "__main__")
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_redirect_link(
            "https://api.example.com",
            "/v1/users",
            {"page": "2", "size": "50"}
        )
        print(url)
    except ValueError as e:
        print(f"URL generation failed: {e}")