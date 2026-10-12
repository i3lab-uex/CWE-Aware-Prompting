import urllib.parse
from typing import Dict, Optional

# Trusted domains and endpoints – in a real project these would be loaded from config
APPROVED_API_DOMAINS = {"api.example.com", "service.partner.org"}
ALLOWED_ENDPOINTS = {
    "/users",
    "/orders",
    "/products",
    "/status",
}

def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None,
) -> str:
    """
    Build a full redirect URL for an API request.

    Parameters
    ----------
    main_url : str
        The base URL of the API, e.g. "https://api.example.com".
    endpoint_name : str
        The relative path to the desired API endpoint, e.g. "/users".
    params_dict : dict[str,str] | None
        Optional query parameters to append.

    Returns
    -------
    str
        A fully-qualified URL that can be used for a redirect.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or uses a disallowed endpoint.
    """
    # 1. Parse the main URL to extract components
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("main_url must be a valid absolute URL")

    # 2. Validate domain
    domain = parsed_main.hostname
    if domain not in APPROVED_API_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved")

    # 3. Normalize endpoint path
    if not endpoint_name.startswith("/"):
        endpoint_path = f"/{endpoint_name}"
    else:
        endpoint_path = endpoint_name

    # 4. Validate endpoint
    if endpoint_path not in ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint '{endpoint_path}' is not allowed")

    # 5. Build the final URL
    #   - Keep scheme and netloc from main_url
    #   - Append the validated endpoint path
    #   - Encode query parameters if provided
    query = urllib.parse.urlencode(params_dict or {}, doseq=True)
    final_parts = (
        parsed_main.scheme,
        parsed_main.netloc,
        endpoint_path,
        "",  # params
        query,
        ""   # fragment
    )
    final_url = urllib.parse.urlunparse(final_parts)

    return final_url