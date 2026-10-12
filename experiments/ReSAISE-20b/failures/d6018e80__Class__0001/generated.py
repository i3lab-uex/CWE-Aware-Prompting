import urllib.parse
from typing import Set

# Domains that are allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "sub.example.org"}

def _is_allowed_domain(url: str) -> bool:
    """
    Check if the hostname of *url* belongs to ALLOWED_RETURN_DOMAINS.
    The comparison is case‑insensitive and ignores port numbers.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        # Normalize to lower case for comparison.
        hostname = hostname.lower()
        # Allow subdomains that exactly match an allowed domain
        return any(
            hostname == domain or hostname.endswith(f".{domain}") for domain in ALLOWED_RETURN_DOMAINS
        )
    except Exception:
        return False

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to return to after SSO authentication.

    Returns
    -------
    str
        Fully constructed redirect URL pointing at the SSO service.

    Raises
    ------
    ValueError
        If *redirect_url* does not belong to an allowed domain.
    """
    # Validate the return URL's domain
    if not _is_allowed_domain(redirect_url):
        raise ValueError("Return URL domain is not allowed")

    # Encode query parameters
    params = {
        "uid": uid,
        "redirect": redirect_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&")

    # Combine base SSO URL with the query string
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Preserve any existing query parameters in sso_url
    base_query = parsed_sso.query
    if base_query:
        full_query = f"{base_query}&{query_string}"
    else:
        full_query = query_string

    # Reconstruct the URL
    new_url = urllib.parse.urlunparse(
        parsed_sso._replace(query=full_query)
    )
    return new_url