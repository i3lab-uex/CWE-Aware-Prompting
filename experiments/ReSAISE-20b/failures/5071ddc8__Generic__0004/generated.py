import urllib.parse

# List of external domains that are allowed for redirection.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URI after login.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_route : str
        The target URL or path the user wants to reach after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe – i.e. it points to a domain that is not
        the same as the base URL and not in ``ALLOWED_DOMAINS``.
    """
    # Parse the base URL once
    base_parts = urllib.parse.urlparse(main_base_url)

    # Resolve the target route against the base URL
    resolved = urllib.parse.urljoin(main_base_url, next_route)

    # Parse the resolved URL to examine its components
    parsed = urllib.parse.urlparse(resolved)

    # Ensure the scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # If the netloc (domain) is empty, it means ``next_route`` was a relative
    # path and the result inherits the base domain – this is safe.
    if not parsed.netloc:
        return resolved

    # If the domain matches the base domain, it's safe
    if parsed.netloc.lower() == base_parts.netloc.lower():
        return resolved

    # Otherwise, the domain must be in ALLOWED_DOMAINS
    host = parsed.netloc.split(":")[0].lower()  # strip optional port
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect to external domain '{host}' is not allowed")

    return resolved