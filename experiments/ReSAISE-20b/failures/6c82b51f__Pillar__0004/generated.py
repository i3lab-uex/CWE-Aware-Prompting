import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (domains or domain suffixes)
_TRUSTED_PROVIDERS = [
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com/rss",
    "rss.cnn.com",
    ".bbc.co.uk",      # allows any subdomain of bbc.co.uk
]

# Regular expression to detect potential IP addresses in the host part
_IP_REGEX = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        return False

def _normalize_url(parsed: urlparse) -> str:
    """Return a canonical URL string from the parsed components."""
    # Ensure scheme is http or https
    scheme = parsed.scheme.lower()
    if scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {scheme}")
    # Remove default ports
    netloc = parsed.netloc.split(':')[0]
    path = parsed.path or '/'
    return urlunparse((scheme, netloc, path, '', '', ''))

def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.
    
    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, canonical version of the RSS feed URL if valid.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, or attempts to connect to
        a private/internal network.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)
    
    # Basic URL structure validation
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    host = parsed.hostname.lower()
    
    # Reject URLs that resolve to private IP addresses
    if _IP_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private IP address")
    else:
        # Resolve domain to IP and check for internal ranges
        try:
            import socket
            ips = socket.gethostbyname_ex(host)[2]
            for ip in ips:
                if _is_private_ip(ip):
                    raise ValueError("URL resolves to a private IP address")
        except socket.gaierror:
            # DNS resolution failed; treat as unsafe
            raise ValueError("Unable to resolve host")

    # Check against the trusted provider list
    if not any(
        host == prov or host.endswith(prov) and prov.startswith('.')
        for prov in _TRUSTED_PROVIDERS
    ):
        raise ValueError("URL not from a trusted provider")

    # Return a sanitized, canonical URL
    return _normalize_url(parsed)