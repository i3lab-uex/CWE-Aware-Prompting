import urllib.parse as urlparse

# Pre‑approved external domains that can be used for redirection
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        Base authentication URL (e.g. "https://app.example.com/login").
    post_login_param : str
        URL path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        Fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside base domain and not in ALLOWED_DOMAINS).
    """
    # Parse the base authentication URL
    base = urlparse.urlparse(auth_base_url)
    if not base.scheme or not base.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Resolve the post_login_param relative to the base
    resolved = urlparse.urljoin(auth_base_url, post_login_param)

    # Parse the resolved URL for validation
    parsed = urlparse.urlparse(resolved)

    # If the URL is relative or empty, treat it as a path on the base domain
    if not parsed.scheme:
        # Construct a URL using the same scheme and netloc as base
        resolved = urlparse.urlunparse(
            (base.scheme, base.netloc, parsed.path or "", parsed.params,
             parsed.query, parsed.fragment)
        )
        parsed = urlparse.urlparse(resolved)

    # Check that the hostname is either:
    # 1. The same as the base domain (or a sub‑domain), or
    # 2. In ALLOWED_DOMAINS.
    host = parsed.hostname.lower() if parsed.hostname else ""
    base_host = base.hostname.lower()

    # Allow sub‑domains of the base host (e.g., api.example.com)
    def is_subdomain(child: str, parent: str) -> bool:
        return child == parent or child.endswith("." + parent)

    if not (is_subdomain(host, base_host) or host in ALLOWED_DOMAINS):
        raise ValueError(f"Unsafe redirect target: {resolved}")

    return resolved