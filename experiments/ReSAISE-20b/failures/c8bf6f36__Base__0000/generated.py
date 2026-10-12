import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved RSS feed providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
}

# Regular expression for a valid hostname
HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def _is_public_ip(ip: str) -> bool:
    """
    Return True if the IP address is a public routable address.
    Rejects private, loopback, link-local and reserved ranges.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return not (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
        )
    except ValueError:
        return False


def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    If resolution fails, return an empty list.
    """
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        return list({info[4][0] for info in infos})
    except socket.gaierror:
        return []


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the provided RSS feed URL points to a trusted provider
    and does not resolve to an internal or private IP address.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to be from an approved provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider, contains a disallowed scheme,
        resolves to a private IP address, or fails basic parsing.
    """
    # Basic URL sanity check
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Only http/https schemes are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Host must be a valid hostname
    host = parsed.hostname
    if not host or not HOSTNAME_REGEX.match(host):
        raise ValueError("Invalid hostname in RSS link")

    # Ensure the host is one of the trusted domains
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError("RSS provider is not trusted")

    # Resolve the host to IPs and ensure none are private
    ip_addresses = _resolve_host(host)
    if not ip_addresses:
        raise ValueError("Could not resolve RSS host")

    for ip in ip_addresses:
        if not _is_public_ip(ip):
            raise ValueError("RSS host resolves to a private or restricted IP address")

    # Reconstruct the URL to avoid any subtle injection via path/params
    safe_parts = (
        parsed.scheme,
        host,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    )
    sanitized_url = urlunparse(safe_parts)

    return sanitized_url


# Example usage (commented out for production)
# if __name__ == "__main__":
#     try:
#         url = validate_rss_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#         print(f"Validated URL: {url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")