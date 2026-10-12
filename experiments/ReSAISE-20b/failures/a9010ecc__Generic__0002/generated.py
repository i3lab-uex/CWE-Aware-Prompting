import urllib.parse

# Example list of domains that are considered safe for external redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted-site.org",
    "myapp.example.net",
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_param : str
        The user-provided path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the target is not within the application domain and is not an allowed external domain.
    """
    # Normalize base URL
    parsed_base = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Parse the redirect target
    parsed_target = urllib.parse.urlparse(redirect_param)

    # Case 1: relative path (no scheme, no netloc)
    if not parsed_target.scheme and not parsed_target.netloc:
        # Join the relative path with the base URL
        final_url = urllib.parse.urljoin(app_base_url, redirect_param)
        return final_url

    # Case 2: absolute URL
    target_domain = parsed_target.netloc.lower()
    if not parsed_target.scheme or not parsed_target.netloc:
        raise ValueError("redirect_param must be a valid absolute URL if it contains a scheme")

    # Check that the target domain is either the same as the base or in ALLOWED_DOMAINS
    if (target_domain == parsed_base.netloc.lower()) or (target_domain in {d.lower() for d in ALLOWED_DOMAINS}):
        # Return the target as-is (already absolute)
        return redirect_param

    raise ValueError(
        f"Redirect target '{redirect_param}' is not allowed. "
        f"Allowed external domains: {ALLOWED_DOMAINS}"
    )