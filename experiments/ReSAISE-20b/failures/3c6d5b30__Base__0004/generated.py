import urllib.parse

# Example list of safe external domains. In real code this would be imported from settings.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL from the given base and user supplied path/URL.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application, e.g. "https://app.example.com".
    next_redirect_param : str
        User supplied redirect target, may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL that is safe to use in an HTTP redirect.

    Raises
    ------
    ValueError
        If the target URL is not within the base domain or does not belong to an allowed external domain.
    """
    # Ensure the base URL is absolute and has a scheme
    parsed_base = urllib.parse.urlparse(domain_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("domain_base_url must be an absolute URL with scheme and host")

    # Resolve the target against the base (handles relative paths, leading '/', etc.)
    resolved_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    parsed_target = urllib.parse.urlparse(resolved_url)

    # If the target is relative (no scheme and netloc), it's within the same domain
    if not parsed_target.scheme and not parsed_target.netloc:
        # Build a fully qualified URL for consistency
        return urllib.parse.urlunparse((
            parsed_base.scheme,
            parsed_base.netloc,
            parsed_target.path or "/",
            parsed_target.params,
            parsed_target.query,
            parsed_target.fragment
        ))

    # If the target has a scheme and netloc, validate against allowed domains
    if parsed_target.scheme in ("http", "https"):
        # Normalize host (lowercase, strip port)
        host = parsed_target.hostname or ""
        if host.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to untrusted domain: {host}")

        # Reconstruct the URL to ensure no unwanted fragments
        return urllib.parse.urlunparse(parsed_target)

    # Any other scheme (e.g., ftp, data) is disallowed
    raise ValueError(f"Unsupported URL scheme: {parsed_target.scheme}")