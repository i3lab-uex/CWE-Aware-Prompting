import re
from urllib.parse import urlparse, urlunparse

# List of approved target domains (exact match or subdomain allowed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regular expression to validate URL schemes
SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def handle_user_redirect(user_url: str) -> str:
    """
    Safely validates a user-provided URL against an approved domain list
    and returns the sanitized URL ready for redirection.

    Parameters:
        user_url (str): The raw URL input from the user.

    Returns:
        str: A fully qualified, validated URL that can be safely redirected to.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    or its domain is not in the approved list.
    """
    # Basic sanity check for scheme
    if not SCHEME_RE.match(user_url):
        raise ValueError("URL must start with http:// or https://")

    # Parse the URL
    parsed = urlparse(user_url)

    # Reject URLs with no netloc (e.g., "http://")
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalize the hostname (lowercase, strip port)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Allow subdomains of approved domains
    def is_approved(hostname: str) -> bool:
        for domain in APPROVED_DOMAINS:
            if hostname == domain or hostname.endswith("." + domain):
                return True
        return False

    if not is_approved(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no hidden characters or fragments
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # query
        "",  # fragment
    ))

    return sanitized


# Example usage (would normally be called from a web framework handler)
if __name__ == "__main__":
    try:
        url = handle_user_redirect("https://sub.example.com/welcome?foo=bar")
        print(f"Redirect to: {url}")
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")