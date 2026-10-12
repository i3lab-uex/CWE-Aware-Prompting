import re
from urllib.parse import urlparse, urlunparse

# A predefined set of domains that are allowed for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Allowed schemes for redirection
ALLOWED_SCHEMES = {"http", "https"}


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the given domain or any of its parent domains is in ALLOWED_DOMAINS.
    """
    # Normalize to lowercase
    domain = domain.lower()
    while True:
        if domain in ALLOWED_DOMAINS:
            return True
        # Stop when we reach the top‑level domain
        if "." not in domain:
            break
        # Strip the leftmost sub‑domain
        domain = ".".join(domain.split(".")[1:])
    return False


def _sanitize_url(parsed: "ParseResult") -> str:
    """
    Reconstruct the URL, stripping unsafe components (e.g., fragments).
    """
    # Remove fragment and query to avoid unintended data leakage
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    return urlunparse(safe_parts)


def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, safe URL that is allowed for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if its domain is not in ALLOWED_DOMAINS.
    """
    # Parse the URL; this also normalizes it
    parsed = urlparse(input_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and domain")

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed")

    # Extract the hostname (exclude port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Sanitize the URL: remove fragments and query strings
    safe_url = _sanitize_url(parsed)

    return safe_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(process_user_redirect("https://example.com/path?query=1#frag"))
#     except ValueError as e:
#         print(f"Redirection blocked: {e}")