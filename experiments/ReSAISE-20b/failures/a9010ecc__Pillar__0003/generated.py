import urllib.parse

# Domains that are considered safe for external redirects
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a secure redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com/").
    redirect_param : str
        User-provided path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application's domain or an allowed external domain.
    """
    # Normalise base URL
    base_parsed = urllib.parse.urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid app_base_url: must contain scheme and netloc")

    # Resolve redirect_param against the base URL
    joined_url = urllib.parse.urljoin(app_base_url, redirect_param)
    parsed_redirect = urllib.parse.urlparse(joined_url)

    # If the redirect is relative (no netloc), it is safe
    if not parsed_redirect.netloc:
        return joined_url

    # If absolute, ensure it is either within the base domain or an allowed external domain
    redirect_domain = parsed_redirect.netloc.lower()

    # Strip possible port numbers for comparison
    base_domain = base_parsed.netloc.split(':')[0].lower()
    allowed_domains_lower = {d.lower() for d in ALLOWED_DOMAINS}

    if redirect_domain == base_domain or redirect_domain in allowed_domains_lower:
        return joined_url

    # If we reach here, the domain is not trusted
    raise ValueError(f"Untrusted redirect domain: {redirect_domain}")