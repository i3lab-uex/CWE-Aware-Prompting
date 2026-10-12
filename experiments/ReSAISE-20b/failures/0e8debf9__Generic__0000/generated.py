import urllib.parse as urlparse

# Example list of allowed external domains. In a real application this would
# be defined in configuration.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        Base URL of the authentication application (e.g. "https://app.example.com").
    post_login_param : str
        The URL or path the user wants to go to after login.

    Returns
    -------
    str
        A fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unapproved domain.
    """
    # Normalize base URL (ensure it has a scheme and trailing slash)
    base = urlparse.urljoin(auth_base_url, "/")

    # Resolve the target URL
    target = urlparse.urljoin(base, post_login_param)

    parsed_target = urlparse.urlparse(target)
    parsed_base = urlparse.urlparse(base)

    # If the target is a relative path, it will inherit the base domain
    if not parsed_target.netloc:
        return target

    # If the target has a netloc, ensure it is allowed
    if parsed_target.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed_target.scheme}")

    # Strip port for comparison
    target_domain = parsed_target.hostname or ""
    base_domain = parsed_base.hostname or ""

    if target_domain == base_domain:
        # Same domain – allowed
        return target

    # Check against the list of explicitly permitted external domains
    if target_domain in ALLOWED_DOMAINS:
        return target

    raise ValueError(f"Redirect to unapproved domain: {target_domain}")