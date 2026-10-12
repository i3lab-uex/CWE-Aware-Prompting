import urllib.parse

# Set of domains that are permitted as return URLs
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.com",
    # Add other trusted domains here
}

def _is_allowed_domain(url: str) -> bool:
    """
    Verify that the domain of `url` is in ALLOWED_RETURN_DOMAINS.
    Subdomains are allowed only if explicitly listed.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.hostname or ""
        # Normalize to lowercase for comparison
        return domain.lower() in ALLOWED_RETURN_DOMAINS
    except Exception:
        return False

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the SSO service should redirect after authentication.

    Returns
    -------
    str
        A fully-qualified URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If `redirect_url` does not point to an allowed domain.
    """
    # Validate the return URL domain
    if not _is_allowed_domain(redirect_url):
        raise ValueError(f"Return URL domain is not allowed: {redirect_url}")

    # Build query parameters safely
    params = {
        "uid": uid,
        "return_url": redirect_url
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&")  # Allow typical URL characters

    # Combine base SSO URL with query string
    if urllib.parse.urlparse(sso_url).query:
        # If sso_url already contains query parameters, append with &
        separator = "&"
    else:
        separator = "?"
    return f"{sso_url}{separator}{query_string}"