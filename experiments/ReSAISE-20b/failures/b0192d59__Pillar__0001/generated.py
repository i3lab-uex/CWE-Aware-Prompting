import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – adjust these values to your environment
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    # Add more approved domains here
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/search",
    # Add more allowed endpoints here
]

# ----------------------------------------------------------------------
# Utility function
# ----------------------------------------------------------------------
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully qualified API redirect URI by merging the base URI,
    endpoint, and optional query parameters.

    Parameters
    ----------
    base_uri : str
        Base URL of the API (e.g., "https://api.example.com").
    api_endpoint : str
        Endpoint path to be appended (e.g., "/v1/users").
    query : dict, optional
        Dictionary of key/value pairs to be URL‑encoded as query parameters.

    Returns
    -------
    str
        The fully assembled, validated URI.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Normalise base_uri and api_endpoint
    parsed_base = urllib.parse.urlparse(base_uri.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri!r}")

    # Ensure the endpoint starts with a slash
    if not api_endpoint.startswith("/"):
        api_endpoint = f"/{api_endpoint}"

    # Verify domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {parsed_base.hostname!r}")

    # Verify endpoint
    if api_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {api_endpoint!r}")

    # Construct the full path
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", api_endpoint.lstrip("/"))
    full_url_parts = parsed_base._replace(path=joined_path)

    # Attach query string if provided
    if query:
        # Filter out None values to avoid accidental injection of "None" strings
        filtered_query = {k: v for k, v in query.items() if v is not None}
        full_url_parts = full_url_parts._replace(query=urllib.parse.urlencode(filtered_query))

    return urllib.parse.urlunparse(full_url_parts)

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        uri = generate_api_redirect_uri(
            base_uri="https://api.example.com",
            api_endpoint="/v1/users",
            query={"id": "123", "verbose": "true"}
        )
        print(uri)
    except ValueError as exc:
        print(f"Validation error: {exc}")