import urllib.parse

# Domains that are allowed to receive the user after authentication.
ALLOWED_RETURN_DOMAINS = {"example.com", "auth.example.org"}

def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a complete SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        Base URL of the SSO service endpoint.
    user_identifier : str
        Unique identifier for the user (will be passed as a query parameter).
    redirect_uri : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        Fully-qualified redirect URL ready to send the user to the SSO provider.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect_uri domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect URI: {redirect_uri!r}")

    # Extract the hostname without port
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Construct query parameters
    params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_uri,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&")  # preserve redirect_uri encoding

    # Build the final URL
    return f"{auth_service_endpoint.rstrip('/')}/login?{query_string}"