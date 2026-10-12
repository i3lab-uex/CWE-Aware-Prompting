import re
import socket
from urllib.parse import urlparse
import ipaddress

# Trusted image hosting domains. Add or remove as needed.
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.example.org",
    "pictures.safe-host.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to detect IPv4 or IPv6 addresses in netloc
_IP_RE = re.compile(r"""
    ^(?:
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}  # IPv4
        |
        \[
            (?:(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}      # IPv6
            |
            (?:[0-9a-fA-F]{1,4}:){1,7}:\d+                  # IPv6 with numeric port
            |
            :(?:(?:[0-9a-fA-F]{1,4}:){1,6}[0-9a-fA-F]{1,4}) # IPv6 with leading ::
            |
            (?:[0-9a-fA-F]{1,4}:){2,7}:\d+                  # IPv6 with numeric port
            |
            (?:[0-9a-fA-F]{1,4}:){3,7}:\d+                  # IPv6 with numeric port
        )\]
    )
$""", re.VERBOSE)

def _is_ip_address(netloc: str) -> bool:
    """
    Return True if the netloc part of a URL is an IP address.
    Handles IPv4, IPv6 (with or without port).
    """
    # Strip optional port
    host = netloc.split(":")[0]
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that a picture URL points to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    pic_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original, validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the scheme is not http/https, or if the domain is not in the trusted list,
        or if the URL contains an IP address (to mitigate SSRF).
    """
    # Parse the URL
    parsed = urlparse(pic_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Reject URLs that directly specify an IP address
    if _is_ip_address(parsed.netloc):
        raise ValueError("IP addresses are not allowed in URLs")

    # Validate domain against trusted list
    host = parsed.netloc.split(":")[0].lower()  # drop port if present

    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the trusted list")

    # All checks passed; return the original URL
    return pic_url