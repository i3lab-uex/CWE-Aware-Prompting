import urllib.parse

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trustedpartner.net",
}

def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base SSO endpoint (e.g. "https://sso.example.com/login").
    user_identifier : str
        Unique identifier of the user (e.g. a UUID or username).
    redirect_link : str
        The URL to which the user should be sent after successful SSO.

    Returns
    -------
    str
        A fully constructed URL that can be sent to the browser.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect link to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be a valid absolute URL")

    # Normalise the domain to compare against the whitelist.
    redirect_domain = parsed_redirect.hostname.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{redirect_domain}' is not allowed for SSO"
        )

    # Build the query parameters. We encode the redirect link to avoid
    # injection or malformed URLs.
    params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_link,
    }
    encoded_params = urllib.parse.urlencode(params, safe=":/?&=")

    # Ensure the base SSO URI ends with a slash or query separator.
    if urllib.parse.urlparse(sso_uri).scheme not in ("http", "https"):
        raise ValueError("sso_uri must be an absolute HTTP/HTTPS URL")

    # Append the query string to the SSO endpoint.
    if urllib.parse.urlparse(sso_uri).query:
        # If sso_uri already contains a query string, append with '&'
        full_url = f"{sso_uri}&{encoded_params}"
    else:
        full_url = f"{sso_uri}?{encoded_params}"

    return full_url