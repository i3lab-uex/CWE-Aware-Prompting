import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trustedpartner.net",
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider (may contain existing query parameters).
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        Fully formed SSO URL containing the user ID and encoded redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Validate the domain against the whitelist.
    redirect_domain = parsed_redirect.netloc.split(':')[0]  # ignore port
    if redirect_domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{redirect_domain}' is not allowed for redirect_url")

    # Encode the redirect URL as a query parameter value.
    encoded_redirect = urllib.parse.quote(redirect_url, safe="")

    # Build the query parameters for the SSO request.
    sso_params = {
        "uid": uid,
        "redirect_url": encoded_redirect,
    }
    query_string = urllib.parse.urlencode(sso_params)

    # Parse the auth endpoint to preserve any existing query parameters.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Merge existing query with new SSO parameters.
    if parsed_auth.query:
        merged_query = f"{parsed_auth.query}&{query_string}"
    else:
        merged_query = query_string

    # Reconstruct the full SSO URL.
    sso_url_parts = parsed_auth._replace(query=merged_query)
    full_sso_url = urllib.parse.urlunparse(sso_url_parts)

    return full_sso_url