import urllib.parse

# Example list of externally allowed domains. In a real application this should be configured securely.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "secure.example.net",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        The path or absolute URL supplied by the user to redirect to.

    Returns
    -------
    str
        The fully-qualified URL to redirect the user to.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the base domain or to an unapproved external domain.
    """
    # Normalize the base URL
    base_parsed = urllib.parse.urlparse(domain_base_url.rstrip('/'))
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid base URL provided")

    # Resolve the next redirect parameter relative to the base
    resolved_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urllib.parse.urlparse(resolved_url)

    # If the scheme is missing (e.g., a relative path), use the base's scheme
    if not target_parsed.scheme:
        target_parsed = target_parsed._replace(scheme=base_parsed.scheme)

    # If the netloc is empty, it's a relative path within the same domain
    if not target_parsed.netloc:
        # Reconstruct using base domain
        safe_url = urllib.parse.urlunparse(
            (
                target_parsed.scheme,
                base_parsed.netloc,
                target_parsed.path or '',
                target_parsed.params,
                target_parsed.query,
                target_parsed.fragment,
            )
        )
        return safe_url

    # For absolute URLs, verify the host
    target_host = target_parsed.hostname.lower() if target_parsed.hostname else ''
    base_host = base_parsed.hostname.lower() if base_parsed.hostname else ''

    # Allow the URL only if it is within the same host as the base
    # or its hostname is in the ALLOWED_DOMAINS list.
    if target_host == base_host:
        return resolved_url

    # Check against the allowed domains list
    if target_host in ALLOWED_DOMAINS:
        return resolved_url

    raise ValueError(
        f"Redirect URL '{resolved_url}' is not within the base domain or an allowed external domain."
    )