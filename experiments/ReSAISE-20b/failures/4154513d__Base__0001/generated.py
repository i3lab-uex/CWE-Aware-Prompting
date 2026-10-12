import urllib.parse

# Domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "auth.example.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The SSO service endpoint URL.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which users should be returned after authentication.

    Returns
    -------
    str
        The complete redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL and validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be an absolute URL")

    # Extract the hostname (domain) and compare against allowed list
    domain = parsed_redirect.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for redirect URLs")

    # Encode query parameters safely
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Combine the auth endpoint with encoded query parameters
    if urllib.parse.urlparse(auth_endpoint).scheme == "":
        raise ValueError("auth_endpoint must be an absolute URL")

    redirect = f"{auth_endpoint.rstrip('?')}"
    if '?' in auth_endpoint:
        # Append parameters to existing query string
        redirect = f"{auth_endpoint}&{encoded_query}"
    else:
        redirect = f"{redirect}?{encoded_query}"

    return redirect