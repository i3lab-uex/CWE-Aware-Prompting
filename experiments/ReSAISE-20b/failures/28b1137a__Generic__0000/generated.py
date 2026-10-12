import urllib.parse

# Whitelist of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trustedsite.net",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Absolute URL to return to after authentication.

    Returns
    -------
    str
        Fully formed SSO redirect URL with the user ID and return URL encoded as query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that redirect_url is absolute and has an allowed domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Extract the domain (netloc may contain port, strip it)
    host = parsed_redirect.hostname
    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{host}' is not allowed")

    # Parse the SSO base URL and preserve its existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_path)
    qs = dict(urllib.parse.parse_qsl(parsed_sso.query))

    # Add or override the uid and redirect parameters
    qs.update({"uid": uid, "redirect": redirect_url})

    # Reconstruct the URL
    new_query = urllib.parse.urlencode(qs, doseq=True)
    sso_url_parts = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(sso_url_parts)


# Example usage:
if __name__ == "__main__":
    base_sso = "https://sso.example.com/login"
    user_id = "user123"
    return_url = "https://myapp.org/dashboard"

    try:
        url = build_sso_url(base_sso, user_id, return_url)
        print("SSO URL:", url)
    except ValueError as e:
        print("Error:", e)