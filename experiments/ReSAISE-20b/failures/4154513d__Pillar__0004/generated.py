import urllib.parse

# Set of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedsite.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service endpoint.
    uid : str
        The unique identifier for the user.
    redirect_url : str
        The URL to which users should be returned after authentication.

    Returns
    -------
    str
        A fully formed redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    domain = parsed_redirect.hostname

    if not domain or domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(
            f"Return URL domain '{domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters safely.
    query_params = {
        "uid": uid,
        "redirect": redirect_url
    }
    encoded_query = urllib.parse.urlencode(query_params)

    # Combine the auth endpoint with query string.
    return f"{auth_endpoint}?{encoded_query}"