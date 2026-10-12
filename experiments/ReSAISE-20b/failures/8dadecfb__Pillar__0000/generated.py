import urllib.parse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe-domain.net",
}

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated, fully-qualified URL safe for redirection.

    Raises
    ------
    ValueError
        If the input URL is malformed, lacks a scheme or netloc,
        or its domain is not in APPROVED_DOMAINS.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(input_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and domain.")

    # Normalize the netloc: lower case, strip default ports
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    port = parsed.port

    # Remove default ports for comparison
    if (parsed.scheme == "http" and port == 80) or (parsed.scheme == "https" and port == 443):
        netloc = hostname
    else:
        netloc = f"{hostname}:{port}" if port else hostname

    # Verify the domain is approved
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection.")

    # Reconstruct the URL to ensure it is fully qualified
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return safe_url