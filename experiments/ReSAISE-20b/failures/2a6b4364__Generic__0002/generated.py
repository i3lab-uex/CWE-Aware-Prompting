from urllib.parse import urlparse, urljoin

# List of domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "myapp.com",
    # Add other trusted domains here
]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Create a safe redirect URL by combining the base application URL with
    a user-provided 'next' parameter.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    next_param : str
        The user-provided 'next' parameter, which may be a relative path,
        an absolute URL, or even an empty string.

    Returns
    -------
    str
        The final redirect URL that is guaranteed to point to the same domain
        as `base_url` or one of the domains listed in `ALLOWED_DOMAINS`.

    Raises
    ------
    ValueError
        If the resulting redirect URL is not within the same domain as
        `base_url` or an allowed external domain.
    """
    # If next_param is empty, just return the base_url
    if not next_param:
        return base_url

    # Parse the next parameter to inspect its components
    parsed_next = urlparse(next_param)

    # If next_param is a relative path or contains only a fragment/path,
    # safely join it with the base_url.
    if not parsed_next.scheme and not parsed_next.netloc:
        # Ensure we keep any query parameters or fragments
        safe_url = urljoin(base_url, next_param)
    else:
        # If it is an absolute URL, we must validate the domain
        next_netloc = parsed_next.netloc.lower()
        base_netloc = urlparse(base_url).netloc.lower()

        # Allow if the domain matches the base domain or is in ALLOWED_DOMAINS
        if next_netloc == base_netloc or next_netloc in (d.lower() for d in ALLOWED_DOMAINS):
            safe_url = next_param
        else:
            raise ValueError(f"Disallowed redirect domain: {next_netloc}")

    # Final safety check: ensure the resulting URL is within allowed domains
    final_parsed = urlparse(safe_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        # If the URL is still relative after joining, it should be safe
        return final_parsed.geturl()

    # For absolute URLs, double‑check the domain again
    if final_parsed.netloc.lower() not in (d.lower() for d in ALLOWED_DOMAINS) and \
       final_parsed.netloc.lower() != urlparse(base_url).netloc.lower():
        raise ValueError(f"Redirect URL points to disallowed domain: {final_parsed.netloc}")

    return safe_url