import urllib.parse

# Domains that are allowed for the return URL.  These should be whitelisted
# by your application to prevent open redirect attacks (CWE‑610).
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trustedpartner.net",
}

def _is_allowed_return_url(return_url: str) -> bool:
    """
    Verify that the return URL's domain is in ALLOWED_RETURN_DOMAINS.
    """
    try:
        parsed = urllib.parse.urlparse(return_url)
        domain = parsed.hostname
        if not domain:
            return False
        # Allow subdomains only if explicitly listed
        return domain in ALLOWED_RETURN_DOMAINS or any(
            domain.endswith(f".{allowed}") for allowed in ALLOWED_RETURN_DOMAINS
        )
    except Exception:
        return False

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        Base endpoint of the SSO provider.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back to after successful SSO.

    Returns
    -------
    str
        A fully constructed, URL‑encoded redirect URL.

    Raises
    ------
    ValueError
        If ``return_url`` is not from an allowed domain.
    """
    if not _is_allowed_return_url(return_url):
        raise ValueError("Return URL domain is not allowed.")

    # Build query parameters safely
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/")  # preserve :// in return_url

    # Ensure the endpoint ends with a slash for proper joining
    base = sso_endpoint.rstrip("/") + "/"

    return urllib.parse.urljoin(base, f"?{query_string}")