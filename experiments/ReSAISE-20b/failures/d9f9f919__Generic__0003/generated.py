import urllib.parse

# Example list of permitted external domains.
# In real usage, replace this with your application's actual allowed domains.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com/login").
    redirect_param : str
        The URL path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: not within the base domain and not in ALLOWED_DOMAINS.
    """
    # Validate base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid app_base_url: {app_base_url!r}")

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect is an absolute URL
    if parsed_redirect.scheme and parsed_redirect.netloc:
        base_domain = parsed_base.netloc.lower()
        redirect_domain = parsed_redirect.netloc.lower()

        # Allow same‑domain redirects
        if redirect_domain == base_domain:
            return redirect_param

        # Allow external domains that are explicitly permitted
        if redirect_domain in (d.lower() for d in ALLOWED_DOMAINS):
            return redirect_param

        # Any other external domain is disallowed
        raise ValueError(f"Redirect URL domain not allowed: {redirect_domain!r}")

    # If the redirect is relative (path, query, fragment), safely join it with base
    joined_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Ensure the joined URL does not contain a scheme that could be dangerous
    parsed_joined = urllib.parse.urlparse(joined_url)
    if parsed_joined.scheme not in ("http", "https"):
        raise ValueError(f"Disallowed scheme in redirect URL: {parsed_joined.scheme!r}")

    return joined_url