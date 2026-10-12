import urllib.parse

# Pre-approved external domains that can be used for redirection.
ALLOWED_DOMAINS = {"example.com", "trustedsite.org"}

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        Base authentication URL (e.g., "https://app.example.com").
    post_login_param : str
        Path or full URL to redirect to after login.

    Returns
    -------
    str
        Fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain or is otherwise unsafe.
    """
    # Parse the base authentication URL
    base_parsed = urllib.parse.urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Resolve the post-login target against the base
    resolved = urllib.parse.urljoin(auth_base_url, post_login_param)
    target_parsed = urllib.parse.urlparse(resolved)

    # If the target is a relative path, it's safe
    if not target_parsed.netloc:
        return resolved

    # If the host matches the base domain, it's safe
    if target_parsed.netloc.lower() == base_parsed.netloc.lower():
        return resolved

    # If the host is in the list of allowed external domains, it's safe
    if target_parsed.netloc.lower() in ALLOWED_DOMAINS:
        return resolved

    # All other cases are considered unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")