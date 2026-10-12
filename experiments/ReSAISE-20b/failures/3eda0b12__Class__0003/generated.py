import re
from urllib.parse import urlparse, urljoin

# Domains that are allowed for external redirects (example)
PERMITTED_DOMAINS = [
    "trusted.example.com",
    "api.safe-site.org"
]

# Regex to reject dangerous schemes such as javascript:, data: etc.
INVALID_SCHEMES = re.compile(r"^(javascript|data):", re.IGNORECASE)


def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL based on ``target_param`` after successful login.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    target_param : str
        The user supplied URL path or full URL to redirect to.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application's domain or an allowed external domain,
        or if it contains a disallowed scheme.
    """
    # Reject obviously unsafe schemes early
    if INVALID_SCHEMES.match(target_param.strip()):
        raise ValueError("Unsafe redirect scheme detected")

    # Parse the main application URL once
    base = urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError("Invalid main application URL")

    # Resolve the target relative to the base
    joined = urljoin(main_url, target_param)

    # Parse the resolved URL to inspect components
    parsed = urlparse(joined)

    # Ensure scheme is HTTP/HTTPS (no ftp, file, etc.)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Unsupported URL scheme")

    # If the redirect is relative (no netloc) it automatically resolves to main domain
    if not parsed.netloc:
        return joined

    # For absolute URLs, the netloc must be either the same as main or in PERMITTED_DOMAINS
    if parsed.netloc.lower() == base.netloc.lower():
        return joined

    # Check against permitted external domains
    if parsed.netloc.lower() in (d.lower() for d in PERMITTED_DOMAINS):
        return joined

    # If none of the above, reject
    raise ValueError("Redirect URL is not allowed: outside permitted domains")