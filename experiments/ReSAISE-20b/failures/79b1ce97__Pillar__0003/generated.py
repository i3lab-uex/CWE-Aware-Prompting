import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration: approved domains and endpoints.  These should be kept in a
# secure, immutable configuration file or environment variables in real
# deployments.  For demonstration purposes we hard‑code them here.
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.company.org",
}

ALLOWED_ENDPOINTS = {
    "/users",
    "/accounts",
    "/transactions",
    "/reports/summary",
}

# --------------------------------------------------------------------------- #
def create_redirect_url(
    base_url_api: str,
    desired_endpoint: str,
    optional_params: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a full redirect URL for an API request.

    Parameters
    ----------
    base_url_api : str
        The main API base URL (e.g., "https://api.example.com").
    desired_endpoint : str
        The endpoint path to append (e.g., "/users").
    optional_params : dict, optional
        Query string parameters to append.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the domain is not approved, the endpoint is disallowed,
        or the URL contains suspicious components.
    """
    # --------------------------------------------------------------------- #
    # 1. Parse and validate the base URL
    parsed_base = urllib.parse.urlparse(base_url_api)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must include scheme and domain")

    # Reject any base URLs that are not in the approved list
    if parsed_base.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{parsed_base.hostname}' is not approved")

    # Ensure the base URL does not contain a path that could interfere
    if parsed_base.path and parsed_base.path != "/":
        raise ValueError("Base URL should not contain a path component")

    # --------------------------------------------------------------------- #
    # 2. Validate the endpoint
    if not desired_endpoint.startswith("/"):
        raise ValueError("Endpoint must start with '/'")

    # Reject endpoints containing '..' or other suspicious patterns
    if ".." in desired_endpoint:
        raise ValueError("Endpoint contains disallowed path traversal")

    # Ensure the endpoint is in the whitelist
    if desired_endpoint not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{desired_endpoint}' is not allowed")

    # --------------------------------------------------------------------- #
    # 3. Build the full path
    full_path = urllib.parse.urljoin(parsed_base.path, desired_endpoint)

    # --------------------------------------------------------------------- #
    # 4. Encode query parameters if provided
    query = ""
    if optional_params:
        if not isinstance(optional_params, dict):
            raise ValueError("optional_params must be a dictionary")
        # Ensure all keys/values are strings to avoid surprises
        for k, v in optional_params.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("Query parameters must be string key/value pairs")
        query = urllib.parse.urlencode(optional_params)

    # --------------------------------------------------------------------- #
    # 5. Assemble the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            full_path,
            "",  # params
            query,
            ""   # fragment
        )
    )

    return final_url

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
#
# if __name__ == "__main__":
#     url = create_redirect_url(
#         "https://api.example.com",
#         "/users",
#         {"page": "2", "limit": "50"}
#     )
#     print(url)  # Expected: https://api.example.com/users?page=2&limit=50