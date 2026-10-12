import urllib.parse

# List of external domains that are considered safe for redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_param : str
        The user-supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully-qualified URL that the application may safely redirect to.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application domain or to an
        unapproved external domain.
    """
    if not app_url:
        raise ValueError("app_url must be a non-empty string")

    # Ensure app_url is normalized (no trailing slash)
    base = urllib.parse.urlparse(app_url.rstrip("/"))
    if not base.scheme or not base.netloc:
        raise ValueError("app_url must be a valid absolute URL")

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect is a relative path, simply join it with the base
    if not parsed_redirect.scheme and not parsed_redirect.netloc:
        # Ensure it starts with a slash to avoid missing path separator
        rel_path = parsed_redirect.path if parsed_redirect.path.startswith("/") else f"/{parsed_redirect.path}"
        # Preserve query and fragment from the redirect_param
        rel_path = urllib.parse.urlunparse(("", "", rel_path, parsed_redirect.params,
                                            parsed_redirect.query, parsed_redirect.fragment))
        return urllib.parse.urljoin(app_url.rstrip("/") + "/", rel_path)

    # If the redirect is absolute, check that it points to a safe domain
    if parsed_redirect.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed for redirection")

    redirect_netloc = parsed_redirect.netloc.lower()
    base_netloc = base.netloc.lower()

    # Allow redirect to the same domain as the application
    if redirect_netloc == base_netloc:
        return urllib.parse.urlunparse(parsed_redirect)

    # Allow redirect to approved external domains
    if any(redirect_netloc == domain.lower() or redirect_netloc.endswith("." + domain.lower())
           for domain in APPROVED_DOMAINS):
        return urllib.parse.urlunparse(parsed_redirect)

    # All other cases are disallowed
    raise ValueError(f"Redirect URL '{redirect_param}' is not allowed")