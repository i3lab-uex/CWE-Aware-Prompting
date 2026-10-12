import urllib.parse

# Whitelisted domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted.partner.net"
}


def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that redirects the user to an external
    identity provider and then back to `redirect_url`.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO endpoint (e.g. "https://sso.example.com/login").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        Full SSO redirect URL that can be used in an HTTP redirect response.

    Raises
    ------
    ValueError
        If `redirect_url` is not a fully-qualified URL with an allowed domain.
    """
    # Parse the redirect URL to validate its components
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully-qualified URL")

    # Extract the domain (host part) and normalize it for comparison
    host = parsed_redirect.netloc.split(':')[0].lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{host}' is not allowed")

    # Ensure the auth endpoint is also a valid URL
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        raise ValueError("auth_endpoint must be a fully-qualified URL")

    # Build the query parameters for the SSO request
    sso_params = {
        "uid": uid,
        # Pass the redirect URL in an encoded form to avoid breaking query syntax
        "return_to": urllib.parse.quote_plus(redirect_url)
    }

    # Construct the final SSO URL
    sso_query = urllib.parse.urlencode(sso_params)
    sso_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path or "",
        parsed_auth.params,
        sso_query,
        ""  # fragment
    )
    return urllib.parse.urlunparse(sso_url_parts)