import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved domains for safe redirects.
# Add any domain you trust here. Subdomains are accepted automatically
# if the base domain matches one of these entries.
APPROVED_DOMAINS = {
    'example.com',
    'trusted.org',
    'myservice.net',
}

# Regular expression to detect IP addresses (IPv4 or IPv6).
IP_REGEX = re.compile(
    r'^(?:'
    r'(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$){4}'          # IPv4
    r'|'
    r'\[?[0-9a-fA-F:]+\]?'                                     # IPv6
    r')$'
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(IP_REGEX.match(host))

def _normalize_host(host: str) -> str:
    """
    Convert host to lowercase and strip any port number.
    Example: 'Example.COM:8080' -> 'example.com'
    """
    host = host.lower()
    if ':' in host:
        host, _port = host.split(':', 1)
    return host

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_link : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the domain is not in the
        approved list, or if the host is an IP address that is not explicitly
        approved.
    """
    # Parse URL components
    parsed = urlparse(input_link)

    # Ensure scheme is http or https only.
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Extract host (netloc may contain userinfo, host, port)
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname.")

    host = _normalize_host(parsed.netloc)

    # Reject raw IP addresses unless explicitly approved
    if _is_ip_address(host) and host not in APPROVED_DOMAINS:
        raise ValueError("IP addresses are not allowed unless explicitly approved.")

    # Check if host ends with an approved domain.
    # This allows subdomains like 'sub.example.com'.
    if not any(host == approved or host.endswith('.' + approved)
               for approved in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not in the list of approved domains.")

    # Reconstruct the URL to ensure it doesn't contain any malicious fragments
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        '',  # params are deprecated in modern URLs
        parsed.query or '',
        ''   # fragment must be removed for redirects
    ))

    return safe_url

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://example.com/page",
        "http://sub.trusted.org/path?foo=bar#section",
        "https://malicious.com/evil",
        "http://127.0.0.1:8000/admin"
    ]

    for url in test_urls:
        try:
            print(f"Original: {url}\nValidated: {validate_safe_redirect(url)}\n")
        except ValueError as e:
            print(f"Original: {url}\nError: {e}\n")