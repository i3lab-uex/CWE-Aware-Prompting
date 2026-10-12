import urllib.parse

# Domains that are allowed to be used as the redirect target.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
}

def _is_allowed_domain(hostname: str) -> bool:
    """
    Check whether the hostname ends with one of the allowed domains.
    The check is case‑insensitive and ignores leading “www.”.
    """
    if not hostname:
        return False

    # Strip any leading "www."
    hostname = hostname.lower().lstrip("www.")
    return any(hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS)

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a Single Sign‑On redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication. Must belong to an allowed domain.

    Returns
    -------
    str
        A fully formed SSO redirect URL that includes the user ID and a
        percent‑encoded return URL.

    Raises
    ------
    ValueError
        If the redirect_url's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate that the redirect URL is absolute and uses http/https
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if parsed_redirect.scheme not in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme")

    # Extract the hostname and verify it is allowed
    if not _is_allowed_domain(parsed_redirect.hostname):
        raise ValueError(f"Return URL domain '{parsed_redirect.hostname}' is not allowed")

    # Prepare query parameters for the SSO service
    sso_query = {
        "uid": uid,
        # Encode the redirect URL as a query value
        "redirect": redirect_url,
    }

    # Parse the base SSO URL to preserve any existing query params
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Merge existing query parameters with the new ones
    existing_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    merged_query = {**existing_query, **sso_query}
    encoded_query = urllib.parse.urlencode(merged_query)

    # Reconstruct the final URL
    final_url_parts = (
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        encoded_query,
        parsed_sso.fragment,
    )
    return urllib.parse.urlunparse(final_url_parts)