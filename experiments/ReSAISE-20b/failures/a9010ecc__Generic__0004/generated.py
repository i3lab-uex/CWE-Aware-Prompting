import urllib.parse

# List of external domains that are allowed for redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more allowed domains here
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a secure redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://myapp.com/").
    redirect_param : str
        The URL path or full address the user wants to navigate to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the redirect target is outside the application's domain and not in
        `ALLOWED_DOMAINS`.
    """
    # Normalize base URL to ensure it ends with a slash
    if not app_base_url.endswith("/"):
        app_base_url += "/"

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect is relative, join it with the base URL
    if not parsed_redirect.scheme and not parsed_redirect.netloc:
        final_url = urllib.parse.urljoin(app_base_url, redirect_param)
    else:
        # Absolute URL: validate domain
        netloc = parsed_redirect.netloc.lower()
        if not any(netloc == allowed or netloc.endswith("." + allowed) for allowed in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect domain '{netloc}' is not allowed.")
        final_url = redirect_param

    # Final sanity check: ensure the resulting URL is still within the base domain
    final_parsed = urllib.parse.urlparse(final_url)
    if not (final_parsed.scheme in ("http", "https")):
        raise ValueError("Redirect URL must use http or https scheme.")
    # If the redirect is relative, it will be within app_base_url; otherwise check netloc
    if final_parsed.netloc:
        base_netloc = urllib.parse.urlparse(app_base_url).netloc.lower()
        if final_parsed.netloc != base_netloc:
            # Ensure external redirects are explicitly allowed
            if not any(final_parsed.netloc == allowed or final_parsed.netloc.endswith("." + allowed) for allowed in ALLOWED_DOMAINS):
                raise ValueError(f"Redirect to external domain '{final_parsed.netloc}' is not permitted.")
    return final_url