import urllib.parse

# Example allowed external domains; adjust as needed for your application.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "another-safe-site.net"
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    forward_param : str
        Desired redirect target, either a relative path or an absolute URL.

    Returns
    -------
    str
        A fully qualified redirect URL that is either within the app's domain
        or an allowed external domain.

    Raises
    ------
    ValueError
        If the resulting URL is not safe (i.e., points outside the base domain
        or to an unapproved external domain).
    """
    # Normalize app_home_url (ensure it ends with a slash for urljoin)
    if not app_home_url.endswith("/"):
        base = f"{app_home_url}/"
    else:
        base = app_home_url

    # Resolve the forward target
    joined = urllib.parse.urljoin(base, forward_param)

    parsed_target = urllib.parse.urlparse(joined)
    if not parsed_target.scheme or not parsed_target.netloc:
        # If the target is still relative after join, prepend base scheme/netloc
        parsed_base = urllib.parse.urlparse(base)
        joined = f"{parsed_base.scheme}://{parsed_base.netloc}{joined}"
        parsed_target = urllib.parse.urlparse(joined)

    # Security checks
    base_parsed = urllib.parse.urlparse(base)
    if parsed_target.netloc == base_parsed.netloc:
        # Internal redirect: safe
        return joined

    # External domain: ensure it is allowed
    if parsed_target.netloc in ALLOWED_DOMAINS:
        return joined

    raise ValueError(
        f"Redirect target '{joined}' is not within the base domain or an allowed external domain."
    )