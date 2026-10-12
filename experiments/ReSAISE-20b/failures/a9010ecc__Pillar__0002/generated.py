import urllib.parse

# List of external domains that are allowed for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL after successful login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_param : str
        The user-provided path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully constructed, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    # Parse the base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Ensure redirect_param is a relative path or a full URL
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If redirect_param is a relative path, join it with the base
    if not parsed_redirect.scheme and not parsed_redirect.netloc:
        # Use urljoin to correctly handle leading slashes
        full_url = urllib.parse.urljoin(app_base_url, redirect_param)
    else:
        # It's a full URL; keep it as is
        full_url = redirect_param

    parsed_full = urllib.parse.urlparse(full_url)

    # Check that the scheme is HTTP or HTTPS
    if parsed_full.scheme not in {"http", "https"}:
        raise ValueError(f"Disallowed URL scheme: {parsed_full.scheme!r}")

    # Normalize netloc (lowercase)
    netloc = parsed_full.netloc.lower()

    # Validate against base domain or allowed domains
    base_domain = parsed_base.hostname.lower() if parsed_base.hostname else ""
    if netloc == base_domain:
        # OK: internal redirect
        return full_url

    # Allow subdomains of the base domain as well
    if netloc.endswith("." + base_domain):
        return full_url

    # Check against allowed external domains
    if any(netloc == d.lower() or netloc.endswith("." + d.lower()) for d in ALLOWED_DOMAINS):
        return full_url

    # If none of the checks passed, reject
    raise ValueError(f"Redirect URL {full_url!r} is not allowed")