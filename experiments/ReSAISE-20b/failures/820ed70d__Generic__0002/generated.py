import urllib.parse
from typing import Dict, Optional

# Allowed domains and endpoints for security
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "data.partner.net",
}
ALLOWED_ENDPOINTS = [
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    "/healthcheck",
]


def assemble_api_redirect_link(
    base_api_url: str,
    api_path: str,
    query_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Construct a full API URL by combining a base URL, an endpoint path,
    and optional query parameters.

    Parameters
    ----------
    base_api_url : str
        Base URL of the API (e.g., "https://api.example.com").
    api_path : str
        Endpoint path to append (e.g., "/v1/users").
    query_dict : dict, optional
        Mapping of query keys to values.

    Returns
    -------
    str
        Fully assembled URL ready for redirect.

    Raises
    ------
    ValueError
        If the domain of `base_api_url` is not in ``APPROVED_API_DOMAINS`` or
        if `api_path` is not in ``ALLOWED_ENDPOINTS``.
    """
    # Normalise and parse the base URL
    parsed_base = urllib.parse.urlparse(base_api_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_api_url}")

    # Check domain approval
    domain = parsed_base.hostname.lower()
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Unapproved API domain: {domain}")

    # Ensure the path is an allowed endpoint
    normalized_path = urllib.parse.urljoin("/", api_path)
    if normalized_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Unapproved API endpoint: {normalized_path}")

    # Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path, normalized_path)

    # Encode query parameters if provided
    query = urllib.parse.urlencode(query_dict or {}, doseq=True)

    # Reconstruct the URL
    assembled = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",          # params
            query,       # query
            "",          # fragment
        )
    )

    return assembled


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = assemble_api_redirect_link(
#         "https://api.example.com",
#         "/v1/users",
#         {"id": "123", "verbose": "true"}
#     )
#     print(url)