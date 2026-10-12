import re
from urllib.parse import urlparse, ParseResult

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net",
}

# Allowed URL schemes for redirection.
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(hostname: str) -> bool:
    """
    Check if the given hostname is exactly an approved domain or a
    sub‑domain of one.  Sub‑domains are accepted only when the
    base domain matches an approved entry.
    """
    if not hostname:
        return False

    # Normalize to lowercase for comparison
    host = hostname.lower()

    if host in APPROVED_DOMAINS:
        return True

    # Check for sub‑domain (e.g., foo.example.com)
    for domain in APPROVED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False


def validate_redirect_url(input_url: str) -> str:
    """
    Validate that a user supplied URL points to an approved domain
    and uses an allowed scheme.  Return the original URL if it is
    safe, otherwise raise ValueError.

    Parameters:
        input_url (str): The URL supplied by the user.

    Returns:
        str: The validated URL that is safe for redirection.

    Raises:
        ValueError: If the URL's domain is not approved or if the
                    scheme is not allowed.
    """
    # Parse the URL; this will also handle malformed URLs gracefully
    parsed: ParseResult = urlparse(input_url)

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Ensure netloc (hostname + optional port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Extract the hostname (strip port if present)
    host = parsed.hostname

    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to avoid any potential hidden characters
    sanitized = parsed._replace(scheme=parsed.scheme.lower()).geturl()
    return sanitized


# Example usage:
if __name__ == "__main__":
    try:
        safe_url = validate_redirect_url("https://sub.example.com/path?query=1")
        print(f"Safe URL: {safe_url}")
    except ValueError as e:
        print(f"Invalid redirect target: {e}")