import urllib.parse

# Define the set of allowed return domains.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    "trustedpartner.net",
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service : str
        The base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        The URL to return to after SSO.

    Returns
    -------
    str
        A fully constructed SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL and extract its hostname.
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be a valid absolute URL")

    # Normalize hostname (lowercase, strip port if present).
    host = parsed_back.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build query parameters for the SSO request.
    query_params = {
        "user_ref": user_ref,
        "return_url": back_url,  # include the full URL
    }
    encoded_params = urllib.parse.urlencode(query_params)

    # Combine the SSO service base URL with the encoded query string.
    parsed_sso = urllib.parse.urlparse(sso_service)
    # Preserve any existing query parameters on the SSO service URL.
    existing_query = parsed_sso.query
    if existing_query:
        new_query = f"{existing_query}&{encoded_params}"
    else:
        new_query = encoded_params

    # Reconstruct the full SSO redirect URL.
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return sso_redirect