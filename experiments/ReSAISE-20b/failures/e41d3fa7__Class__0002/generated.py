import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration: trusted domains and allowed endpoints
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

# ------------------------------------------------------------------
# Helper: normalize and validate domain
# ------------------------------------------------------------------
def _validate_domain(parsed_url: urllib.parse.ParseResult) -> None:
    """
    Ensure the parsed URL's network location (netloc) is one of the approved domains.
    """
    # Strip potential port numbers
    domain = parsed_url.netloc.split(":")[0].lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {domain}")

# ------------------------------------------------------------------
# Helper: normalize and validate endpoint
# ------------------------------------------------------------------
def _validate_endpoint(endpoint_path: str) -> None:
    """
    Ensure the endpoint path is in the allowed list.
    The comparison is case‑sensitive and expects a leading slash.
    """
    if not endpoint_path.startswith("/"):
        raise ValueError("Endpoint path must start with a leading slash '/'")
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {endpoint_path}")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_redirect_link(
    base_url: str,
    endpoint_path: str,
    query_info: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a fully‑qualified redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The main API base URL (e.g. "https://api.example.com").
    endpoint_path : str
        The API endpoint path (e.g. "/users").
    query_info : dict, optional
        Dictionary of query string parameters to append.

    Returns
    -------
    str
        A validated, fully‑qualified URL ready for use in an HTTP redirect.

    Raises
    ------
    ValueError
        If the base URL's domain is not approved or if the endpoint path is disallowed.
    """
    # Parse the base URL and validate its domain
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    _validate_domain(parsed_base)

    # Validate the endpoint path
    _validate_endpoint(endpoint_path)

    # Build the new URL components
    scheme = parsed_base.scheme
    netloc = parsed_base.netloc
    path = urllib.parse.urljoin(parsed_base.path, endpoint_path)
    params = ""  # No parameters for this use‑case
    fragment = ""  # No fragment

    # Encode query parameters if provided
    query = ""
    if query_info:
        if not isinstance(query_info, dict):
            raise ValueError("query_info must be a dictionary")
        # Ensure all keys and values are strings
        for k, v in query_info.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("All query keys and values must be strings")
        query = urllib.parse.urlencode(query_info)

    # Assemble the final URL
    full_url = urllib.parse.urlunparse(
        (scheme, netloc, path, params, query, fragment)
    )

    # Final safety check: ensure the resulting domain is still approved
    parsed_full = urllib.parse.urlparse(full_url)
    _validate_domain(parsed_full)

    return full_url