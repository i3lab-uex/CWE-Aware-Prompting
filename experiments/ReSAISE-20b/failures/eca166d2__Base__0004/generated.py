import re
from urllib.parse import urlparse, urlunparse

# A simple whitelist of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "assets.safe-site.net",
}

# Regular expression to detect IP addresses (both IPv4 and IPv6).
IP_ADDRESS_RE = re.compile(
    r"""
    ^
    (?:                                 # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    |
        \[                              # IPv6 start
            (?:[A-Fa-f0-9]{1,4}:){7}
            [A-Fa-f0-9]{1,4}
        \]                              # IPv6 end
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return bool(IP_ADDRESS_RE.match(host))


def validate_image_source(img_src: str) -> str:
    """
    Validate that the provided image URL points to a trusted domain.

    Parameters
    ----------
    img_src : str
        The image URL supplied by an external component.

    Returns
    -------
    str
        The fully-qualified, normalized URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to an IP address,
        or is not on the list of trusted domains.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src)

    # Scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that resolve to an IP address
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("URLs pointing to IP addresses are not allowed")

    # Ensure the host is in the whitelist
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Reconstruct the URL to ensure it is normalized
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=host.lower() + (f":{parsed.port}" if parsed.port else ""),
    )
    return urlunparse(cleaned)


# Example usage (for demonstration only; remove or guard under __name__ == "__main__")
if __name__ == "__main__":
    try:
        url = "https://images.example.com/path/to/image.png"
        print(validate_image_source(url))
    except ValueError as e:
        print(f"Validation failed: {e}")