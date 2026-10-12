import urllib.parse

# Domains that are allowed to receive the SSO redirect back.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add more allowed domains here
}

def _extract_domain(url: str) -> str:
    """
    Return the hostname part of a URL (without port).
    Raises ValueError if the URL is malformed.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Invalid URL: {url!r}")
    return host.lower()

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        Absolute URL to which the SSO service should redirect after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL domain to mitigate CWE‑610 (open redirect)
    redirect_domain = _extract_domain(redirect_url)
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{redirect_domain}' is not allowed "
            f"(allowed: {sorted(ALLOWED_RETURN_DOMAINS)})"
        )

    # Build query parameters
    params = {
        "uid": uid,
        "redirect": redirect_url,  # The SSO service will URL‑decode this
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the base SSO URL ends with a slash if needed
    sso_base = sso_url.rstrip("/")
    # Combine the base URL with the query string
    full_url = f"{sso_base}?{query_string}"
    return full_url