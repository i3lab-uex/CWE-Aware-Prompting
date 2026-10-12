import urllib.parse

# Domains that are considered safe for external redirection.
APPROVED_DOMAINS = [
    "trusted.example.com",
    "partner.org",
    # Add more domains as needed
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL based on the user supplied ``redirect_param``.
    
    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. ``https://app.example.com``).
    redirect_param : str
        The user supplied path or full URL to redirect to after login.
    
    Returns
    -------
    str
        The fully resolved, safe URL that the application should redirect to.
    
    Raises
    ------
    ValueError
        If ``redirect_param`` resolves to a URL that is not within the same origin
        as ``app_url`` or does not belong to one of :data:`APPROVED_DOMAINS`.
    """
    # Parse the base application URL
    app_parsed = urllib.parse.urlparse(app_url)
    if not (app_parsed.scheme and app_parsed.netloc):
        raise ValueError(f"Invalid application URL: {app_url}")

    # Resolve the redirect target relative to the base
    joined = urllib.parse.urljoin(app_url, redirect_param)
    target_parsed = urllib.parse.urlparse(joined)

    # Ensure the scheme is HTTP/HTTPS
    if target_parsed.scheme not in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme")

    # If the target is relative (no netloc), it's safe to redirect
    if not target_parsed.netloc:
        # Rebuild the URL relative to app_url (preserve path/query/fragment)
        return urllib.parse.urlunparse((
            target_parsed.scheme or app_parsed.scheme,
            target_parsed.netloc or app_parsed.netloc,
            target_parsed.path,
            target_parsed.params,
            target_parsed.query,
            target_parsed.fragment,
        ))

    # For absolute URLs, check that the host matches app_url or is approved
    target_host = target_parsed.hostname.lower()
    app_host = app_parsed.hostname.lower()

    if target_host == app_host:
        # Same origin: safe
        return joined

    if target_host in {d.lower() for d in APPROVED_DOMAINS}:
        # Approved external domain: safe
        return joined

    raise ValueError(
        f"Redirect target '{joined}' is not within the application domain "
        f"or an approved external domain."
    )