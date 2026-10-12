import urllib.parse

# Example allowed domains; replace with your real list.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def _extract_domain(url: str) -> str:
    """
    Extracts the domain part (netloc) from a URL.
    Handles URLs with or without scheme and ignores ports.
    """
    parsed = urllib.parse.urlparse(url)
    # If scheme missing, urlparse treats entire string as path; prepend dummy scheme.
    if not parsed.scheme:
        parsed = urllib.parse.urlparse("https://" + url)
    # Lowercase domain for comparison
    return parsed.hostname.lower() if parsed.hostname else ""

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Builds a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service.
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to return to after SSO completion.

    Returns
    -------
    str
        Fully-qualified SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate redirect URL domain
    domain = _extract_domain(redirect_url)
    if not domain or domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters
    params = {
        "uid": uid,
        "redirect_uri": redirect_url,  # let the SSO service handle encoding
    }
    query = urllib.parse.urlencode(params, safe="/:?=&")

    # Construct final URL
    return f"{sso_url.rstrip('?&')}?{query}"