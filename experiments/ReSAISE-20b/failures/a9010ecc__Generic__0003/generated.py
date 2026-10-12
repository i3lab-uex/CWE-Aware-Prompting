import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    "secure.net",
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_param : str
        The user-specified path or URL to redirect to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the redirect is not within the application domain or an allowed external
        domain.
    """
    # Normalize base URL (ensure it has a scheme)
    if not urllib.parse.urlparse(app_base_url).scheme:
        raise ValueError("app_base_url must include a scheme (e.g., https://)")

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    if not parsed_redirect.scheme:
        # Treat as a relative path. Join with the base URL.
        joined = urllib.parse.urljoin(app_base_url, redirect_param)
        # Ensure the resulting URL stays within the base domain
        joined_parsed = urllib.parse.urlparse(joined)
        base_netloc = urllib.parse.urlparse(app_base_url).netloc
        if joined_parsed.netloc != base_netloc:
            raise ValueError("Redirect attempts to escape the application domain")
        return joined

    # If a scheme is present, validate the external domain
    redirect_netloc = parsed_redirect.netloc.lower()
    if redirect_netloc not in [d.lower() for d in ALLOWED_DOMAINS]:
        raise ValueError(f"Redirect domain '{redirect_netloc}' is not allowed")

    # Return the redirect URL unchanged (it's already absolute)
    return redirect_param