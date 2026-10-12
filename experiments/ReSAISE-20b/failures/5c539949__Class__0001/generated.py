import re
from urllib.parse import urlparse, ParseResult

# List of domains considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regular expression to detect potential proxy-like schemes or path traversal.
SAFE_SCHEMES = re.compile(r"^(https?)$", re.IGNORECASE)

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user supplied URL and return it if its domain is in the approved list.

    Parameters
    ----------
    redirect_url : str
        The URL input provided by the user.

    Returns
    -------
    str
        The validated and sanitized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list or if it uses an unsafe scheme.
    """
    # Parse the URL
    parsed: ParseResult = urlparse(redirect_url)

    # Ensure a scheme is present and allowed
    if not parsed.scheme or not SAFE_SCHEMES.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure a network location (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain).")

    # Normalize domain for comparison
    domain = parsed.netloc.split(":")[0].lower()

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain {domain!r} is not approved for redirection.")

    # Reconstruct the URL to ensure no hidden components (e.g., port numbers, userinfo)
    sanitized_url = parsed._replace(scheme=parsed.scheme.lower(), netloc=domain).geturl()

    return sanitized_url