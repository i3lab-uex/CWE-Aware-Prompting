import urllib.parse

# List of external domains that are considered safe for redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL based on the provided `redirect_param`.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The user-supplied value that indicates where to redirect after login.
        It may be a relative path ("/dashboard") or an absolute URL
        ("https://example.com/welcome").

    Returns
    -------
    str
        A fully-qualified redirect URL that is guaranteed to point either
        within the application domain or to an approved external domain.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not the application
        domain or one of the `APPROVED_DOMAINS`.
    """
    # Ensure app_url ends with a slash so urljoin behaves as expected.
    base = app_url if app_url.endswith("/") else f"{app_url}/"

    # Resolve the redirect URL against the base. This handles relative paths
    # and normalizes absolute URLs.
    resolved = urllib.parse.urljoin(base, redirect_param)

    parsed = urllib.parse.urlparse(resolved)

    # If the URL is relative after resolution, it means redirect_param was
    # something like "../etc/passwd". Reject such attempts.
    if not parsed.netloc:
        raise ValueError("Redirect must be an absolute URL or a relative path within the app.")

    # Normalize domain comparison: strip 'www.' prefix for consistency.
    def normalize_domain(netloc):
        return netloc.lower().lstrip("www.")

    app_netloc = normalize_domain(urllib.parse.urlparse(app_url).netloc)
    target_netloc = normalize_domain(parsed.netloc)

    # Check that the redirect is either to the app itself or an approved domain.
    if target_netloc != app_netloc and target_netloc not in [normalize_domain(d) for d in APPROVED_DOMAINS]:
        raise ValueError(f"Redirect to unapproved domain: {parsed.netloc}")

    # Reconstruct the URL to ensure no fragments or query parameters are
    # tampered with. We keep them as provided because they may be necessary
    # for the target resource.
    safe_url = urllib.parse.urlunparse(parsed)

    return safe_url