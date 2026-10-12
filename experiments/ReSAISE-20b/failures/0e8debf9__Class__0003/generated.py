import urllib.parse as urlparse

# Example list of external domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "subdomain.allowed.net",
}


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Build a safe redirect URL after authentication.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    post_login_param : str
        The user-specified path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe domain that is not in
        ALLOWED_DOMAINS and is not under the auth_base_url domain.
    """
    # Parse the base authentication URL
    base = urlparse.urlparse(auth_base_url)
    if not base.scheme or not base.netloc:
        raise ValueError("Invalid auth_base_url")

    # Resolve the post-login parameter relative to the base URL
    resolved = urlparse.urljoin(auth_base_url, post_login_param)

    # Parse the resulting URL to inspect its components
    parsed = urlparse.urlparse(resolved)

    # Ensure the scheme is HTTP or HTTPS (avoid data:, javascript:, etc.)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # If the host matches the base domain (or a subdomain of it), it's safe
    def is_subdomain(child: str, parent: str) -> bool:
        return child == parent or child.endswith("." + parent)

    base_host = base.hostname.lower()
    target_host = parsed.hostname
    if not target_host:
        raise ValueError("Target URL does not contain a hostname")

    target_host = target_host.lower()

    if is_subdomain(target_host, base_host):
        # Same domain or sub‑domain – safe
        return resolved

    # If not in the same domain, check against the whitelist of allowed external domains
    if target_host in ALLOWED_DOMAINS:
        return resolved

    # If we reach here, the URL is considered unsafe
    raise ValueError(
        f"Unsafe redirect target: {resolved} not in allowed domains"
    )