import re
from urllib.parse import urlparse, urlunparse, quote_plus, unquote_plus
import ipaddress

# List of approved providers (domains or domain suffixes)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regular expression to detect private IP ranges or localhost
PRIVATE_IP_REGEX = re.compile(
    r"^(?:(?:10|127)\.|(?:172\.(?:1[6-9]|2\d|3[0-1])\.)(?:\d{1,3}\.){2}"
    r"|(?:192\.168)\.(?:\d{1,3}\.){2}"
    r"|0\.0\.0\.0$)"
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or attempts to access a private/internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    # Basic parsing
    parsed = urlparse(rss_link)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http or https schemes are allowed")

    # Resolve hostname to IP if possible
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("Invalid URL: missing hostname")

    # Reject obvious private IP addresses or localhost
    if _is_private_ip(host) or PRIVATE_IP_REGEX.match(host):
        raise ValueError("URL points to a private or internal network")

    # Resolve DNS for host (optional, can be omitted if no network access)
    try:
        import socket
        ip_list = socket.gethostbyname_ex(host)[2]
    except Exception:
        # If DNS resolution fails, we cannot confirm it's safe
        raise ValueError("Unable to resolve hostname")

    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError("URL resolves to a private IP address")

    # Verify that the host is in the whitelist
    if host not in TRUSTED_PROVIDERS:
        # Allow subdomains of trusted providers
        matched = any(host.endswith(f".{trusted}") for trusted in TRUSTED_PROVIDERS)
        if not matched:
            raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure it is properly escaped
    sanitized_path = quote_plus(unquote_plus(parsed.path))
    sanitized_query = parsed.query  # queries are typically safe; adjust if needed
    sanitized_fragment = ""        # discard fragments

    sanitized_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        sanitized_path,
        parsed.params,
        sanitized_query,
        sanitized_fragment
    ))

    return sanitized_url