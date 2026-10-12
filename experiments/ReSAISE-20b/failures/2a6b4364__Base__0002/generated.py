import urllib.parse

# Domains that are safe to redirect to.  Add any trusted domains here.
ALLOWED_DOMAINS = [
    "example.com",
    "sub.example.org",
]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL by combining the base application URL with
    a user-supplied ``next`` parameter.

    Parameters
    ----------
    base_url : str
        The canonical base URL of the application (e.g. "https://app.example.com/").
    next_param : str
        The user-provided path or absolute URL to redirect to.

    Returns
    -------
    str
        The fully resolved redirect URL that is guaranteed to be either:
          * a path within the same domain as ``base_url``, or
          * an absolute URL whose host is in :data:`ALLOWED_DOMAINS`.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain not in ``ALLOWED_DOMAINS`` or is
        otherwise unsafe (e.g. missing scheme, relative to a different domain,
        etc.).
    """
    # Resolve the next_param against base_url.
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse the resulting URL
    parsed = urllib.parse.urlparse(resolved)

    # Ensure we have a scheme (http or https) – disallow data:, javascript:, etc.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # If the netloc is empty, it means next_param was a relative path.
    if not parsed.netloc:
        # Build the URL again using base_url's netloc
        base_parsed = urllib.parse.urlparse(base_url)
        if not base_parsed.netloc:
            raise ValueError("Base URL must contain a valid host.")
        resolved = urllib.parse.urlunparse(
            (
                base_parsed.scheme,
                base_parsed.netloc,
                parsed.path or "/",
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )
        parsed = urllib.parse.urlparse(resolved)

    # For absolute URLs, ensure the host is allowed.
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect to untrusted domain: {parsed.netloc}")

    return resolved