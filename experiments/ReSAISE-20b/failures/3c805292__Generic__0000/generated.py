import re
from urllib.parse import urlparse, urlunparse, ParseResult

# List of fully qualified domain names that are allowed to provide RSS feeds.
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogger.com",                     # e.g., https://blogger.com/feeds/posts/default
    "wordpress.com",
    "medium.com",
}

# Regular expression for matching private IP addresses (RFC 1918 + localhost)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                                  # start of string
        (?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or local address."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _is_trusted_domain(host: str) -> bool:
    """Check if the host ends with any of the trusted domains."""
    # Normalize trailing dot
    host = host.rstrip(".")
    return any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS)

def validate_feed_source(feed_address: str) -> str:
    """
    Validate that the given RSS feed URL is from a trusted provider and does not
    point to an internal network address.

    Parameters:
        feed_address (str): The RSS feed URL to validate.

    Returns:
        str: A sanitized, validated URL.

    Raises:
        ValueError: If the URL is not trusted or points to a restricted network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Strip userinfo if present
    netloc = parsed.netloc.split("@")[-1]

    # Resolve potential IPv6 literal or hostname
    host = netloc.split(":")[0]  # ignore port

    # Basic IP address check (no DNS resolution)
    if re.match(r"^\[?[0-9a-fA-F:.]+\]?$", host):  # IPv4 or IPv6 literal
        # Remove surrounding brackets for IPv6
        host_ip = host.strip("[]")
        if _is_private_ip(host_ip):
            raise ValueError(f"URL points to a private IP address: {host_ip}")

    # Domain validation
    if not _is_trusted_domain(host):
        raise ValueError(f"Host '{host}' is not in the list of trusted providers")

    # Rebuild a sanitized URL (remove fragments)
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=netloc,
        path=parsed.path or "",
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(sanitized)