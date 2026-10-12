import urllib.parse as urlparse

# List of external domains that are explicitly allowed for redirects.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com/auth").
    next_route : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe domain (outside of `main_base_url`'s
        host and not in `ALLOWED_DOMAINS`).
    """
    # Parse the base URL to extract its components.
    base_parsed = urlparse.urlparse(main_base_url)

    # Resolve the next_route relative to the base URL.
    resolved = urlparse.urljoin(main_base_url, next_route)

    # Parse the resulting URL to inspect its components.
    resolved_parsed = urlparse.urlparse(resolved)

    # If the URL is relative after joining (i.e., no scheme/host), treat it as
    # relative to the base host.
    if not resolved_parsed.scheme or not resolved_parsed.netloc:
        # Construct a full URL using the base scheme and netloc.
        resolved = f"{base_parsed.scheme}://{base_parsed.netloc}{resolved_parsed.path}"
        if resolved_parsed.query:
            resolved += f"?{resolved_parsed.query}"
        if resolved_parsed.fragment:
            resolved += f"#{resolved_parsed.fragment}"
        resolved_parsed = urlparse.urlparse(resolved)

    # Determine the hostname of the resolved URL.
    host = resolved_parsed.hostname
    if not host:
        raise ValueError("Redirect URL does not contain a hostname")

    # Check if the host matches the base application's host.
    if host == base_parsed.hostname:
        return resolved

    # Check against the list of externally allowed domains.
    if host in ALLOWED_DOMAINS:
        return resolved

    # If none of the checks pass, raise an error to prevent open redirects.
    raise ValueError(
        f"Unsafe redirect target: host '{host}' is not allowed. "
        "Allowed domains: {}.".format(", ".join(ALLOWED_DOMAINS))
    )