import urllib.parse

# Example allowed domains; in production this would be loaded from config or env
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        Fully constructed redirect URL containing the user ID and encoded return URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URL and ensure it is absolute
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Extract the hostname and normalize it
    domain = parsed_redirect.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build the query parameters safely
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,  # will be encoded by urlencode
    }
    encoded_params = urllib.parse.urlencode(query_params, safe=":/?#[]@!$&'()*+,;=")

    # Combine with the auth endpoint
    if urllib.parse.urlparse(auth_endpoint).scheme == "":
        raise ValueError("auth_endpoint must be an absolute URL")

    # Ensure the auth endpoint ends with '?' or '&' appropriately
    separator = "&" if "?" in auth_endpoint else "?"
    return f"{auth_endpoint}{separator}{encoded_params}"