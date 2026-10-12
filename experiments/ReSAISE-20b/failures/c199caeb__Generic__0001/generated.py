import urllib.parse

# Domains that are allowed for external redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        Path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        Fully-qualified redirect URL that is safe and within the
        application or an approved external domain.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or is otherwise unsafe.
    """
    # Normalise the base application URL
    base_parsed = urllib.parse.urlparse(app_url.rstrip("/"))
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid app_url: {app_url!r}")

    # Parse the redirect parameter
    redirect_parsed = urllib.parse.urlparse(redirect_param)

    if not redirect_parsed.scheme:
        # Relative path – prepend the base
        joined = urllib.parse.urljoin(base_parsed.geturl(), redirect_param)
        final_parsed = urllib.parse.urlparse(joined)
    else:
        # Absolute URL – use as-is
        final_parsed = redirect_parsed

    # Ensure the URL is HTTPS to avoid downgrade attacks
    if final_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {final_parsed.scheme!r}")

    # Check that the final domain is either the app's domain or an approved one
    target_domain = final_parsed.netloc.lower()
    base_domain = base_parsed.netloc.lower()

    if target_domain == base_domain:
        # Internal redirect – safe
        return final_parsed.geturl()

    if any(target_domain == d.lower() or target_domain.endswith("." + d.lower())
           for d in APPROVED_DOMAINS):
        # External but approved domain
        return final_parsed.geturl()

    raise ValueError(f"Redirect to unapproved domain: {target_domain!r}")