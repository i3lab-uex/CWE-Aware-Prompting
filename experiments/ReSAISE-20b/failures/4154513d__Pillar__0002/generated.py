import urllib.parse

# Example allowed domains; in real use these should be configured securely.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "app.company.net",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider's authentication endpoint.
    uid : str
        Unique identifier for the user to be authenticated.
    redirect_url : str
        The URL to which the provider should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that the client can redirect to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL to validate its domain.
    parsed_return = urllib.parse.urlparse(redirect_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Redirect URL must be a full, valid URL.")

    # Normalize the domain (lowercase and strip port if present).
    netloc = parsed_return.netloc.split(":")[0].lower()
    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{netloc}' is not allowed.")

    # Build the query parameters for the SSO endpoint.
    params = {
        "uid": uid,
        # The provider expects a URL-encoded redirect URI.
        "redirect_uri": redirect_url
    }
    query = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")

    # Ensure the auth endpoint ends with a slash or question mark appropriately.
    if urllib.parse.urlparse(auth_endpoint).scheme == "":
        raise ValueError("auth_endpoint must be a full URL with scheme (e.g., https://).")

    # Construct the final redirect URL.
    redirect = f"{auth_endpoint.rstrip('/')}/?{query}" if "?" not in auth_endpoint else f"{auth_endpoint}&{query}"
    return redirect