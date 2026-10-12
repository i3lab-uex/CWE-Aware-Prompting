import urllib.parse

# Example list of external domains that are safe for redirection.
ALLOWED_DOMAINS = {"trusted.com", "example.org"}

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    next_redirect_param : str
        The user-specified path or URL to redirect to.

    Returns
    -------
    str
        A fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Parse the base URL
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid base URL")

    # Parse the next redirect parameter
    next_parsed = urllib.parse.urlparse(next_redirect_param)

    # If the user supplied a full URL, we must validate it
    if next_parsed.scheme or next_parsed.netloc:
        # Absolute URL: check domain against allowed list
        if next_parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to untrusted domain: {next_parsed.netloc}")
        # Construct the final URL (scheme and netloc from user input)
        final_url = urllib.parse.urlunparse(next_parsed)
    else:
        # Relative path: safely join with base URL
        final_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Final sanity check: ensure the URL starts with the base domain
    final_parsed = urllib.parse.urlparse(final_url)
    if (final_parsed.scheme, final_parsed.netloc) != (base_parsed.scheme, base_parsed.netloc):
        # If it is an allowed external domain we already checked; otherwise reject
        if final_parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError("Redirect leads outside allowed domains")

    return final_url