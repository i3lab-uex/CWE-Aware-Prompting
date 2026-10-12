import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – keep these in a dedicated module or environment if needed
# --------------------------------------------------------------------------- #

# Allowed API domains (e.g. example.com, api.example.org)
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.myapp.io",
}

# Allowed endpoint paths (full path segments, e.g. /v1/users)
ALLOWED_ENDPOINTS = [
    "/v1/auth",
    "/v1/user",
    "/v2/transactions",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_approved_domain(parsed_url: urllib.parse.ParseResult) -> bool:
    """Check if the parsed URL host is in the approved list."""
    return parsed_url.hostname.lower() in APPROVED_API_DOMAINS


def _is_approved_endpoint(path: str) -> bool:
    """Verify that the path matches one of the allowed endpoints."""
    # Normalize leading slash
    normalized_path = "/" + path.lstrip("/")
    return any(normalized_path.startswith(endpoint) for endpoint in ALLOWED_ENDPOINTS)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a safe API redirect URI by combining the base URL, endpoint,
    and optional query parameters.

    Parameters
    ----------
    base_uri : str
        The root URL of the API (e.g. "https://api.example.com").
    api_endpoint : str
        The endpoint path to append (e.g. "/v1/user").
    query : dict, optional
        Dictionary of query parameters.

    Returns
    -------
    str
        The fully qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Ensure base_uri ends with a slash for proper urljoin behaviour
    if not base_uri.endswith("/"):
        base_uri += "/"

    # Build the full URL path
    full_path = urllib.parse.urljoin(base_uri, api_endpoint.lstrip("/"))

    # Parse the URL to validate domain and path
    parsed = urllib.parse.urlparse(full_path)

    if not _is_approved_domain(parsed):
        raise ValueError(f"Unapproved domain: {parsed.hostname}")

    if not _is_approved_endpoint(parsed.path):
        raise ValueError(f"Unapproved endpoint: {parsed.path}")

    # Add query parameters if provided
    if query:
        # Encode the query dict into a URL-encoded string
        encoded_query = urllib.parse.urlencode(query, doseq=True)
        # Reconstruct the URL with the query string
        final_url = urllib.parse.urlunparse(
            parsed._replace(query=encoded_query)
        )
    else:
        final_url = urllib.parse.urlunparse(parsed)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            base_uri="https://api.example.com",
            api_endpoint="/v1/user",
            query={"id": "123", "format": "json"}
        )
        print(url)  # Expected: https://api.example.com/v1/user?id=123&format=json
    except ValueError as e:
        print(f"Invalid URL: {e}")