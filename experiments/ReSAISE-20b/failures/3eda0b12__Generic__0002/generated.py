import urllib.parse

# Domains that are allowed for external redirects (e.g. OAuth, social logins)
PERMITTED_DOMAINS = ["example.com", "trustedpartner.org"]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://myapp.com").
    target_param : str
        The URL path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        The full redirect URL that is safe and within allowed domains.

    Raises
    ------
    ValueError
        If the resolved URL points outside of `main_url` or any domain in
        :data:`PERMITTED_DOMAINS`.
    """
    # Normalise the main URL to ensure it has a scheme and netloc
    base = urllib.parse.urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Resolve the target relative to the base URL
    joined = urllib.parse.urljoin(base.geturl(), target_param)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(joined)

    # Allow absolute URLs only if they are within the same host as main_url
    # or belong to one of the permitted external domains.
    if parsed.scheme in ("http", "https"):
        # Compare netlocs case‑insensitively
        target_host = parsed.hostname or ""
        base_host = base.hostname or ""

        if target_host.lower() == base_host.lower():
            # Same origin – safe
            return joined

        if any(target_host.lower() == d.lower() for d in PERMITTED_DOMAINS):
            # Allowed external domain
            return joined

    # If we reach here, the target is either a relative path with no scheme
    # (e.g. "/dashboard") or an unsafe absolute URL.
    if not parsed.scheme:
        # No scheme means it's a relative path; prepend the base
        safe_url = urllib.parse.urljoin(base.geturl(), parsed.path)
        return safe_url

    # All other cases are disallowed
    raise ValueError(f"Redirect to {joined!r} is not allowed")