import re
from urllib.parse import urlparse

# List of trusted RSS providers (example domains)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.yahoo.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to detect private IP ranges
_PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                                   # 127.0.0.0/8 localhost
    (^10\.)|                                    # 10.0.0.0/8 private network
    (^172\.(1[6-9]|2\d|3[0-1])\. )|             # 172.16.0.0/12 private network
    (^192\.168\.)|                              # 192.168.0.0/16 private network
    (^169\.254\.)|                              # 169.254.0.0/16 link local
    (^::1$)|                                    # IPv6 loopback
    (^(fc00:|fd00:) )                           # IPv6 unique local addresses
    """,
    re.VERBOSE,
)


def _is_private_ip(netloc: str) -> bool:
    """
    Check if the hostname or IP in netloc is a private/internal address.
    Handles both IPv4 and IPv6 literals as well as hostnames that resolve to private IPs.
    """
    # Extract hostname part (strip port if present)
    host = netloc.split(":")[0]

    # If the hostname is an IP literal, check it directly
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) or re.match(r"^\[.*\]$", host):
        # Strip IPv6 brackets
        ip = host.strip("[]")
        return bool(_PRIVATE_IP_RE.search(ip))

    # For non-IP hostnames, perform a simple check: if it is in the trusted list,
    # we consider it safe. Otherwise, we cannot resolve it here and assume
    # potential risk; the caller must verify with DNS if needed.
    return host not in TRUSTED_DOMAINS


def check_rss_source(source_url: str) -> str:
    """
    Validate that the given RSS feed URL originates from a trusted provider
    and does not point to an internal network address.

    Parameters
    ----------
    source_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if it points to a private/internal
        address, or if the domain is not in the list of trusted providers.
    """
    parsed = urlparse(source_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Check for private or internal IPs
    if _is_private_ip(parsed.netloc):
        raise ValueError(f"URL '{source_url}' points to an untrusted or internal address: {parsed.netloc}")

    # Verify domain is in the trusted list
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not a trusted RSS provider.")

    # All checks passed
    return source_url