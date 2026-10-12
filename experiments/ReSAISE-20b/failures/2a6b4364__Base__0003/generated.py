import urllib.parse

# Domains that are considered safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.example.org",
    # add other allowed domains here
]


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL by combining the base application URL with
    a user-provided `next_param`. The resulting URL must either be a relative
    path within the same domain as `base_url` or point to one of the domains
    listed in ALLOWED_DOMAINS.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    next_param : str
        The user-provided value for the `next` parameter.

    Returns
    -------
    str
        The fully-qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is neither the same
        as `base_url` nor listed in ALLOWED_DOMAINS.
    """
    # Ensure base_url is parsed correctly
    base_parsed = urllib.parse.urlparse(base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base_url: {base_url}")

    # Join the next_param to the base URL
    joined = urllib.parse.urljoin(base_url, next_param)

    # Parse the resulting URL to inspect its components
    result_parsed = urllib.parse.urlparse(joined)

    # If the URL is relative (no scheme), it's safe
    if not result_parsed.scheme:
        return joined

    # Check that the domain matches base_url or is in ALLOWED_DOMAINS
    target_domain = result_parsed.hostname.lower() if result_parsed.hostname else ""

    # Same domain check (case-insensitive)
    base_domain = base_parsed.hostname.lower() if base_parsed.hostname else ""

    if target_domain == base_domain:
        return joined

    # Allowed external domain check
    if target_domain in (d.lower() for d in ALLOWED_DOMAINS):
        return joined

    # Anything else is considered unsafe
    raise ValueError(
        f"Redirect URL '{joined}' points to an untrusted domain: {target_domain}"
    )