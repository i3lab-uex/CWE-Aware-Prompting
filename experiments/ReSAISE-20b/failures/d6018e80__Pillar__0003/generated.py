import urllib.parse

# Domains that are allowed to receive the SSO redirect callback.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add more trusted domains as needed.
}


def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that the client can use to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL to inspect its domain.
    parsed_return = urllib.parse.urlparse(redirect_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Invalid redirect URL: missing scheme or host")

    # Normalise the domain for comparison (lowercase, strip port).
    host = parsed_return.hostname.lower() if parsed_return.hostname else ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Build query parameters for the SSO request.
    params = {
        "uid": uid,
        # Encode the original redirect URL so that the SSO provider can
        # safely forward the user back to it after authentication.
        "return_url": redirect_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?=&")

    # Combine the base SSO URL with the query string.
    sso_redirect = urllib.parse.urljoin(sso_url, f"?{query_string}")

    return sso_redirect