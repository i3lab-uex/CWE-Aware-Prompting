import urllib.parse

# Set of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully-formed SSO redirect URL including the user ID and encoded return URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain.
    parsed_return = urllib.parse.urlparse(redirect_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Redirect URL must be a valid absolute URL")

    # Extract the domain (hostname) and normalize it.
    return_domain = parsed_return.hostname
    if return_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{return_domain}' is not allowed")

    # Encode query parameters safely.
    params = {
        "uid": uid,
        "return_url": redirect_url,  # this will be percent‑encoded by urlencode
    }
    query_string = urllib.parse.urlencode(params, safe="")

    # Parse the base SSO URL to merge with our query string.
    parsed_sso = urllib.parse.urlparse(sso_url)

    # Build the new URL with the added query parameters.
    sso_parts = parsed_sso._replace(query=query_string)
    final_url = urllib.parse.urlunparse(sso_parts)

    return final_url