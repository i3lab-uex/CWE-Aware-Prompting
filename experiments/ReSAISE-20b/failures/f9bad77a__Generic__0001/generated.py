import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: replace these with your actual values
APPROVED_API_DOMAINS = {
    "api.example.com",
    "service.otherdomain.org",
}

ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "login",
}

# --------------------------------------------------------------------------- #
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
        Base API URL (e.g., "https://api.example.com/v1").
    endpoint_name : str
        Desired API endpoint (e.g., "users").
    params_dict : dict, optional
        Dictionary of query parameters to append.

    Returns
    -------
    str
        The fully constructed URL.

    Raises
    ------
    ValueError
        If the final URL does not use an approved domain or endpoint.
    """
    if params_dict is None:
        params_dict = {}

    # Parse the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url}")

    # Validate domain
    if parsed_main.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_main.netloc}' is not in the list of approved domains."
        )

    # Validate endpoint
    if endpoint_name.lower() not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{endpoint_name}' is not in the list of allowed endpoints."
        )

    # Build path: ensure it ends with a slash and append endpoint
    base_path = parsed_main.path.rstrip("/") + "/"
    full_path = urllib.parse.urljoin(base_path, endpoint_name)

    # Encode query parameters
    query_string = urllib.parse.urlencode(params_dict)

    # Reconstruct the URL
    final_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        full_path,
        "",  # params
        query_string,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out to keep the module clean)
# if __name__ == "__main__":
#     url = construct_redirect_url(
#         "https://api.example.com/v1",
#         "users",
#         {"page": "2", "sort": "asc"}
#     )
#     print(url)