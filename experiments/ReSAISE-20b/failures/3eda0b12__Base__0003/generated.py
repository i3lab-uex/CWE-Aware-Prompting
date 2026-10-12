import urllib.parse

# External domains that are considered safe for redirects.
PERMITTED_DOMAINS = [
    "example.com",
    "trusted.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL based on the user's `target_param`.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    target_param : str
        The path or full URL the user wishes to be redirected to.

    Returns
    -------
    str
        A fully qualified URL that is safe to use for redirection.

    Raises
    ------
    ValueError
        If the resolved URL points outside the application domain or an
        unapproved external domain.
    """
    # Normalise and parse the base URL.
    base_parsed = urllib.parse.urlparse(main_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid main_url: must contain scheme and netloc")

    # If target_param is an absolute URL, validate its domain.
    target_parsed = urllib.parse.urlparse(target_param)
    if target_parsed.scheme in ("http", "https"):
        # Absolute URL: ensure it is on a permitted domain.
        if target_parsed.netloc not in PERMITTED_DOMAINS:
            raise ValueError(f"Redirect to untrusted domain: {target_parsed.netloc}")
        # Use the target as is.
        final_url = urllib.parse.urlunparse(target_parsed)
    else:
        # Relative path: join with the base URL.
        final_url = urllib.parse.urljoin(main_url, target_param)
        # Ensure the resulting URL still points to the same domain.
        final_parsed = urllib.parse.urlparse(final_url)
        if final_parsed.netloc != base_parsed.netloc:
            raise ValueError("Redirect would leave the application domain")

    return final_url