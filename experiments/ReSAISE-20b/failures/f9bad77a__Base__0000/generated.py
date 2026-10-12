import urllib.parse
from typing import Dict, Optional

# Trusted domains and endpoints. Adjust these lists to your environment.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "services.partner.com",
}
ALLOWED_ENDPOINTS = {
    "users",
    "orders",
    "products",
    "inventory",
}


def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a fully qualified redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        Base URL of the API (e.g., "https://api.example.com").
    endpoint_name : str
        Specific API endpoint (e.g., "users").
    params_dict : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        Fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the domain or endpoint is not approved.
    """
    # Parse the base URL to ensure it has a valid scheme and netloc
    parsed_base = urllib.parse.urlparse(main_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL: missing scheme or host")

    # Check that the domain is approved
    if parsed_base.netloc.lower() not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.netloc}' is not approved")

    # Ensure the endpoint is allowed
    if endpoint_name.lower() not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_name}' is not allowed")

    # Construct the path: base path + endpoint
    base_path = parsed_base.path.rstrip("/")
    endpoint_path = f"/{endpoint_name.lstrip('/')}"
    full_path = urllib.parse.urljoin(base_path + "/", endpoint_path)

    # Encode query parameters if provided
    query_string = ""
    if params_dict:
        # Filter out None values and convert all keys/values to strings
        cleaned_params = {
            str(k): str(v) for k, v in params_dict.items() if v is not None
        }
        query_string = urllib.parse.urlencode(cleaned_params)

    # Rebuild the URL with the new path and query string
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return redirect_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = construct_redirect_url(
            "https://api.example.com/v1",
            "users",
            {"id": 123, "verbose": "true"},
        )
        print(url)
    except ValueError as e:
        print(f"URL construction failed: {e}")