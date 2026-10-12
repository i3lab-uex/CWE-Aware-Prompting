import urllib.parse

# Example list of domains that are safe to redirect to externally.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "myapp.example.net",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    next_redirect_param : str
        The URL path or full address the user wants to navigate to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting redirect is not within the base domain or an allowed external domain.
    """
    # Parse the base URL
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base URL: {domain_base_url!r}")

    # Resolve the next redirect against the base URL
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resolved URL to inspect its components
    joined_parsed = urllib.parse.urlparse(joined_url)

    # If the redirect is an absolute URL (has a scheme and netloc)
    if joined_parsed.scheme in ("http", "https") and joined_parsed.netloc:
        # If the netloc matches the base domain, it's safe
        if joined_parsed.netloc == base_parsed.netloc:
            return joined_url

        # Otherwise, ensure the netloc is in ALLOWED_DOMAINS
        if joined_parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError(
                f"Redirect to external domain '{joined_parsed.netloc}' is not allowed."
            )
        return joined_url

    # If the redirect does not contain a netloc, it's a relative URL
    if not joined_parsed.netloc:
        return joined_url

    # Any other case is considered unsafe
    raise ValueError(
        f"Redirect URL '{joined_url}' is not a safe target."
    )