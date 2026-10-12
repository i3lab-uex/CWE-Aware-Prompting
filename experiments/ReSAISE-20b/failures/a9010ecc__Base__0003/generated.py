import urllib.parse

# Example list of allowed external domains (can be extended as needed)
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    "sub.domain.net"
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The user supplied path or absolute URL to redirect to.

    Returns
    -------
    str
        A fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    # Normalise base URL to avoid trailing slashes issues
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect target relative to the base
    joined_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resulting URL
    parsed_target = urllib.parse.urlparse(joined_url)

    # If the target is relative (empty scheme/netloc), it is safe
    if not parsed_target.scheme and not parsed_target.netloc:
        # Ensure the path stays within the base URL's root
        if not parsed_target.path.startswith("/"):
            # Normalise relative paths to start with a slash
            joined_url = urllib.parse.urljoin(app_base_url, "/" + redirect_param)
        return joined_url

    # For absolute URLs: check domain against allowed list
    target_netloc = parsed_target.netloc.lower()
    # Strip port if present for comparison
    target_domain = target_netloc.split(":")[0]

    # Check if the domain is the same as app_base_url
    base_domain = parsed_base.netloc.lower()
    if target_domain == base_domain:
        return joined_url

    # Otherwise, verify against ALLOWED_DOMAINS
    if target_domain in (d.lower() for d in ALLOWED_DOMAINS):
        return joined_url

    # If none of the checks passed, reject
    raise ValueError("Redirect URL is not allowed: {}".format(joined_url))