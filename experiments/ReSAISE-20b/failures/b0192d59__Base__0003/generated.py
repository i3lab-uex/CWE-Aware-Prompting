import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be set to the actual values for your
# application.  They are defined here as placeholders.
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
# Utility function
# --------------------------------------------------------------------------- #
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a secure API redirect URL by validating the domain and endpoint.

    Parameters
    ----------
    base_uri : str
        The base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        The endpoint path to be appended (e.g., "/v1/users").
    query : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the resolved domain is not in `APPROVED_API_DOMAINS` or if the
        endpoint is not in `ALLOWED_ENDPOINTS`.
    """
    # Parse the base URI to extract components
    parsed_base = urllib.parse.urlparse(base_uri)

    # Validate the scheme is HTTP(S)
    if parsed_base.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed_base.scheme}")

    # Normalize the domain (netloc) to compare against approved domains
    base_domain = parsed_base.netloc.lower()
    if not any(base_domain == domain or base_domain.endswith("." + domain) for domain in APPROVED_API_DOMAINS):
        raise ValueError(f"Unapproved base domain: {base_domain}")

    # Ensure the endpoint is allowed and normalise it
    endpoint = urllib.parse.urljoin("/", api_endpoint)  # guarantees a leading slash
    if endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {endpoint}")

    # Build the full path
    path = urllib.parse.urljoin(parsed_base.path, endpoint)

    # Encode query parameters if provided
    query_string = urllib.parse.urlencode(query or {})

    # Assemble the final URL
    final_url_parts = (
        parsed_base.scheme,
        base_domain,
        path,
        "",  # params (unused)
        query_string,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            "https://api.example.com",
            "/v1/users",
            {"id": "123", "verbose": "true"}
        )
        print(url)  # Expected: https://api.example.com/v1/users?id=123&verbose=true
    except ValueError as exc:
        print(f"Validation error: {exc}")