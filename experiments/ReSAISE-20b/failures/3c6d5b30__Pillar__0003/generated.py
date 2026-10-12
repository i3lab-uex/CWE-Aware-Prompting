import urllib.parse

# Example list of domains considered safe for external redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (must include scheme and netloc).
    next_redirect_param : str
        The user-specified path or URL to redirect to.

    Returns
    -------
    str
        A fully qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    if not domain_base_url:
        raise ValueError("Base URL cannot be empty")

    # Parse the base URL to extract its components
    parsed_base = urllib.parse.urlparse(domain_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must contain a scheme and netloc")

    # If next_redirect_param is empty or None, redirect to the base URL
    if not next_redirect_param:
        return domain_base_url.rstrip("/")

    # Join the base URL with the provided redirect parameter
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resulting URL to validate it
    parsed_joined = urllib.parse.urlparse(joined_url)

    # 1. If the redirect is relative (no netloc), it's safe
    if not parsed_joined.netloc:
        return joined_url

    # 2. If the redirect points to the same domain as the base, it's safe
    if parsed_joined.netloc.lower() == parsed_base.netloc.lower():
        return joined_url

    # 3. If the redirect points to an allowed external domain, it's safe
    if parsed_joined.netloc.lower() in (d.lower() for d in ALLOWED_DOMAINS):
        return joined_url

    # Anything else is considered unsafe
    raise ValueError(
        f"Redirect URL '{joined_url}' is not allowed. "
        "Must be within the base domain or an explicitly permitted external domain."
    )