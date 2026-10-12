import urllib.parse
from typing import List


# Define a list of domains that are considered safe for redirection.
SAFE_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    "safe-site.net",
]


def _is_safe_domain(netloc: str) -> bool:
    """
    Check if the netloc (domain part of a URL) is in the SAFE_DOMAINS list.
    The comparison is case‑insensitive and ignores any port numbers.

    Args:
        netloc: The domain part of a URL, possibly including a port (e.g., 'example.com:8080').

    Returns:
        True if the domain is allowed, False otherwise.
    """
    # Strip any port number
    host = netloc.split(":")[0].lower()
    return host in SAFE_DOMAINS


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    The function ensures that:
      * The URL has a scheme of either http or https.
      * The domain (netloc) is in the predefined SAFE_DOMAINS list.
      * No relative URLs or scheme‑less fragments are allowed.

    If the URL passes validation, it is returned unchanged.  Otherwise a
    ValueError is raised.

    Args:
        destination_url: The user‑supplied URL string.

    Returns:
        A sanitized, fully qualified URL that is safe for redirection.

    Raises:
        ValueError: If the URL scheme is unsupported, if the domain is not allowed,
                    or if the URL is malformed.
    """
    if not destination_url:
        raise ValueError("Destination URL must not be empty.")

    parsed = urllib.parse.urlparse(destination_url)

    # Ensure the scheme is present and safe
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure there is a netloc (i.e., not a relative URL)
    if not parsed.netloc:
        raise ValueError("URL must contain a domain (netloc).")

    # Verify the domain is in the allowed list
    if not _is_safe_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed for redirection.")

    # Re‑construct the URL to ensure normalization (e.g., remove duplicate slashes)
    sanitized = urllib.parse.urlunparse(parsed)

    return sanitized