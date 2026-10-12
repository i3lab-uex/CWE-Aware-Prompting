import urllib.parse

# Allowed domains for the return URL. Adjust as needed.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trustedpartner.org",
}

def _is_allowed_domain(url: str) -> bool:
    """
    Check whether the domain of *url* is in ALLOWED_RETURN_DOMAINS.
    The check allows subdomains of the allowed domains but rejects
    any other host.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        # Reject URLs without a scheme or netloc
        if not parsed.scheme or not parsed.netloc:
            return False

        # Extract the hostname (without port)
        host = parsed.hostname
        if not host:
            return False

        # Compare against allowed domains (case‑insensitive)
        host = host.lower()
        for domain in ALLOWED_RETURN_DOMAINS:
            if host == domain or host.endswith("." + domain):
                return True
        return False
    except Exception:
        # Any parsing error should be treated as disallowed
        return False


def generate_sso_redirect(
    sso_endpoint: str,
    user_id: str,
    return_url: str
) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        Base endpoint of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to which the SSO service should redirect after authentication.

    Returns
    -------
    str
        The full URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If *return_url* does not belong to an allowed domain.
    """
    if not _is_allowed_domain(return_url):
        raise ValueError("Return URL domain is not allowed")

    # Build query parameters safely
    params = {
        "user_id": user_id,
        "return_url": return_url,   # The SSO service will URL‑encode this internally
    }
    query_string = urllib.parse.urlencode(params)

    # Combine the endpoint and query string
    if "?" in sso_endpoint:
        separator = "&"
    else:
        separator = "?"

    return f"{sso_endpoint}{separator}{query_string}"