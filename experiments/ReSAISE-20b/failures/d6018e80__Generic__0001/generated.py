import urllib.parse

# Set of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a single‑sign‑on redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        Full URL that the user should be sent to for SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    domain = parsed_redirect.hostname
    if not domain or domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Parse the base SSO URL and preserve any existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_url)
    sso_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))

    # Add/override the required parameters.
    sso_query.update({
        "uid": uid,
        "redirect_url": redirect_url
    })

    # Reconstruct the SSO URL with updated query string.
    new_query = urllib.parse.urlencode(sso_query, doseq=True)
    sso_url_with_params = parsed_sso._replace(query=new_query)

    return urllib.parse.urlunparse(sso_url_with_params)