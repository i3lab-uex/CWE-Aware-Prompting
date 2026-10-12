import urllib.parse
from typing import Set

# Example whitelist – replace with the actual allowed domains for your application.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # add more domains as needed
}


def _is_allowed_domain(url: str) -> bool:
    """
    Check whether the domain of a URL is in ALLOWED_RETURN_DOMAINS.
    The comparison is case‑insensitive and allows subdomains if the
    domain ends with an allowed entry (e.g. foo.example.com is accepted
    when example.com is whitelisted).
    """
    parsed = urllib.parse.urlparse(url)
    domain = parsed.hostname
    if not domain:
        return False

    domain = domain.lower()
    for allowed in ALLOWED_RETURN_DOMAINS:
        allowed = allowed.lower()
        if domain == allowed or domain.endswith("." + allowed):
            return True
    return False


def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint URL (may already contain query parameters).
    uid : str
        Unique user identifier to be passed to the identity provider.
    redirect_url : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If ``redirect_url``'s domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    if not _is_allowed_domain(redirect_url):
        raise ValueError(
            f"Redirect URL domain is not allowed: {urllib.parse.urlparse(redirect_url).hostname}"
        )

    # Parse the base auth endpoint and its existing query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    auth_query = dict(urllib.parse.parse_qsl(parsed_auth.query))

    # Add/override the required parameters
    auth_query.update(
        {
            "uid": uid,
            "redirect": redirect_url,
        }
    )

    # Rebuild the full URL
    new_query = urllib.parse.urlencode(auth_query)
    sso_url_parts = parsed_auth._replace(query=new_query)

    return urllib.parse.urlunparse(sso_url_parts)