import urllib.parse

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more trusted domains here.
}

def _extract_domain(url: str) -> str:
    """
    Extract the hostname (domain) from a URL.
    Normalizes the domain by converting to lowercase and stripping any port number.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    return hostname.lower()


def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base endpoint for the SSO provider (e.g. "https://sso.example.com/auth").
    uid : str
        The unique identifier for the user.
    redirect_url : str
        The URL to which the SSO provider should return after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user to the SSO provider.

    Raises
    ------
    ValueError
        If ``redirect_url``'s domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain.
    domain = _extract_domain(redirect_url)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{domain}' is not in the list of allowed domains."
        )

    # Build query parameters. Use ``urllib.parse.quote_plus`` to escape values.
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote_plus)

    # Ensure the SSO path is absolute; if not, raise an error.
    parsed_sso = urllib.parse.urlparse(sso_path)
    if not (parsed_sso.scheme and parsed_sso.netloc):
        raise ValueError(f"SSO path must be an absolute URL: {sso_path!r}")

    # Combine the base SSO path with the query string.
    # ``urljoin`` preserves existing query components if present.
    base_url = urllib.parse.urlunparse(parsed_sso._replace(query=""))
    full_url = f"{base_url}?{encoded_params}"

    return full_url