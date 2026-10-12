import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = ["example.com", "trusted.org"]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g. "https://app.example.com").
    forward_param : str
        User supplied redirect target (path or full URL).

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same domain as `app_home_url`
        and is not one of the externally allowed domains.
    """
    # Parse base URL once
    base = urllib.parse.urlparse(app_home_url)
    if not base.scheme or not base.netloc:
        raise ValueError("Invalid app_home_url")

    # Resolve the forward parameter against the base URL
    resolved = urllib.parse.urljoin(app_home_url, forward_param)

    parsed = urllib.parse.urlparse(resolved)

    # If the resolved URL is relative, return it as a path
    if not parsed.scheme and not parsed.netloc:
        # Ensure it starts with a single slash
        return '/' + parsed.path.lstrip('/')

    # If the scheme is missing, default to https
    if not parsed.scheme:
        parsed = parsed._replace(scheme="https")

    # Validate domain
    target_netloc = parsed.netloc.lower()
    base_netloc = base.netloc.lower()

    if target_netloc == base_netloc:
        # Same host as the app – safe
        return urllib.parse.urlunparse(parsed)

    # Check if the target domain is in the allowed list
    if target_netloc not in ALLOWED_DOMAINS:
        raise ValueError(
            f"Redirect to untrusted domain '{target_netloc}' is not allowed."
        )

    # All checks passed – return the full URL
    return urllib.parse.urlunparse(parsed)