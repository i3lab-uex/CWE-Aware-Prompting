import urllib.parse

# Example list of allowed external domains for safe redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "another-safe-site.net"
]


def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        Desired redirect path or URL provided by the user.

    Returns
    -------
    str
        The fully-qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or one of the
        allowed external domains.
    """
    # Ensure app_base_url has a scheme and netloc for proper parsing
    parsed_app = urllib.parse.urlparse(app_base_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError("app_base_url must be a valid absolute URL with scheme and host")

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    if parsed_redirect.scheme and parsed_redirect.netloc:
        # Absolute URL supplied by the user
        redirect_netloc = parsed_redirect.netloc.lower()
        if redirect_netloc != parsed_app.netloc:
            # External domain: must be in the allowed list
            if redirect_netloc not in (d.lower() for d in ALLOWED_DOMAINS):
                raise ValueError(f"Redirect domain '{redirect_netloc}' is not allowed")
        # Return the absolute URL as-is (no modification)
        final_url = urllib.parse.urlunparse(parsed_redirect)
    else:
        # Relative path or incomplete URL: join with app_base_url
        final_url = urllib.parse.urljoin(app_base_url, redirect_param)

        # Verify that the joined URL stays within the base domain
        parsed_final = urllib.parse.urlparse(final_url)
        if parsed_final.netloc.lower() != parsed_app.netloc:
            raise ValueError("Redirect URL resolves to a different domain than the app base")

    # Normalize final URL (remove fragment, ensure path)
    parsed_final = urllib.parse.urlparse(final_url)
    normalized = parsed_final._replace(fragment="")  # drop fragment for safety
    return urllib.parse.urlunparse(normalized)