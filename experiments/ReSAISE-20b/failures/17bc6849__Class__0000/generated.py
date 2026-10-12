import urllib.parse

# List of external domains considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base application URL (e.g., "https://myapp.com/").
    forward_param : str
        User-specified target path or full URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain or is otherwise invalid.
    """
    # Parse the base application URL
    app_parsed = urllib.parse.urlparse(app_home_url)
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError("app_home_url must be a valid absolute URL")

    # Resolve the forward parameter against the base URL
    resolved_url = urllib.parse.urljoin(app_home_url, forward_param)

    # Parse the resulting URL
    resolved_parsed = urllib.parse.urlparse(resolved_url)

    # Ensure scheme is HTTP or HTTPS
    if resolved_parsed.scheme not in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme")

    # Check if the host matches the app's domain
    host = resolved_parsed.netloc.lower()
    base_host = app_parsed.netloc.lower()

    if host == base_host:
        # Internal redirect – allowed
        return resolved_url

    # External domain: verify against ALLOWED_DOMAINS
    # Strip port if present for comparison
    host_no_port = host.split(":")[0]
    if host_no_port in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved_url

    raise ValueError(f"Redirect URL host '{host_no_port}' is not allowed")