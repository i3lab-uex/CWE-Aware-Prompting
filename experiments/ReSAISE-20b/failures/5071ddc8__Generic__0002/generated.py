import urllib.parse

# List of external domains that are allowed for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URI by combining the base application URL with
    a user-specified `next_route`.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g., 'https://app.example.com').
    next_route : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        The resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe domain.
    """
    # Parse base URL once for reuse
    base_parsed = urllib.parse.urlparse(main_base_url)

    # If next_route is an absolute URL, parse it separately
    parsed_next = urllib.parse.urlparse(next_route)

    # If next_route is absolute, validate domain
    if parsed_next.scheme and parsed_next.netloc:
        # Allow only HTTPS for security
        if parsed_next.scheme.lower() != "https":
            raise ValueError(f"Unsafe scheme: {parsed_next.scheme}")

        # Domain must be either the same as base or in ALLOWED_DOMAINS
        host = parsed_next.netloc.lower()
        if host != base_parsed.netloc.lower() and host not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to disallowed domain: {host}")

        # Reconstruct the URL to ensure normalisation
        safe_url = urllib.parse.urlunparse(parsed_next._replace(scheme="https"))
    else:
        # next_route is relative; join with base
        joined = urllib.parse.urljoin(main_base_url, next_route)

        # Re-parse to validate that we didn't escape the base domain
        parsed_joined = urllib.parse.urlparse(joined)
        if parsed_joined.netloc.lower() != base_parsed.netloc.lower():
            raise ValueError("Redirect escapes the base domain")

        safe_url = joined

    return safe_url