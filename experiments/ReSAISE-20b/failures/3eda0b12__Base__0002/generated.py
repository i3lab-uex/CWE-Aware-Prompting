import urllib.parse

# Domains that are explicitly allowed for redirects (e.g. trusted partner sites)
PERMITTED_DOMAINS = [
    "trusted.example.com",
    "partner.org",
    # add more domains as needed
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL based on the user-provided target_param.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    target_param : str
        The user-specified path or URL to redirect to after login.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to stay within the
        application or one of the PERMITTED_DOMAINS.

    Raises
    ------
    ValueError
        If target_param resolves to a domain that is not the same as main_url's
        host or one of the PERMITTED_DOMAINS.
    """
    # Parse the base URL to get its components
    main_parsed = urllib.parse.urlparse(main_url)
    if not main_parsed.scheme or not main_parsed.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Parse the target parameter
    target_parsed = urllib.parse.urlparse(target_param)

    # If the target has a scheme, it's an absolute URL
    if target_parsed.scheme:
        # Ensure the netloc is either the same as main_url or in PERMITTED_DOMAINS
        if target_parsed.netloc not in (main_parsed.netloc, *PERMITTED_DOMAINS):
            raise ValueError(f"Redirect to untrusted domain: {target_parsed.netloc!r}")
        # Return the target as-is (it's already a full URL)
        return urllib.parse.urlunparse(target_parsed)

    # If no scheme, treat as a relative path
    # Resolve it against the base URL to get an absolute URL
    resolved_url = urllib.parse.urljoin(main_url, target_param)

    # Double-check that the resolved URL hasn't changed the domain
    resolved_parsed = urllib.parse.urlparse(resolved_url)
    if resolved_parsed.netloc != main_parsed.netloc:
        raise ValueError(f"Redirect path resolved to a different domain: {resolved_parsed.netloc!r}")

    return resolved_url