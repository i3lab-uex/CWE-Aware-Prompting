import urllib.parse

# Domains considered safe for external redirects (e.g. partner sites)
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL after login.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        The user-provided path or full URL to redirect to.

    Returns
    -------
    str
        A fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resolved URL points outside the application or to an unapproved domain.
    """
    # Ensure app_url is absolute and has a scheme
    base_parsed = urllib.parse.urlparse(app_url)
    if not base_parsed.scheme:
        raise ValueError("Base application URL must include a scheme (http/https).")

    # Resolve the redirect target relative to the base URL
    resolved = urllib.parse.urljoin(app_url, redirect_param)

    # Parse the final URL to examine its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the redirect is a relative path, it will have an empty netloc
    if not target_parsed.netloc:
        # Relative path is safe because it stays within the app domain
        return resolved

    # Absolute URLs must be checked against allowed domains
    host = target_parsed.netloc.lower()
    # Strip possible port number for comparison
    host_without_port = host.split(":")[0]

    # Check if the target is within the same domain as app_url
    base_host = base_parsed.netloc.lower().split(":")[0]
    if host_without_port == base_host:
        return resolved

    # Check against approved external domains
    if host_without_port in (d.lower() for d in APPROVED_DOMAINS):
        return resolved

    # If none of the checks pass, reject the redirect
    raise ValueError(f"Redirect target '{resolved}' is not allowed.")