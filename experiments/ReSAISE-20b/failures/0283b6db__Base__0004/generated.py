import urllib.parse

# Domains that are considered safe for redirects.
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedpartner.org"}

def _is_allowed_domain(url: str) -> bool:
    """
    Return True if the netloc of *url* ends with one of the allowed domains.
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False

    # Empty netloc or scheme is not allowed
    if not parsed.netloc or not parsed.scheme:
        return False

    # Normalize domain to lower case for comparison
    host = parsed.hostname.lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_RETURN_DOMAINS)

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and a safe return URL.

    Parameters
    ----------
    sso_endpoint : str
        Base endpoint of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back to after authentication.

    Returns
    -------
    str
        Fully formed SSO redirect URL.

    Raises
    ------
    ValueError
        If *return_url* does not belong to an allowed domain.
    """
    if not _is_allowed_domain(return_url):
        raise ValueError("Return URL domain is not allowed")

    # Prepare query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,  # Let urlencode handle proper escaping
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the base endpoint does not already contain a query
    parsed_base = urllib.parse.urlparse(sso_endpoint)
    if parsed_base.query:
        raise ValueError("SSO endpoint must not contain query parameters")

    # Build final URL
    redirect_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            parsed_base.path,
            "",  # params
            query_string,
            "",  # fragment
        )
    )

    return redirect_url