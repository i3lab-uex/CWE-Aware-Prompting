import urllib.parse

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "mycompany.co.uk",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint URL.
    uid : str
        Unique user identifier to be passed to the IdP.
    redirect_url : str
        The URL where the user should be sent after successful authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL containing the uid and a
        percent‑encoded return URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not present in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect URL: {redirect_url!r}")

    # Extract the hostname (excluding port)
    hostname = parsed_redirect.hostname
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters for the SSO request
    params = {
        "uid": uid,
        # The redirect URL must be percent‑encoded so that it can safely travel
        # through the IdP without being altered.
        "redirect": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(params, doseq=True)

    # Combine the base endpoint with the query string
    # Ensure we handle cases where auth_endpoint may already contain a query part.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Preserve any existing query parameters in the auth endpoint
    if parsed_auth.query:
        new_query = f"{parsed_auth.query}&{encoded_params}"
    else:
        new_query = encoded_params

    sso_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        new_query,
        parsed_auth.fragment,
    )
    sso_url = urllib.parse.urlunparse(sso_url_parts)

    return sso_url