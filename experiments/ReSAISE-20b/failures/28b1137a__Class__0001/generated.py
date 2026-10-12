import urllib.parse

# Whitelisted domains for the redirect URL (example values)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "secure.service.net",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and a return URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL (may already contain query parameters).
    uid : str
        Unique user identifier to be passed to the identity provider.
    redirect_url : str
        The URL to return to after successful SSO.

    Returns
    -------
    str
        A fully-formed URL ready for redirection.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    host = parsed_redirect.hostname

    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect URL domain '{host}' is not allowed")

    # Prepare query parameters
    params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }

    # Parse the SSO path to merge existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_path)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query))
    merged_params = {**existing_params, **params}

    # Build the final URL
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    sso_url_parts = parsed_sso._replace(query=new_query)

    return urllib.parse.urlunparse(sso_url_parts)