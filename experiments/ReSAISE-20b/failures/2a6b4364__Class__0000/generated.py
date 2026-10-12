import urllib.parse

# Domains considered safe for redirection.
ALLOWED_DOMAINS = ["example.com", "trusted.com"]


def _is_safe_url(url: str, base_netloc: str) -> bool:
    """
    Determine whether the given URL is safe for redirection.

    A URL is considered safe if:
      * It has no scheme or its scheme is http/https.
      * Its netloc (domain) matches the base domain, or
        it is in ALLOWED_DOMAINS.
    """
    parsed = urllib.parse.urlparse(url)

    # If the URL is relative, it's safe by definition.
    if not parsed.scheme and not parsed.netloc:
        return True

    # Allow only http/https schemes.
    if parsed.scheme not in {"http", "https"}:
        return False

    # If the netloc matches the base, it's safe.
    if parsed.netloc == base_netloc:
        return True

    # Otherwise, it must be in the allowed domains list.
    host = parsed.hostname
    return host in ALLOWED_DOMAINS


def create_redirect_url(base_url: str, next_param: str | None) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://app.example.com/").
    next_param : str | None
        The user-provided 'next' parameter, which may be relative or absolute.

    Returns
    -------
    str
        The final redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same domain or an allowed external domain.
    """
    if next_param is None:
        # Default to the base URL if no redirect target is supplied.
        return base_url

    # Resolve next_param against the base URL to get an absolute URL.
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse the base URL to extract its netloc for comparison.
    base_parsed = urllib.parse.urlparse(base_url)
    base_netloc = base_parsed.netloc

    # Validate the resolved URL.
    if not _is_safe_url(resolved, base_netloc):
        raise ValueError(f"Unsafe redirect target: {resolved}")

    return resolved