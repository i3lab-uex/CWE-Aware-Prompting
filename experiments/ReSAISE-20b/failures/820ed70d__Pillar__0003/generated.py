import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – only approved domains and endpoints are allowed.
# --------------------------------------------------------------------------- #

APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.another.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/public/info",
]

# --------------------------------------------------------------------------- #
# Utility – Assemble a secure, validated API redirect URL.
# --------------------------------------------------------------------------- #

def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API URL by safely combining the base URL, path and
    optional query parameters.  The function validates that the resulting
    domain is approved and that the endpoint path is allowed.

    Parameters
    ----------
    base_api_url : str
        The base URL of the API (e.g., "https://api.example.com").
    api_path : str
        The endpoint path (e.g., "/v1/users").
    query_dict : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully assembled, validated URL.

    Raises
    ------
    ValueError
        If the constructed domain is not in ``APPROVED_API_DOMAINS`` or
        if the endpoint path is not in ``ALLOWED_ENDPOINTS``.
    """
    # --------------------------------------------------------------------- #
    # 1. Resolve the full URL using urljoin (prevents path traversal)
    # --------------------------------------------------------------------- #
    joined_url = urllib.parse.urljoin(base_api_url.rstrip("/") + "/", api_path.lstrip("/"))
    parsed = urllib.parse.urlparse(joined_url)

    # --------------------------------------------------------------------- #
    # 2. Validate domain
    # --------------------------------------------------------------------- #
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved domain: {hostname}")

    # --------------------------------------------------------------------- #
    # 3. Validate endpoint path (case-sensitive)
    # --------------------------------------------------------------------- #
    if parsed.path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Disallowed endpoint: {parsed.path}")

    # --------------------------------------------------------------------- #
    # 4. Append query parameters if provided
    # --------------------------------------------------------------------- #
    if query_dict:
        # Ensure all values are string representations; avoid injection
        safe_query = {k: str(v) for k, v in query_dict.items()}
        query_string = urllib.parse.urlencode(safe_query)
        assembled_url = parsed._replace(query=query_string).geturl()
    else:
        assembled_url = parsed.geturl()

    return assembled_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": 42, "format": "json"}
#     )
#     print(url)   # https://api.example.com/v1/users?id=42&format=json