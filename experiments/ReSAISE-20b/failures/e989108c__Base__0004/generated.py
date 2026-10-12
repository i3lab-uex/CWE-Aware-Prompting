import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# A set of trusted domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.example.com",
    "images.unsplash.com",
}

# Regular expression to match IPv4 or IPv6 addresses
_IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}
        |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )$
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    try:
        # ipaddress will raise ValueError if host is not a valid IP
        ipaddress.ip_address(host)
        return True
    except ValueError:
        # Fallback to regex for IPv6 literal without brackets
        return bool(_IP_REGEX.match(host))


def _is_trusted_domain(host: str) -> bool:
    """Return True if host ends with a trusted domain and is not an IP."""
    # Reject plain IP addresses
    if _is_ip_address(host):
        return False

    # Normalize host: lower‑case, strip trailing dot
    host = host.lower().rstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS)


def get_image_link(link_image: str) -> str:
    """
    Validate that the provided image URL points to a trusted domain and uses
    a supported scheme (http or https).

    Parameters
    ----------
    link_image : str
        The URL to validate.

    Returns
    -------
    str
        The original, validated URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to an untrusted domain,
        or contains an IP address.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed: ParseResult = urlparse(link_image)

    # Scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc (host) validation
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Reject URLs with IPv6 literals that are not wrapped in brackets
    if "[" in parsed.netloc or "]" in parsed.netloc:
        host = re.sub(r"[\[\]]", "", parsed.netloc.split(":")[0])
    else:
        host = parsed.netloc.split(":")[0]

    if not _is_trusted_domain(host):
        raise ValueError(f"Untrusted domain: {host}")

    # Re‑assemble the URL to ensure it is in a canonical form
    cleaned_url = parsed.geturl()
    return cleaned_url


# Example usage (uncomment to test)
# print(get_image_link("https://i.imgur.com/abc123.jpg"))