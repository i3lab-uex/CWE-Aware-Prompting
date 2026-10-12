import urllib.parse

# List of external domains considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a secure redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        Path or full URL where the user wants to go after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Normalise and parse the base URL
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base URL: {domain_base_url}")

    # If next_redirect_param is empty or None, return the base URL
    if not next_redirect_param:
        return domain_base_url.rstrip('/')

    # Resolve the target URL
    resolved = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the target URL has no scheme/netloc, it is a relative path – safe.
    if not target_parsed.scheme and not target_parsed.netloc:
        return resolved

    # For absolute URLs, ensure the host is either the same as base or in ALLOWED_DOMAINS
    target_host = target_parsed.netloc.lower()
    base_host = base_parsed.netloc.lower()

    if target_host == base_host:
        # Same host – safe
        return resolved

    # Check if the target host is in the list of allowed external domains
    for domain in ALLOWED_DOMAINS:
        if target_host == domain.lower() or target_host.endswith("." + domain.lower()):
            return resolved

    # If we reach here, the redirect target is not allowed
    raise ValueError(
        f"Redirect to {resolved} is disallowed: host '{target_host}' not in allowed domains."
    )