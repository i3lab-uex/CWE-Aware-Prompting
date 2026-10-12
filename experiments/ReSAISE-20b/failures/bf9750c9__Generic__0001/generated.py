import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted.co",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base URI of the SSO provider.
    user_identifier : str
        Unique identifier for the user to be authenticated.
    redirect_link : str
        URL where the user should land after authentication.

    Returns
    -------
    str
        The fully formed SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect link to validate its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a full URL with scheme and host")

    # Extract the hostname (domain) for validation.
    domain = parsed_redirect.hostname
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for redirect URLs")

    # Ensure the SSO URI has a scheme and netloc.
    parsed_sso = urllib.parse.urlparse(sso_uri)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("sso_uri must be a full URL with scheme and host")

    # Build query parameters.
    params = {
        "user_id": user_identifier,
        "redirect_url": redirect_link,
    }
    query = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")  # allow URL-safe characters

    # Construct the final URL preserving existing components of sso_uri.
    new_parts = (
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path or "",
        parsed_sso.params,
        query,          # replace existing query with our parameters
        parsed_sso.fragment,
    )
    return urllib.parse.urlunparse(new_parts)