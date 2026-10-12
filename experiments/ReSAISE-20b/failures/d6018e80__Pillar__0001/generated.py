import urllib.parse
from typing import Set

# Domains that are allowed for the return URL.  Update this set as needed.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "myapp.org"}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        Full SSO redirect URL containing the user ID and return URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL's domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect URL: missing scheme or netloc")

    # Extract the domain (host) part; strip any port
    host = parsed_redirect.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{host}' is not allowed")

    # Build the query parameters safely
    params = {
        "uid": uid,
        "return_url": redirect_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Construct the final URL
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Preserve existing query parameters in sso_url, if any
    existing_query = parsed_sso.query
    combined_query = urllib.parse.urlencode(
        dict(urllib.parse.parse_qsl(existing_query)) | params
    )
    sso_redirect = urllib.parse.urlunparse(
        parsed_sso._replace(query=combined_query)
    )
    return sso_redirect