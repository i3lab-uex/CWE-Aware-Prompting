import urllib.parse as urlparse

# Domains that are allowed for external redirects (example list)
APPROVED_DOMAINS = [
    "trusted.com",
    "partner.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_url : str
        Base application URL (e.g., "https://app.example.com").
    redirect_param : str
        User supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the final URL is not within the application domain or an approved external domain.
    """
    # Parse base and redirect URLs
    app_parsed = urlparse.urlparse(app_url.rstrip("/"))
    redirect_parsed = urlparse.urlparse(redirect_param)

    # If the redirect is a relative path, join it with app_url
    if not redirect_parsed.scheme and not redirect_parsed.netloc:
        # Normalise path to avoid directory traversal
        safe_path = urllib.parse.urljoin(app_parsed.path + "/", redirect_parsed.path)
        final_url = app_parsed._replace(path=safe_path).geturl()
    else:
        # Full URL: validate domain
        redirect_netloc = redirect_parsed.netloc.lower()
        app_domain = app_parsed.hostname.lower()

        if redirect_netloc == app_domain:
            # Internal redirect – ensure path is absolute and not empty
            final_url = redirect_parsed.geturl()
        elif any(redirect_netloc == domain.lower() for domain in APPROVED_DOMAINS):
            # Allowed external redirect
            final_url = redirect_parsed.geturl()
        else:
            raise ValueError("Redirect URL domain is not approved.")

    # Final sanity check: ensure the resulting URL starts with the app base or an approved domain
    final_parsed = urlparse.urlparse(final_url)
    if not (final_parsed.netloc == app_parsed.hostname or
            any(final_parsed.netloc == d.lower() for d in APPROVED_DOMAINS)):
        raise ValueError("Final redirect URL is outside allowed domains.")

    return final_url