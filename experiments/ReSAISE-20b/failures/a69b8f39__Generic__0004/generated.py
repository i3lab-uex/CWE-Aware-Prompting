import urllib.parse

# Domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted-site.net",
}

def _extract_domain(url: str) -> str:
    """
    Extracts the domain (netloc without port) from a URL.
    Raises ValueError if the URL is malformed or has no domain.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url!r}")
    # Remove port if present
    domain = parsed.hostname or ""
    return domain.lower()


def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Builds an SSO redirect URL that points to the third‑party SSO service
    with query parameters for the user reference and return URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to redirect back to after SSO.

    Returns
    -------
    str
        Fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the return URL domain
    back_domain = _extract_domain(back_url)
    if back_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{back_domain}' is not allowed."
        )

    # Build query parameters
    params = {
        "user_ref": user_ref,
        "back_url": back_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the SSO service URL is properly parsed
    base = urllib.parse.urlparse(sso_service)
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid SSO service URL: {sso_service!r}")

    # Construct the final redirect URL
    new_url = urllib.parse.urlunparse(
        (base.scheme, base.netloc, base.path or "", "", query_string, "")
    )
    return new_url