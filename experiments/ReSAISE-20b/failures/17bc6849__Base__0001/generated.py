import urllib.parse

# Example list of domains that are considered safe for external redirects.
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
        Base URL of the application (e.g. "https://myapp.com/").
    forward_param : str
        User-provided URL path or full URL to redirect to.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    # Parse the forward parameter
    parsed = urllib.parse.urlparse(forward_param)

    # If netloc is empty, treat as a relative path within the app
    if not parsed.netloc:
        # Ensure that the relative path does not escape the base directory
        if parsed.path.startswith("../") or "//" in parsed.path:
            raise ValueError("Invalid relative path for redirection.")
        # Construct the absolute URL
        redirect_url = urllib.parse.urljoin(app_home_url, forward_param)
    else:
        # Absolute URL: validate domain
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        if hostname not in [d.lower() for d in ALLOWED_DOMAINS]:
            raise ValueError(f"Domain '{hostname}' is not allowed for redirection.")
        redirect_url = forward_param

    # Final sanity check: ensure the URL starts with http or https
    if not urllib.parse.urlparse(redirect_url).scheme in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme.")

    return redirect_url