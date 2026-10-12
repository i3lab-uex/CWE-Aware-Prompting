import urllib.parse
from typing import Dict, Optional

# ------------------------------------------------------------------
# Configuration – keep these values up‑to‑date with your environment
# ------------------------------------------------------------------
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
]

# ------------------------------------------------------------------
# Core functionality
# ------------------------------------------------------------------
def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a fully qualified API URL from a base, an endpoint path,
    and optional query parameters. The function validates that the
    resulting URL uses an approved domain and a permitted endpoint.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g. "https://api.example.com").
    api_path : str
        Endpoint path, starting with a slash (e.g. "/v1/users").
    query_dict : dict | None
        Optional dictionary of query parameters.

    Returns
    -------
    str
        The assembled, fully qualified URL.

    Raises
    ------
    ValueError
        If the domain is not in ``APPROVED_API_DOMAINS`` or the
        endpoint is not listed in ``ALLOWED_ENDPOINTS``.
    """
    # Ensure base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme:
        base_api_url = f"https://{base_api_url}"
        parsed_base = urllib.parse.urlparse(base_api_url)

    # Validate domain
    netloc = parsed_base.netloc.lower()
    if not any(netloc.endswith(domain) for domain in APPROVED_API_DOMAINS):
        raise ValueError(f"Unapproved domain: {netloc}")

    # Validate endpoint
    normalized_path = urllib.parse.normpath(api_path)
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved endpoint: {normalized_path}")

    # Construct the path part
    joined_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_path.lstrip("/"))

    # Build query string
    if query_dict:
        # Ensure all keys/values are strings to avoid type errors in urlencode
        safe_query = {str(k): str(v) for k, v in query_dict.items()}
        query_string = urllib.parse.urlencode(safe_query)
    else:
        query_string = ""

    # Assemble final URL
    final_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        joined_path,
        "",          # params
        query_string,
        ""           # fragment
    ))

    return final_url

# ------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        url = assemble_api_redirect_link(
            base_api_url="api.example.com",
            api_path="/v1/users",
            query_dict={"page": "2", "sort": "asc"}
        )
        print(url)
    except ValueError as exc:
        print(f"URL construction failed: {exc}")