import re
from urllib.parse import urlparse, urlunparse

# A set of approved external domains for safe redirections
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, validated URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL does not contain an approved domain or scheme,
        or if it is malformed.
    """
    # Strip whitespace and ensure we have a string
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    input_url = input_url.strip()
    if not input_url:
        raise ValueError("URL cannot be empty")

    # Parse the URL
    parsed = urlparse(input_url)

    # Reject relative URLs or those without a scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Normalize host (lowercase) and remove default ports
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Reject IP addresses that are not in the approved list
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        raise ValueError("IP addresses are not allowed as domains")

    # Verify domain against approved list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Reconstruct the URL without any user info or fragment
    safe_parts = (
        parsed.scheme,
        f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        "",  # fragment removed
    )
    safe_url = urlunparse(safe_parts)

    return safe_url

# Example usage (commented out):
# try:
#     result = process_url_redirect("https://example.com/path?query=1")
#     print(f"Safe URL: {result}")
# except ValueError as e:
#     print(f"Invalid URL: {e}")