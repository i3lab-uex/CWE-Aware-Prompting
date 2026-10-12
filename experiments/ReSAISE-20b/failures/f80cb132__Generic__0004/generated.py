import urllib.parse

# Pre‑approved external domains (exact match, no subdomains)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.net"
}

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL against a whitelist of approved domains.

    Parameters
    ----------
    url_input : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original URL if it is safe to use for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https,
        or its domain is not in APPROVED_DOMAINS.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(url_input)

    # Basic scheme check – only http or https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    # Extract the network location part (domain + optional port)
    netloc = parsed.hostname
    if not netloc:
        raise ValueError("URL must contain a valid domain")

    # Normalize the hostname (lowercase)
    netloc = netloc.lower()

    # Verify that the domain is exactly one of the approved ones
    if netloc not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not approved for redirection")

    # Rebuild the URL to ensure it is in a canonical form
    safe_url = urllib.parse.urlunparse(parsed._replace(path=urllib.parse.quote_plus(parsed.path)))

    return safe_url