import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – adjust these sets/lists to your environment
# --------------------------------------------------------------------------- #

# Domains that are considered safe for API calls.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

# Endpoints that are explicitly permitted.
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/items",
    "/v2/orders",
]

# --------------------------------------------------------------------------- #
# Core implementation
# --------------------------------------------------------------------------- #

def generate_api_redirect_uri(
    base_uri: str,
    api_endpoint: str,
    query: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully-qualified API URL from a base URI, endpoint and optional
    query parameters while guarding against open‑redirect attacks.

    Parameters
    ----------
    base_uri : str
        The API's base URL (e.g., "https://api.example.com").
    api_endpoint : str
        The target endpoint (e.g., "/v1/users").
    query : dict, optional
        Dictionary of key/value pairs to be added as query parameters.

    Returns
    -------
    str
        The fully-qualified, validated URL.

    Raises
    ------
    ValueError
        If the base URI's domain or endpoint is not approved.
    """
    # 1. Parse the base URI
    parsed_base = urllib.parse.urlparse(base_uri)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URI: {base_uri}")

    # 2. Validate the domain
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # 3. Normalize and validate the endpoint
    cleaned_endpoint = urllib.parse.urljoin("/", api_endpoint)
    if not cleaned_endpoint.startswith("/"):
        raise ValueError(f"Endpoint must start with a '/': {api_endpoint}")

    # Prevent directory traversal or absolute URLs
    if ".." in cleaned_endpoint.split("/"):
        raise ValueError("Endpoint contains disallowed path traversal characters")

    if cleaned_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{cleaned_endpoint}' is not allowed")

    # 4. Assemble the final path
    # Use urljoin to correctly combine base path with endpoint
    full_path = urllib.parse.urljoin(parsed_base.path + "/", cleaned_endpoint)

    # 5. Append query parameters, if any
    if query:
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary")
        # Ensure all keys/values are strings
        query_items = {
            str(k): str(v) for k, v in query.items()
        }
        encoded_query = urllib.parse.urlencode(query_items)
    else:
        encoded_query = ""

    # 6. Rebuild the URL
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
        print(url)  # Expected: https://api.example.com/v1/users?id=123&verbose=true
    except ValueError as e:
        print(f"URL construction failed: {e}")