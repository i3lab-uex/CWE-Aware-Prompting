import urllib.parse
from typing import Dict, Optional

# ----------------------------------------------------------------------
# Trusted configuration – in a real application these would be
# defined elsewhere and kept out of source control or injected at runtime.
# ----------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "trusted.api.net",
}

ALLOWED_ENDPOINTS = {
    "users",
    "orders",
    "products",
    "inventory",
}

# ----------------------------------------------------------------------
# Helper function: normalise and validate a domain
# ----------------------------------------------------------------------
def _extract_domain(url: str) -> str:
    """
    Extract the network location part (netloc) of a URL.
    Raises ValueError if parsing fails or netloc is empty.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    return parsed.netloc.lower()

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base URL of the API (e.g. "https://api.example.com/v1").
    endpoint_name : str
        The desired API endpoint (e.g. "users").
    params_dict : dict, optional
        Dictionary of query string parameters to append.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the target domain or endpoint is not approved.
    """
    # Validate and normalise the main URL
    base_netloc = _extract_domain(main_url)

    if base_netloc not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{base_netloc}' is not in the list of approved API domains."
        )

    # Validate endpoint
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{endpoint_name}' is not an allowed API endpoint."
        )

    # Build the path – ensure no double slashes
    parsed_main = urllib.parse.urlparse(main_url)
    base_path = parsed_main.path.rstrip("/")
    endpoint_path = f"/{endpoint_name.lstrip('/')}"
    full_path = urllib.parse.urljoin(base_path + "/", endpoint_path)

    # Encode query parameters
    if params_dict:
        query = urllib.parse.urlencode(params_dict, doseq=True)
    else:
        query = ""

    # Reconstruct the full URL
    new_url_parts = (
        parsed_main.scheme,
        base_netloc,
        full_path,
        "",          # params
        query,       # query
        ""           # fragment
    )
    redirect_url = urllib.parse.urlunparse(new_url_parts)

    return redirect_url

# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com/v1",
            "users",
            {"page": "2", "limit": "50"}
        )
        print(url)
    except ValueError as exc:
        print(f"Error: {exc}")