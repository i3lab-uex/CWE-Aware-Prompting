import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "upload.wikimedia.org",
    "images.unsplash.com",
    # add more domains here
}

# Regular expression to detect an IPv4 or IPv6 address in the hostname part.
IP_RE = re.compile(
    r"^(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3})$|^(?:\[.*\])$"
)

def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL points to a trusted hosting provider.
    
    Parameters
    ----------
    img_src : str
        The URL to validate.

    Returns
    -------
    str
        The fully qualified, normalized URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, points to an untrusted domain,
        or contains an IP address.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src)

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Hostname check
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a host")

    # Reject URLs that directly reference an IP address
    if IP_RE.match(hostname):
        try:
            ipaddress.ip_address(hostname)
            raise ValueError("Direct IP addresses are not allowed")
        except ValueError:
            # Not a valid IP; continue
            pass

    hostname = hostname.lower()

    # Ensure the host is in the trusted list or a sub‑domain of one
    if not any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Untrusted host: {hostname!r}")

    # Reconstruct the URL to ensure it is canonical
    normalized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return normalized