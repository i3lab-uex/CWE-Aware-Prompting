import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: approved domains and endpoints.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "auth.service.org",
    "data.provider.net",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/transactions",
    "/public/info",
    "/auth/login",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_domain_approved(url: str) -> bool:
    """
    Verify that the URL's domain is in APPROVED_API_DOMAINS.
    """
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    # Remove port if present
    domain = domain.split(":")[0]
    return domain in APPROVED_API_DOMAINS

def _is_endpoint_allowed(endpoint: str) -> bool:
    """
    Verify that the endpoint path is in ALLOWED_ENDPOINTS.
    """
    # Normalize to start with a slash
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    return endpoint in ALLOWED_ENDPOINTS

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Assemble a secure API redirect URL.

    Parameters
    ----------
    base_uri : str
        Base API URL (e.g., "https://api.example.com").
    api_endpoint : str
        Target endpoint path (e.g., "/v1/users").
    query : dict, optional
        Query parameters as key-value pairs.

    Returns
    -------
    str
        Fully qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain is not approved or endpoint is disallowed.
    """
    # Sanitize and validate base URI
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri}")

    # Ensure the domain is approved
    if not _is_domain_approved(base_uri):
        raise ValueError(f"Unapproved domain: {parsed_base.netloc}")

    # Normalize and validate endpoint
    if not _is_endpoint_allowed(api_endpoint):
        raise ValueError(f"Disallowed API endpoint: {api_endpoint}")

    # Build the path by joining base path and endpoint
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = api_endpoint.lstrip("/")
    full_path = f"{base_path}/{endpoint_path}".replace("//", "/")

    # Assemble query string
    if query:
        # Encode values; ensure all keys/values are strings
        encoded_query = urllib.parse.urlencode(
            {k: str(v) for k, v in query.items()}
        )
    else:
        encoded_query = ""

    # Construct the final URL
    final_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        full_path,
        "",  # params
        encoded_query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_api_redirect_uri(
            base_uri="https://api.example.com",
            api_endpoint="/v1/users",
            query={"id": "123", "verbose": "true"}
        )
        print(url)
    except ValueError as e:
        print(f"URL generation failed: {e}")