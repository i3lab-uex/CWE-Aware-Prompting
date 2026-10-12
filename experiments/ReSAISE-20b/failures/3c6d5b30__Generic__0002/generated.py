import urllib.parse

# Example list of domains that are considered safe for external redirects.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application (e.g. "https://myapp.com/").
    next_redirect_param : str
        URL path or full address the user wants to navigate to after login.

    Returns
    -------
    str
        Fully-qualified redirect URL that is guaranteed to be within the
        application domain or one of the allowed external domains.

    Raises
    ------
    ValueError
        If `next_redirect_param` resolves to a location that is not within the
        base domain and not in `ALLOWED_DOMAINS`.
    """
    # Parse the base URL once.
    base_parsed = urllib.parse.urlparse(domain_base_url)

    # Normalize the next parameter: strip leading/trailing whitespace.
    next_redirect_param = next_redirect_param.strip()

    # If the next parameter is an absolute URL, parse it.
    parsed_next = urllib.parse.urlparse(next_redirect_param)

    if parsed_next.scheme and parsed_next.netloc:
        # Absolute URL: ensure it belongs to an allowed domain.
        netloc = parsed_next.netloc.lower()
        # Strip default ports for comparison.
        if ':' in netloc:
            host, _ = netloc.split(':', 1)
        else:
            host = netloc
        if host not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to external domain '{host}' is not allowed.")
        # Return the absolute URL unchanged.
        return parsed_next.geturl()

    # Otherwise treat it as a relative path and join with the base URL.
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resulting URL to ensure it stays within the base domain.
    parsed_joined = urllib.parse.urlparse(joined_url)
    if parsed_joined.scheme != base_parsed.scheme or \
       parsed_joined.netloc.lower() != base_parsed.netloc.lower():
        raise ValueError("Redirect URL must be within the application domain.")

    return joined_url