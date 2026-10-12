import urllib.parse

# Set of domains allowed for the return URL. Adjust as needed.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more trusted domains here
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to redirect back to after SSO authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL with encoded query parameters.

    Raises
    ------
    ValueError
        If the domain of `back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the back_url to extract its domain
    parsed_back = urllib.parse.urlparse(back_url)
    host = parsed_back.hostname

    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Prepare query parameters
    params = {
        "user_ref": user_ref,
        "return_url": back_url,
    }

    # Encode parameters and construct the final URL
    query_string = urllib.parse.urlencode(params, safe="/:?&=")
    # Ensure the base SSO service URL is absolute and has no trailing slash
    base = sso_service.rstrip("/")
    return f"{base}?{query_string}"