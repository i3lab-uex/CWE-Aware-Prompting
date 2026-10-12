import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Allowed resources
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/metrics",
]


def _validate_domain(netloc: str) -> None:
    """
    Ensure the hostname is in the approved domain list.
    Raises ValueError if not approved.
    """
    host = netloc.split(":")[0]  # strip port if present
    if host not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {host}")


def _validate_endpoint(path: str) -> None:
    """
    Ensure the path is in the allowed endpoints list.
    Raises ValueError if not approved.
    """
    # Normalise path: strip trailing slash for comparison
    normalized = path.rstrip("/")
    if not any(normalized == ep.rstrip("/") for ep in ALLOWED_ENDPOINTS):
        raise ValueError(f"Unapproved endpoint: {path}")


def create_api_redirect_link(
    base_url: str,
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a secure API redirect URL.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g., "https://api.example.com").
    path : str
        The target endpoint path (e.g., "/v1/users").
    params : dict, optional
        Query parameters to append.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the resulting domain or endpoint is not approved.
    """
    # Parse base URL to ensure it has a scheme
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (http/https).")

    # Validate domain and endpoint
    _validate_domain(parsed_base.netloc)
    _validate_endpoint(path)

    # Build the path part
    full_path = urllib.parse.urljoin(parsed_base.path + "/", path.lstrip("/"))

    # Merge query parameters
    base_query = urllib.parse.parse_qs(parsed_base.query)
    if params:
        # Encode new params and merge
        for k, v in params.items():
            base_query[k] = [v]
    encoded_query = urllib.parse.urlencode(base_query, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            encoded_query,
            "",  # fragment
        )
    )

    return final_url


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     url = create_api_redirect_link(
#         base_url="https://api.example.com",
#         path="/v1/users",
#         params={"id": "123", "format": "json"}
#     )
#     print(url)  # https://api.example.com/v1/users?id=123&format=json