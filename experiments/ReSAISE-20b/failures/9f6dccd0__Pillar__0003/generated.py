import urllib.parse
from typing import Dict, Optional

# Pre-approved API domains and allowed endpoints.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "data.partner.net",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v2/orders",
    "/search",
    "/healthcheck",
]


def generate_api_redirect(
    base_url: str,
    api_path: str,
    params: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a safe redirect URL for an API call.

    Parameters
    ----------
    base_url : str
        The base address of the API, e.g. "https://api.example.com".
    api_path : str
        The endpoint path, e.g. "/v1/users".
    params : dict[str, str] | None
        Optional query parameters to include in the URL.

    Returns
    -------
    str
        A fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting domain is not in `APPROVED_API_DOMAINS` or
        if the endpoint path is not in `ALLOWED_ENDPOINTS`.
    """
    # Parse the base URL to validate scheme and domain.
    parsed_base = urllib.parse.urlparse(base_url)
    if not parsed_base.scheme in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_base.scheme}")

    # Ensure the domain is approved.
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Validate the endpoint path.
    normalized_path = urllib.parse.urljoin("/", api_path)
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{normalized_path}' is not allowed")

    # Build the path by joining base path and API path.
    full_path = urllib.parse.urljoin(parsed_base.path + "/", normalized_path.lstrip("/"))

    # Assemble query string if parameters are provided.
    query = urllib.parse.urlencode(params or {}, doseq=True)

    # Construct the final URL.
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params (deprecated)
            query,
            "",  # fragment
        )
    )

    return redirect_url


# Example usage (commented out; remove comments to test)
# if __name__ == "__main__":
#     url = generate_api_redirect(
#         base_url="https://api.example.com",
#         api_path="/v1/users",
#         params={"page": "2", "limit": "50"},
#     )
#     print(url)