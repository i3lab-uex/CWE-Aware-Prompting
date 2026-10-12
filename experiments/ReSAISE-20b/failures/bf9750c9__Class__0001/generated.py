import urllib.parse

# Whitelist of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "mycompany.co.uk",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base URI of the SSO provider (e.g., "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or username).
    redirect_link : str
        Absolute URL to which the user should be redirected after authentication.

    Returns
    -------
    str
        A fully-formed SSO redirect URL containing the user identifier and
        return destination.

    Raises
    ------
    ValueError
        If the redirect_link domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate that redirect_link has a scheme and netloc
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError("redirect_link must be a fully-qualified URL")

    # Extract domain and compare against whitelist
    redirect_domain = parsed_redirect.hostname.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{redirect_domain}' is not allowed")

    # Validate the base SSO URI
    parsed_sso = urllib.parse.urlparse(sso_uri)
    if not (parsed_sso.scheme and parsed_sso.netloc):
        raise ValueError("sso_uri must be a fully-qualified URL")

    # Build query parameters safely
    params = {
        "user": user_identifier,
        "redirect": redirect_link,  # Let urlencode handle proper quoting
    }
    query_string = urllib.parse.urlencode(params)

    # Reconstruct the final URL preserving existing path/query of sso_uri
    new_sso = parsed_sso._replace(query=query_string)
    final_url = urllib.parse.urlunparse(new_sso)

    return final_url