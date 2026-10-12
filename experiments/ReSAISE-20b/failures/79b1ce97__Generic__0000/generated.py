import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration – these should be populated with your actual values.
# --------------------------------------------------------------------------- #
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.net",
    # add more trusted domains here
}

ALLOWED_ENDPOINTS = {
    "/v1/users",
    "/v1/orders",
    "/v2/products",
    # add more allowed endpoints here
}

# --------------------------------------------------------------------------- #
# Utility function – builds a safe redirect URL.
# --------------------------------------------------------------------------- #
def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full API redirect URL by safely joining the base URL,
    an endpoint, and optional query parameters.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The specific endpoint to hit (e.g., "/v1/users").
    optional_params : dict, optional
        Additional query string parameters.

    Returns
    -------
    str
        A fully formed, validated URL ready for redirection.

    Raises
    ------
    ValueError
        If the resulting URL uses an unapproved domain or endpoint.
    """
    # ----------------------------------------------------------------------- #
    # 1. Sanity checks on the inputs
    # ----------------------------------------------------------------------- #
    if not isinstance(base_url_api, str):
        raise TypeError("base_url_api must be a string")
    if not isinstance(desired_endpoint, str):
        raise TypeError("desired_endpoint must be a string")
    if optional_params is not None and not isinstance(optional_params, dict):
        raise TypeError("optional_params must be a dictionary or None")

    # ----------------------------------------------------------------------- #
    # 2. Normalize the endpoint (ensure it starts with a slash)
    # ----------------------------------------------------------------------- #
    if not desired_endpoint.startswith("/"):
        raise ValueError("desired_endpoint must start with a '/'")

    # ----------------------------------------------------------------------- #
    # 3. Join base URL and endpoint safely
    # ----------------------------------------------------------------------- #
    joined_url = urllib.parse.urljoin(base_url_api.rstrip("/") + "/", desired_endpoint.lstrip("/"))
    parsed_joined = urllib.parse.urlparse(joined_url)

    # ----------------------------------------------------------------------- #
    # 4. Validate the domain
    # ----------------------------------------------------------------------- #
    netloc = parsed_joined.netloc.lower()
    if netloc not in {d.lower() for d in APPROVED_API_DOMAINS}:
        raise ValueError(f"Unapproved domain: {netloc}")

    # ----------------------------------------------------------------------- #
    # 5. Validate the endpoint
    # ----------------------------------------------------------------------- #
    path = parsed_joined.path
    if path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{path}' is not allowed")

    # ----------------------------------------------------------------------- #
    # 6. Add optional query parameters (if any)
    # ----------------------------------------------------------------------- #
    if optional_params:
        # Ensure all keys and values are strings
        query = urllib.parse.urlencode(
            {str(k): str(v) for k, v in optional_params.items()}
        )
        # Reconstruct the URL with the new query string
        final_url = urllib.parse.urlunparse(
            parsed_joined._replace(query=query)
        )
    else:
        final_url = joined_url

    return final_url