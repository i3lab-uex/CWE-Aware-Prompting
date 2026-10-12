import urllib.parse

# Pre‑approved external domains for safe redirects
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL by joining the base application URL with
    a user‑supplied redirect parameter.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com/").
    redirect_param : str
        User supplied path or absolute URL to redirect to after login.

    Returns
    -------
    str
        The resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain or is otherwise unsafe.
    """
    # Resolve relative URLs against the base URL
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resolved URL
    parsed = urllib.parse.urlparse(resolved)

    # Ensure we have a scheme and netloc (i.e., it is absolute)
    if not parsed.scheme or not parsed.netloc:
        # If the redirect_param was relative and resolved to a relative URL,
        # just return it as is (it will be served by the app)
        return resolved

    # Extract hostname, normalise case
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check if the hostname matches the app's base domain or is in allowed list
    base_parsed = urllib.parse.urlparse(app_base_url)
    app_host = base_parsed.hostname.lower() if base_parsed.hostname else ""

    # Allowed if it is the same host or a sub‑domain of the app host
    def is_subdomain(sub: str, parent: str) -> bool:
        return sub == parent or sub.endswith("." + parent)

    if is_subdomain(host, app_host):
        return resolved

    # Allow certain external domains
    if host in ALLOWED_DOMAINS:
        return resolved

    # Anything else is considered unsafe
    raise ValueError(f"Unsafe redirect URL: {resolved}")