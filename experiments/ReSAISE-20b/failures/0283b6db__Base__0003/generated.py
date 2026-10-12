import urllib.parse

# Allowed domains for the return URL (example)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
}

def _is_allowed_domain(return_url: str) -> bool:
    """
    Check whether the return URL's domain is in ALLOWED_RETURN_DOMAINS.
    Subdomains are allowed only if explicitly listed.
    """
    parsed = urllib.parse.urlparse(return_url)
    # Reject URLs without scheme or netloc
    if not parsed.scheme or not parsed.netloc:
        return False

    # Ensure the scheme is HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        return False

    # Normalize the domain (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""
    return host in ALLOWED_RETURN_DOMAINS


def generate_sso_redirect(
    sso_endpoint: str, user_id: str, return_url: str
) -> str:
    """
    Generate a Single Sign-On redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        The user's unique identifier.
    return_url : str
        The URL to redirect back after SSO.

    Returns
    -------
    str
        The full SSO redirect URL with encoded query parameters.

    Raises
    ------
    ValueError
        If the return_url is not from an allowed domain.
    """
    if not _is_allowed_domain(return_url):
        raise ValueError("Return URL domain is not allowed")

    # Build query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query = urllib.parse.urlencode(params)

    # Join the base endpoint with the query string
    # If sso_endpoint already contains a query, we append parameters appropriately.
    parsed_sso = urllib.parse.urlparse(sso_endpoint)
    if parsed_sso.query:
        # Merge existing query parameters
        existing = dict(urllib.parse.parse_qsl(parsed_sso.query))
        merged_params = {**existing, **params}
        query = urllib.parse.urlencode(merged_params)

    # Reconstruct the full URL
    new_url_parts = parsed_sso._replace(query=query)
    return urllib.parse.urlunparse(new_url_parts)