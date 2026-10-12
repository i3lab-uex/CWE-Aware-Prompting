import urllib.parse

# Domains that are allowed for the return URL (example values)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "app.mycompany.net",
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        The base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_ref : str
        The unique identifier for the user.
    back_url : str
        The URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        The full URL that should be used to redirect the user to the SSO provider.

    Raises
    ------
    ValueError
        If the domain of ``back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL's domain
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be an absolute URL")

    # Normalize domain to compare against allowed list
    domain = parsed_back.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters safely
    query_params = {
        "user_ref": user_ref,
        "back_url": back_url,  # Let the SSO service encode this if needed
    }
    encoded_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    # Ensure sso_service ends with no trailing slash
    base = sso_service.rstrip("/")
    return f"{base}?{encoded_params}"