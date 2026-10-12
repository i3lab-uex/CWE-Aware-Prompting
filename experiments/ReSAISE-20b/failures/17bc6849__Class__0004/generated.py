import urllib.parse

# List of external domains that are explicitly allowed for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a secure redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://myapp.com/").
    forward_param : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the application domain and not in
        `ALLOWED_DOMAINS`, or if it points to an unsafe scheme.
    """
    # Ensure the base URL is absolute
    parsed_base = urllib.parse.urlparse(app_home_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_home_url must be an absolute URL")

    # Resolve the forward_param relative to the base
    resolved = urllib.parse.urljoin(app_home_url, forward_param)

    parsed_resolved = urllib.parse.urlparse(resolved)

    # Reject unsafe schemes (only http/https are allowed)
    if parsed_resolved.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme}")

    # If the redirect is relative to the same domain, accept it
    if parsed_resolved.netloc == parsed_base.netloc:
        return resolved

    # Otherwise, the domain must be in ALLOWED_DOMAINS
    host = parsed_resolved.hostname
    if host is None or host.lower() not in {d.lower() for d in ALLOWED_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    return resolved