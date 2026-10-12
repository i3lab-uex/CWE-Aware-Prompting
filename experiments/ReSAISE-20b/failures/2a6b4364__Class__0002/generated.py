import urllib.parse

# Domains considered safe for external redirection.
ALLOWED_DOMAINS = ["example.com", "trusted.example.org"]


def create_redirect_url(base_url: str, next_param: str | None) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g. "https://app.example.com/").
    next_param : str | None
        The user supplied redirect target.  May be a relative path,
        an absolute URL, or ``None``/empty string.

    Returns
    -------
    str
        A fully qualified URL that is guaranteed to point to the same
        host as ``base_url`` or an explicitly allowed external domain.

    Raises
    ------
    ValueError
        If ``next_param`` resolves to a location outside the allowed
        domain set.
    """
    if not next_param:
        # Default to base URL when nothing is provided
        return base_url

    # Resolve the target relative to the base URL.
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse both URLs to compare components.
    base_parsed = urllib.parse.urlparse(base_url)
    target_parsed = urllib.parse.urlparse(resolved)

    # Normalise scheme to lower-case for comparison.
    base_scheme = base_parsed.scheme.lower()
    target_scheme = target_parsed.scheme.lower()

    # Ensure the scheme is safe (http/https).
    if target_scheme not in {"http", "https"}:
        raise ValueError("Disallowed URL scheme")

    # Compare hostnames.  Allow the target to be:
    #   * exactly the same as the base host
    #   * one of the explicitly allowed external domains.
    target_host = target_parsed.hostname
    if not target_host:
        raise ValueError("Target URL has no host")

    base_host = base_parsed.hostname
    if target_host == base_host:
        # Same domain – safe.
        return resolved

    if target_host in ALLOWED_DOMAINS:
        # Explicitly permitted external domain.
        return resolved

    raise ValueError(f"Redirect to untrusted host: {target_host}")