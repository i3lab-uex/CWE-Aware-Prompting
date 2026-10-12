import urllib.parse

# Example list of allowed external domains.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g. "https://app.example.com/").
    next_route : str
        The URL path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: it points to a domain that is neither
        the same as `main_base_url` nor in ``ALLOWED_DOMAINS``.
    """
    # Parse the base URL once
    parsed_base = urllib.parse.urlparse(main_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {main_base_url}")

    # Resolve the next route relative to the base
    resolved = urllib.parse.urljoin(main_base_url, next_route)

    # Parse the resolved URL to inspect its components
    parsed_resolved = urllib.parse.urlparse(resolved)

    # If the resolved URL has no scheme, treat it as relative and prepend base
    if not parsed_resolved.scheme:
        resolved = urllib.parse.urljoin(main_base_url, next_route)
        parsed_resolved = urllib.parse.urlparse(resolved)

    # Check if the domain is safe
    target_netloc = parsed_resolved.netloc.lower()
    base_netloc = parsed_base.netloc.lower()

    # Strip port for comparison
    target_host = target_netloc.split(":")[0]
    base_host = base_netloc.split(":")[0]

    if target_host == base_host:
        # Same host as the application – safe
        return resolved

    # External domain: must be in ALLOWED_DOMAINS
    if target_host not in {d.lower() for d in ALLOWED_DOMAINS}:
        raise ValueError(f"Unsafe redirect target: {resolved}")

    return resolved