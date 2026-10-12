import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (example)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.example.net"
}

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the given domain or any of its parent domains is in ALLOWED_DOMAINS.
    """
    # Normalise domain: lowercase and strip leading/trailing dots
    domain = domain.lower().strip(".")
    # Split into parts and iterate over parent domains
    parts = domain.split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in ALLOWED_DOMAINS:
            return True
    return False

def secure_url_redirect(destination_url: str) -> str:
    """
    Validate the destination URL and return a sanitized version that can be safely used
    for redirection.

    Parameters:
        destination_url (str): The URL provided by the user.

    Returns:
        str: A sanitized, safe-to-use URL.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if the URL is malformed.
    """
    # Basic sanity check: non-empty
    if not destination_url:
        raise ValueError("Destination URL cannot be empty")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Reject URLs without scheme or netloc (e.g., relative paths)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and netloc")

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # Reconstruct the URL to ensure no malicious fragments or parameters are added
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,  # allow query parameters if needed
        ""   # strip fragment to avoid anchor navigation issues
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = secure_url_redirect("https://example.com/path?foo=bar#section")
        print(f"Safe redirect URL: {safe_url}")
    except ValueError as e:
        print(f"Invalid redirection target: {e}")