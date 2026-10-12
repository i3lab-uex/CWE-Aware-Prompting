import urllib.parse

# Whitelist of allowed return domains
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "localhost",  # for local testing
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base URI of the SSO provider.
    user_identifier : str
        Unique identifier for the user (e.g., username or UUID).
    redirect_link : str
        Absolute URL to return to after authentication.

    Returns
    -------
    str
        Fully qualified SSO redirect URL containing the user identifier and
        encoded return link.

    Raises
    ------
    ValueError
        If the redirect_link's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate that the redirect_link is absolute
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_link must be an absolute URL")

    # Extract the domain (netloc) and compare against whitelist
    redirect_domain = parsed_redirect.hostname or ""
    if redirect_domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{redirect_domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Parse the SSO URI to manipulate its query parameters
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Build the new query parameters
    sso_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    sso_query["user"] = user_identifier
    # The return URL must be encoded as a single parameter value
    sso_query["return"] = redirect_link

    # Construct the updated query string
    new_query = urllib.parse.urlencode(sso_query, doseq=True)

    # Rebuild the full SSO URL
    new_sso = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(new_sso)