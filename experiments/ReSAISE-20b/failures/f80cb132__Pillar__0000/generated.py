import urllib.parse

# List of fully qualified domains that are allowed for external redirects.
APPROVED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "safe-site.net",
}

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL against an approved domain list and
    return the original URL if it is safe.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by a user.

    Returns
    -------
    str
        The validated, safe‑to‑use URL.

    Raises
    ------
    ValueError
        If the URL is not absolute, or its domain is not in APPROVED_DOMAINS.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(url_input)

    # Ensure the scheme is HTTP or HTTPS and that we have a netloc
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be absolute and use http/https scheme")

    # Extract host without port
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check against the approved domain list
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Re‑assemble the URL to ensure it hasn't been tampered with
    safe_url = urllib.parse.urlunparse(parsed)

    return safe_url