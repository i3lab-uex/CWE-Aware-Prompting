import urllib.parse as urlparse

# Pre-approved external domains that can be used for redirection.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        Base authentication URL (e.g., "https://app.example.com/auth").
    post_login_param : str
        Desired target URL or path after login. Can be an absolute URL,
        a relative path, or a query string fragment.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the base domain and not in ALLOWED_DOMAINS.
    """
    # Parse the base authentication URL
    base_parsed = urlparse.urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Resolve the target URL
    resolved = urlparse.urljoin(auth_base_url, post_login_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urlparse.urlparse(resolved)

    # If the scheme or netloc is missing, treat it as a relative path
    if not target_parsed.scheme and not target_parsed.netloc:
        # Ensure it starts with a single slash to avoid double‑slash issues
        path = target_parsed.path or ""
        if not path.startswith("/"):
            path = "/" + path
        resolved = urlparse.urlunparse(
            (base_parsed.scheme, base_parsed.netloc, path,
             target_parsed.params, target_parsed.query, target_parsed.fragment)
        )
    else:
        # Absolute URL: verify domain
        target_domain = target_parsed.netloc.split(":")[0].lower()
        base_domain = base_parsed.netloc.split(":")[0].lower()

        if target_domain != base_domain and target_domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Unsafe redirect URL: {resolved}")

    return resolved