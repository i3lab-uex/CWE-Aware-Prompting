import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal list of approved RSS providers.
# Extend this list as needed. The list may contain domains or
# subdomains; a regex can be used for more complex matching.
APPROVED_DOMAINS = [
    r"^https?://(www\.)?nytimes\.com/rss/.*$",
    r"^https?://(www\.)?bbc\.co\.uk/news/rss/.*$",
    r"^https?://(www\.)?reuters\.com/news/.*/feed$",
    r"^https?://(www\.)?cnn\.com/rss/.*$",
]

# Compile the regexes once for efficiency
APPROVED_REGEXES = [re.compile(pattern, re.IGNORECASE) for pattern in APPROVED_DOMAINS]


def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or an IPv6
    link-local address.
    """
    try:
        # Resolve host to IP if it's numeric; otherwise skip
        ip = ipaddress.ip_address(host)
    except ValueError:
        # Not a numeric IP; assume it's a hostname.
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the provided RSS feed URL belongs to an approved provider
    and does not target internal or private networks.

    Parameters:
        rss_feed_url (str): The URL to validate.

    Returns:
        str: The sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider or
                    attempts to access a restricted network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("RSS feed URL must be a string")

    parsed = urlparse(rss_feed_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: scheme and netloc required")

    # Reject URLs that use a numeric IP address in the host
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.netloc) or re.match(r"^\[.*\]$", parsed.netloc):
        # Extract the host part (strip brackets for IPv6)
        host = re.sub(r"^\[|\]$", "", parsed.netloc)
        if _is_private_ip(host):
            raise ValueError("URL points to a private or internal IP address")

    # Canonicalize the URL: lower-case scheme and host, remove default ports
    netloc = parsed.netloc.lower()
    if (parsed.scheme == "http" and parsed.port == 80) or (
        parsed.scheme == "https" and parsed.port == 443
    ):
        netloc = re.sub(r":\d+$", "", netloc)

    canonical_url = urlunparse(
        (
            parsed.scheme.lower(),
            netloc,
            parsed.path or "",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    # Check against approved patterns
    for regex in APPROVED_REGEXES:
        if regex.match(canonical_url):
            return canonical_url

    raise ValueError("RSS feed URL is not from an approved provider")