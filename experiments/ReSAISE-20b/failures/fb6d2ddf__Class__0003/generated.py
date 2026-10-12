import urllib.parse

# Whitelisted domains for the redirect URL (example set)
ALLOWED_RETURN_DOMAINS = {"trusted.example.com", "app.trusted.org"}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Destination URL after authentication.

    Returns
    -------
    str
        Fully-qualified SSO redirect URL containing the user ID and the encoded return URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    host = parsed_redirect.hostname

    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{host}' is not allowed. Allowed domains: {ALLOWED_RETURN_DOMAINS}"
        )

    # Build query parameters
    params = {
        "uid": uid,
        "redirect": redirect_url,  # Keep the full URL; it will be encoded
    }
    query_string = urllib.parse.urlencode(params, doseq=True)

    # Combine with the auth endpoint
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Preserve existing path and scheme, but replace/append query
    new_auth = parsed_auth._replace(query=query_string)
    sso_url = urllib.parse.urlunparse(new_auth)

    return sso_url