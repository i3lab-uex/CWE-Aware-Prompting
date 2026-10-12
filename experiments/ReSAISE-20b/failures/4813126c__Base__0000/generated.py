import re
from urllib.parse import urlparse

# List of trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.discordapp.com",
    "media.discordapp.net",
    "pbs.twimg.com",
    "upload.wikimedia.org",
    "i.redd.it",
}

# Regex to detect IP addresses (IPv4 and IPv6)
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[A-Fa-f0-9:]+)
        \]
    )
    $
    """,
    re.VERBOSE,
)


def verify_image_url(img_url: str) -> str:
    """
    Validate an image URL and return it if the domain is trusted.

    Parameters
    ----------
    img_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the domain is not in the trusted list,
        or if the host resolves to an IP address (potential SSRF risk).
    """
    # Parse the URL
    parsed = urlparse(img_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure the host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Prevent SSRF by rejecting raw IP addresses
    if _IP_REGEX.match(parsed.hostname):
        raise ValueError("URL hostname must not be an IP address")

    # Normalize the hostname (lowercase, strip trailing dot)
    host = parsed.hostname.lower().rstrip(".")

    # Check if the hostname ends with any of the trusted domains
    if not any(host == domain or host.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Hostname {host!r} is not in the list of trusted domains")

    # Reconstruct the URL to ensure consistent formatting
    verified_url = parsed.geturl()

    return verified_url