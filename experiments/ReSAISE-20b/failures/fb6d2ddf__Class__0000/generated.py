import urllib.parse
from typing import Set

# Whitelist of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "app.example.org"}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO endpoint to which the user will be redirected.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Destination URL to return to after successful authentication.

    Returns
    -------
    str
        A fully constructed SSO redirect URL with the user ID and encoded return URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Normalize the domain (remove port, lowercase).
    domain = parsed_redirect.hostname.lower() if parsed_redirect.hostname else ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Prepare query parameters for the SSO endpoint.
    params = {
        "uid": uid,
        # The redirect URL must be percent‑encoded to avoid injection attacks.
        "redirect_url": urllib.parse.quote(redirect_url, safe=""),
    }
    query_string = urllib.parse.urlencode(params)

    # Build the final SSO URL.
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        raise ValueError("auth_endpoint must be a valid absolute URL")

    # Preserve existing query parameters on the auth endpoint.
    existing_query = parsed_auth.query
    combined_query = urllib.parse.urljoin(
        f"{existing_query}&{query_string}" if existing_query else query_string, ""
    )

    sso_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        combined_query,
        "",  # fragment
    )
    return urllib.parse.urlunparse(sso_url_parts)