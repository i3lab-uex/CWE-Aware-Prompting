import urllib.parse

# Domains that are allowed to be used as return URLs
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org", "trusted.io"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to redirect back to after authentication.

    Returns
    -------
    str
        Fully-qualified SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of `back_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the return URL to validate its domain
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("Invalid back_url: must be a fully-qualified URL")

    # Extract the domain (hostname) and compare against allowed set
    hostname = parsed_back.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{hostname}' is not allowed")

    # Build query parameters
    query_params = {
        "user_ref": user_ref,
        "return_url": back_url,
    }

    # Encode query string
    encoded_query = urllib.parse.urlencode(query_params)

    # Ensure the SSO service URL does not already contain a query
    base = sso_service.rstrip("?")
    redirect_url = f"{base}?{encoded_query}"
    return redirect_url