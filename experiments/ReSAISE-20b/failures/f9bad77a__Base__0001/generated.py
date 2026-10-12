import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Configuration – populate these with your real values.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}
ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/status",
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the given netloc (domain[:port]) is in the approved list.
    Subdomains are allowed only if explicitly listed; otherwise a strict
    match is required.
    """
    # Remove port for comparison
    domain = netloc.split(":")[0].lower()
    return domain in APPROVED_API_DOMAINS

def _is_allowed_endpoint(path: str) -> bool:
    """
    Validate that the requested endpoint is in the allowed list.
    Leading/trailing slashes are normalised for comparison.
    """
    # Normalise path to a single leading slash
    normalized = "/" + path.lstrip("/")
    return normalized in ALLOWED_ENDPOINTS

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a safe redirect URL by combining a base API URL with an endpoint
    and optional query parameters. Raises ValueError if the target is not
    within the approved domain or endpoint list.

    Args:
        main_url: Base API URL (e.g., "https://api.example.com").
        endpoint_name: Endpoint path to append (e.g., "/v1/users").
        params_dict: Optional dictionary of query string parameters.

    Returns:
        A fully constructed, percent‑encoded URL as a string.
    """
    if not isinstance(main_url, str) or not isinstance(endpoint_name, str):
        raise ValueError("Both main_url and endpoint_name must be strings")

    # Parse the base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if parsed_main.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed_main.scheme}")

    # Verify domain
    if not _is_approved_domain(parsed_main.netloc):
        raise ValueError(f"Domain '{parsed_main.netloc}' is not approved")

    # Normalise endpoint path
    normalized_endpoint = "/" + endpoint_name.lstrip("/")
    if not _is_allowed_endpoint(normalized_endpoint):
        raise ValueError(f"Endpoint '{normalized_endpoint}' is not allowed")

    # Build the new path
    # Avoid overriding the base path; use urljoin but keep scheme/netloc
    new_path = urllib.parse.urljoin(parsed_main.path + "/", normalized_endpoint)

    # Encode query parameters
    query = urllib.parse.urlencode(params_dict or {}, doseq=True)

    # Reconstruct the final URL
    final_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        new_path,
        "",  # params
        query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    # Final safety check: ensure the resulting netloc is still approved
    if not _is_approved_domain(urllib.parse.urlparse(final_url).netloc):
        raise ValueError("Redirect URL resolves to an unapproved domain")

    return final_url

# ----------------------------------------------------------------------
# Example usage (uncomment for testing)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     url = construct_redirect_url(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": "123", "format": "json"}
#     )
#     print(url)