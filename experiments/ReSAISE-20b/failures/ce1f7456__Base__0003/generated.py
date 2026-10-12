import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (example)
ALLOWED_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted.example.net"
}

# Regex to reject IPv4/IPv6 addresses
IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
      |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            )
        \]
    )$
    """,
    re.VERBOSE
)

def secure_url_redirect(destination_url: str) -> str:
    """
    Validates and sanitizes a user-provided URL for redirection.

    Parameters
    ----------
    destination_url : str
        The user supplied URL to redirect to.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, if the domain is not in
        ALLOWED_DOMAINS, or if an IP address is used instead of a domain.
    """
    # Parse the URL
    parsed = urlparse(destination_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Reject IP addresses
    if IP_REGEX.match(parsed.netloc.split(":")[0]):
        raise ValueError("Redirecting to an IP address is disallowed")

    # Extract the hostname for whitelist check
    host = parsed.hostname.lower()
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct a clean URL (normalise path, query, fragment)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        re.sub(r"/+", "/", parsed.path),  # collapse multiple slashes
        "",   # params (deprecated)
        parsed.query,
        ""    # fragment
    ))

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        url = secure_url_redirect("https://example.com/some/path?x=1#frag")
        print(f"Safe URL: {url}")
    except ValueError as e:
        print(f"Redirect rejected: {e}")