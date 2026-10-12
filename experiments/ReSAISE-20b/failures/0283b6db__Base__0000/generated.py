import urllib.parse

# Domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add other trusted domains here
}

def _is_allowed_domain(url: str) -> bool:
    """
    Validate that the URL belongs to an allowed domain.
    Returns True if valid, False otherwise.
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False

    # Must be an absolute URL with http or https scheme
    if parsed.scheme not in ("http", "https"):
        return False

    host = parsed.hostname
    if not host:
        return False

    # Check exact match or subdomain of an allowed domain
    for allowed in ALLOWED_RETURN_DOMAINS:
        if host == allowed or host.endswith("." + allowed):
            return True
    return False

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back to after authentication.

    Returns
    -------
    str
        The complete SSO redirect URL with encoded parameters.

    Raises
    ------
    ValueError
        If ``return_url`` does not belong to an allowed domain.
    """
    if not _is_allowed_domain(return_url):
        raise ValueError(f"Return URL domain is not allowed: {return_url}")

    # Build query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the endpoint does not already contain a query string
    if urllib.parse.urlparse(sso_endpoint).query:
        raise ValueError("SSO endpoint must not contain a query string")

    # Construct the full redirect URL
    return f"{sso_endpoint}?{query_string}"