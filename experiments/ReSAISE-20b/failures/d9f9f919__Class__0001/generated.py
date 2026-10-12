import urllib.parse

# List of external domains that are allowed for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add other approved domains here
}


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com/").
    redirect_param : str
        The URL path or full URL the user intends to navigate to post-login.

    Returns
    -------
    str
        The resolved redirect URL as a string.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe, i.e., outside the base domain and not in the permitted external domains list.
    """
    # Normalize the base URL to ensure it ends with a slash
    base = app_base_url.rstrip("/") + "/"

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    if parsed_redirect.scheme and parsed_redirect.netloc:
        # The redirect is an absolute URL
        netloc = parsed_redirect.netloc.lower()
        # Strip port if present for domain comparison
        host = netloc.split(":")[0]

        # Check against the allowed domains list
        if host not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to unapproved domain: {host}")

        # Reconstruct the URL to ensure consistent formatting
        safe_url = urllib.parse.urlunparse(parsed_redirect)
    else:
        # The redirect is a relative path
        # Prevent leading double slashes that could bypass base domain check
        if redirect_param.startswith("//"):
            raise ValueError("Redirect parameter starts with //, which is disallowed")

        # Resolve relative path against the base URL
        safe_url = urllib.parse.urljoin(base, redirect_param)

        # After joining, ensure the resulting URL still points to the base domain
        joined_parsed = urllib.parse.urlparse(safe_url)
        if not joined_parsed.netloc or joined_parsed.netloc.lower() != urllib.parse.urlparse(base).netloc.lower():
            raise ValueError("Resolved redirect URL points outside the base domain")

    return safe_url