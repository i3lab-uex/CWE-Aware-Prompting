import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (use FQDNs only)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.net",
}

# Regular expression to detect potentially malicious schemes or relative URLs
SAFE_SCHEMES = {"http", "https"}


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that the user supplied URL is safe for redirection.

    The function ensures that:
      * The URL uses an allowed scheme (http/https).
      * The hostname matches one of the approved domains.
      * The URL is absolute (no relative paths).
    If any check fails, a ValueError is raised.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated, absolute URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    # Parse the URL
    parsed = urlparse(input_link)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in SAFE_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Ensure the URL is absolute (netloc must be present)
    if not parsed.netloc:
        raise ValueError("Relative URLs are not allowed.")

    # Extract hostname (lowercase for comparison)
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("URL does not contain a valid hostname.")

    # Domain must match exactly one of the approved domains
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection.")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed)

    return safe_url


# Example usage (commented out)
# try:
#     redirect_to = validate_safe_redirect("https://example.com/path?query=123")
#     print(f"Redirecting to: {redirect_to}")
# except ValueError as e:
#     print(f"Redirection blocked: {e}")