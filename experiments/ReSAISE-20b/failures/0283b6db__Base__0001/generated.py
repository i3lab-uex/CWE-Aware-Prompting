import urllib.parse

# Domains that are permitted to be used as a return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net",
}


def _is_allowed_return_url(return_url: str) -> bool:
    """
    Validate that the return URL belongs to one of the allowed domains.
    The check is case‑insensitive and allows subdomains only if they
    explicitly appear in ALLOWED_RETURN_DOMAINS.
    """
    try:
        parsed = urllib.parse.urlparse(return_url)
    except Exception:
        return False

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        return False

    # Extract the host (netloc may include port)
    host = parsed.hostname
    if not host:
        return False

    # Normalize to lowercase for comparison
    host = host.lower()

    # Direct match or subdomain check
    if host in ALLOWED_RETURN_DOMAINS:
        return True

    # Allow subdomains only if the parent domain is explicitly listed
    for allowed in ALLOWED_RETURN_DOMAINS:
        if host.endswith("." + allowed.lower()):
            return True

    return False


def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        The URL to which the SSO service should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If `return_url` is not from an allowed domain.
    """
    if not _is_allowed_return_url(return_url):
        raise ValueError(f"Return URL domain is not allowed: {return_url}")

    # Build query parameters, ensuring proper encoding
    query_params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    encoded_query = urllib.parse.urlencode(query_params)

    # Construct the final URL
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    if parsed_endpoint.scheme and parsed_endpoint.netloc:
        # Use the endpoint as is, appending query
        final_url = f"{sso_endpoint.rstrip('?')}&{encoded_query}" if '?' in sso_endpoint else f"{sso_endpoint}?{encoded_query}"
    else:
        # If the endpoint is relative, join it with the current request context
        raise ValueError(f"Invalid SSO endpoint: {sso_endpoint}")

    return final_url