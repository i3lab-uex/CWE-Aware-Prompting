import urllib.parse

# Example list of external domains considered safe for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a secure redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (e.g., "https://app.example.com").
    forward_param : str
        The user supplied redirect target.  It may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Parse the base application URL
    base_parsed = urllib.parse.urlparse(app_home_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid application home URL")

    # Resolve the forward parameter against the base URL
    resolved = urllib.parse.urljoin(app_home_url, forward_param)

    # Parse the resolved URL
    parsed = urllib.parse.urlparse(resolved)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Resolved URL is malformed")

    # Determine if the target domain is safe
    target_domain = parsed.netloc.lower()

    # Allow only URLs that are either:
    #   1) within the same domain as app_home_url
    #   2) in the list of ALLOWED_DOMAINS
    base_domain = base_parsed.netloc.lower()

    if target_domain != base_domain and target_domain not in ALLOWED_DOMAINS:
        raise ValueError(
            f"Redirection to domain '{target_domain}' is not allowed"
        )

    return resolved