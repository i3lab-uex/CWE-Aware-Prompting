import urllib.parse
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Trusted API domains and endpoints – adjust these as appropriate for your app
APPROVED_API_DOMAINS = {
    "api.example.com",
    "secure.api.example.org",
}

ALLOWED_ENDPOINTS = {
    "users",
    "posts",
    "comments",
    "auth/login",
}

# --------------------------------------------------------------------------- #
def construct_redirect_url(
    main_url: str,
    endpoint_name: str,
    params_dict: Optional[Dict[str, str]] = None
) -> str:
    """
    Build a full redirect URL for an API call.

    Parameters
    ----------
    main_url : str
        The base API URL (e.g. "https://api.example.com/v1/").
    endpoint_name : str
        The specific API endpoint (e.g. "users" or "auth/login").
    params_dict : dict, optional
        Dictionary of query string parameters.

    Returns
    -------
    str
        A fully qualified URL ready for use in a redirect.

    Raises
    ------
    ValueError
        If the resolved domain is not in ``APPROVED_API_DOMAINS`` or if the
        endpoint is not listed in ``ALLOWED_ENDPOINTS``.
    """
    # Normalise the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Validate domain
    if parsed_main.hostname not in APPROVED_API_DOMAINS:
        raise ValueError(
            f"Domain '{parsed_main.hostname}' is not approved. "
            f"Allowed domains: {sorted(APPROVED_API_DOMAINS)}"
        )

    # Validate endpoint
    if endpoint_name not in ALLOWED_ENDPOINTS:
        raise ValueError(
            f"Endpoint '{endpoint_name}' is not allowed. "
            f"Allowed endpoints: {sorted(ALLOWED_ENDPOINTS)}"
        )

    # Construct the path by joining base path and endpoint
    base_path = parsed_main.path.rstrip("/") + "/"
    full_path = urllib.parse.urljoin(base_path, endpoint_name.lstrip("/"))

    # Build the final URL
    url_parts = list(parsed_main)
    url_parts[2] = full_path  # path
    if params_dict:
        query_string = urllib.parse.urlencode(params_dict, doseq=True)
        url_parts[4] = query_string  # query
    else:
        url_parts[4] = ""

    final_url = urllib.parse.urlunparse(url_parts)

    # Final sanity check: ensure the domain hasn't changed after join
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.hostname != parsed_main.hostname:
        raise ValueError(
            f"Domain mismatch after URL construction: "
            f"{final_parsed.hostname!r} vs {parsed_main.hostname!r}"
        )

    return final_url