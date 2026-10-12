import urllib.parse

# List of domains that are allowed for external redirects
PERMITTED_DOMAINS = ["example.com", "trusted.example.org"]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    target_param : str
        The user-provided redirect path or URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL would redirect to an untrusted domain.
    """
    # Parse main_url once
    base_parsed = urllib.parse.urlparse(main_url)

    # If target_param is empty or just whitespace, redirect to main_url
    if not target_param or not target_param.strip():
        return base_parsed.geturl()

    # Resolve the target against main_url
    resolved = urllib.parse.urljoin(base_parsed.geturl(), target_param)

    # Parse the resolved URL
    parsed = urllib.parse.urlparse(resolved)

    # If scheme is missing (e.g., relative path), use main_url's scheme
    if not parsed.scheme:
        parsed = parsed._replace(scheme=base_parsed.scheme)

    # If netloc is empty, the URL is relative to main_url; it's safe
    if not parsed.netloc:
        return urllib.parse.urlunparse(parsed)

    # Normalize host to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Allow redirect if the host matches main_url's host
    if host == base_parsed.hostname.lower():
        return urllib.parse.urlunparse(parsed)

    # Allow redirect if host is in PERMITTED_DOMAINS
    if host in [d.lower() for d in PERMITTED_DOMAINS]:
        return urllib.parse.urlunparse(parsed)

    # All other cases are disallowed
    raise ValueError(f"Redirect to untrusted domain '{host}' is not allowed.")