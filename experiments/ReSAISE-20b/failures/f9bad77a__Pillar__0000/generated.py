import urllib.parse
from typing import Dict, Optional

# Trusted domains that the API can redirect to
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.org",
    "services.mycompany.net",
}

# Valid endpoints that are allowed to be called
ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "auth/login",
    "auth/logout",
}

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Construct a fully-qualified redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base API URL (e.g. "https://api.example.com/v1").
    endpoint_name : str
        The API endpoint to append (e.g. "users").
    params_dict : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to an unapproved domain or endpoint.
    """
    # Parse the base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Ensure the domain is approved
    if parsed_main.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain {parsed_main.hostname!r} is not approved")

    # Validate the endpoint
    if endpoint_name.lstrip("/").rstrip("/") not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint {endpoint_name!r} is not allowed")

    # Build the new path, preserving any existing path segments
    base_path = parsed_main.path.rstrip("/")
    endpoint_clean = endpoint_name.strip("/")
    new_path = f"{base_path}/{endpoint_clean}"

    # Encode query parameters if provided
    query_string = ""
    if params_dict:
        if not isinstance(params_dict, dict):
            raise ValueError("params_dict must be a dictionary")
        query_string = urllib.parse.urlencode(params_dict)

    # Assemble the final URL
    new_url_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        new_path,
        parsed_main.params,
        query_string,
        parsed_main.fragment,
    )
    redirect_url = urllib.parse.urlunparse(new_url_parts)

    # Final sanity check: ensure the URL is still within an approved domain
    final_parsed = urllib.parse.urlparse(redirect_url)
    if final_parsed.hostname not in APPROVED_API_DOMAINS:
        raise ValueError("Resulting URL points to an unapproved domain")

    return redirect_url