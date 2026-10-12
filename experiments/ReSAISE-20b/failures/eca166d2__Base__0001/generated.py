import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted image hosting providers (full domain names)
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.imgur.com",
    "storage.googleapis.com",
    "images.unsplash.com",
    # add more domains as needed
}

# Regular expression to detect IP addresses (IPv4 and IPv6)
IP_REGEX = re.compile(
    r"""
    ^\s*
    (?:                             # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    |
        \[?                         # optional opening bracket for IPv6
        (?:[0-9a-fA-F]{1,4}:){7}
        [0-9a-fA-F]{1,4}
        \]?                         # optional closing bracket
    )
    \s*$
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address."""
    return bool(IP_REGEX.match(host))

def _normalize_url(parsed: urlparse) -> str:
    """Reconstruct the URL ensuring default port handling."""
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc
    path = parsed.path or "/"
    return urlunparse((scheme, netloc, path, "", "", ""))

def validate_image_source(img_src: str) -> str:
    """
    Validate that `img_src` points to a trusted image hosting domain.
    
    Parameters
    ----------
    img_src : str
        The URL to validate.

    Returns
    -------
    str
        The fully resolved, normalized URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the scheme is not http/https, the host is an IP address,
        or the domain is not in the trusted list.
    """
    if not isinstance(img_src, str):
        raise ValueError("Image source must be a string")

    parsed = urlparse(img_src)

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host extraction and validation
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses to mitigate SSRF
    if _is_ip_address(host):
        raise ValueError("IP address hosts are not allowed")

    # Normalize subdomains: allow only exact match or subdomain of trusted domains
    host_lower = host.lower()
    if not any(
        host_lower == domain or host_lower.endswith("." + domain)
        for domain in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Untrusted host: {host}")

    # Return the normalized URL
    return _normalize_url(parsed)