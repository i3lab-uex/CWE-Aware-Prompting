import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    # add more domains as needed
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL by appending ``forward_param`` to the base
    application URL.

    Parameters
    ----------
    app_home_url : str
        The application's base URL (e.g. "https://app.example.com/").
    forward_param : str
        The user supplied path or URL to redirect to after login.

    Returns
    -------
    str
        The fully qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an
        allowed external domain.
    """
    # Ensure the base URL has a scheme; otherwise parsing fails
    if not urllib.parse.urlparse(app_home_url).scheme:
        raise ValueError("app_home_url must be a full URL with scheme")

    # Parse the forward_param
    parsed_forward = urllib.parse.urlparse(forward_param)

    # If the forward param is an absolute URL, verify its domain
    if parsed_forward.scheme and parsed_forward.netloc:
        # Normalize the hostname (lowercase, strip port)
        host = parsed_forward.hostname or ""
        if host.lower() not in [d.lower() for d in ALLOWED_DOMAINS]:
            raise ValueError(f"Redirect to untrusted domain: {host}")
        # Reconstruct the absolute URL (preserve path, query, fragment)
        redirect_url = urllib.parse.urlunparse(parsed_forward._replace(
            scheme=parsed_forward.scheme,
            netloc=host
        ))
    else:
        # Treat as a relative path; join it with the base URL
        redirect_url = urllib.parse.urljoin(app_home_url, forward_param)

    # Final safety check: ensure the redirect URL is either under app_home_url
    # or points to an allowed external domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)

    # Check if the redirect is within the same host as app_home_url
    base_host = urllib.parse.urlparse(app_home_url).hostname or ""
    if parsed_redirect.hostname and parsed_redirect.hostname.lower() == base_host.lower():
        return redirect_url

    # Otherwise it must be an allowed external domain
    if parsed_redirect.hostname and parsed_redirect.hostname.lower() in [d.lower() for d in ALLOWED_DOMAINS]:
        return redirect_url

    raise ValueError(f"Redirect URL not allowed: {redirect_url}")